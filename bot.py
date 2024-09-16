from aiohttp import ClientSession
import json, asyncio, sys, random, time
from json.decoder import JSONDecodeError
from math import ceil
from urllib.parse import unquote
from loguru import logger


logger.remove()
logger.add(
    sink=sys.stdout,
    format="<white>{time:YYYY-MM-DD HH:mm:ss}</white>"
    " | <level>{level: <8}</level>"
    " | <cyan><b>{line}</b></cyan>"
    " | <white><b>{message}</b></white>",
)
logger = logger.opt(colors=True)

min_amount_for_spin = 20000
play_spin_wheel = False


class GoatsBot:
    def __init__(self, tg_auth_data: str) -> None:
        self.http = ClientSession()
        self.auth_data = tg_auth_data
        userdata = json.loads(unquote(tg_auth_data).split("user=")[1].split("&auth")[0])
        self.user_id = userdata.get("id")

    @staticmethod
    def decode_json(text: str) -> dict:
        try:
            return json.loads(text)
        except JSONDecodeError:
            return {"error": "Error decoding to json", "text": text}

    async def login(self) -> bool:
        logger.info(f"{self.user_id} | Trying to login...")
        resp = await self.http.post(
            "https://dev-api.goatsbot.xyz/auth/login",
            data={},
            headers={"Rawdata": self.auth_data},
        )
        resp = self.decode_json(await resp.text())
        if resp.get("statusCode"):
            logger.error(f"{self.user_id} | Error while login | {resp['message']}")
            return False
        else:
            _access_token = resp.get("tokens", {}).get("access", {})
            access_token = _access_token.get("token")
            self.http.headers["Authorization"] = f"Bearer {access_token}"
            logger.success(f"{self.user_id} | Login successful")
            return True

    async def profile_data(self) -> dict:
        resp = await self.http.get("https://api-me.goatsbot.xyz/users/me")
        resp = self.decode_json(await resp.text())
        if resp.get("statusCode"):
            logger.error(
                f"{self.user_id} | Error getting profile data | {resp['message']}"
            )
            return False
        else:
            return resp

    async def get_missions(self) -> list:
        resp = await self.http.get("https://api-mission.goatsbot.xyz/missions/user")
        resp = self.decode_json(await resp.text())
        if resp.get("statusCode"):
            logger.error(f"{self.user_id} | Error getting missions | {resp['message']}")
            return False
        else:
            result = []
            for category in resp:
                for mission in resp[category]:
                    if category == "SPECIAL MISSION" and mission.get(
                        "next_time_execute"
                    ) < int(time.time()):
                        result.append(
                            {
                                "id": mission.get("_id"),
                                "name": mission.get("name"),
                                "reward": mission.get("reward"),
                            }
                        )
                    if not mission.get("status", True):
                        result.append(
                            {
                                "id": mission.get("_id"),
                                "name": mission.get("name"),
                                "reward": mission.get("reward"),
                            }
                        )
            return result

    async def complete_mission(self, mission_data: dict) -> bool:
        resp = await self.http.post(
            f"https://dev-api.goatsbot.xyz/missions/action/{mission_data['id']}"
        )
        resp = self.decode_json(await resp.text())
        if resp.get("statusCode"):
            logger.error(
                f"{self.user_id} | Error completing mission | {resp['message']}"
            )
            return False
        else:
            if resp.get("status"):
                logger.success(
                    f"{self.user_id} | Completed mission {mission_data['name']} | Bonus: {mission_data['reward']}"
                )
                return True
            else:
                logger.error(
                    f"{self.user_id} | Mission {mission_data['name']} not fininshed"
                )
                return False

    async def get_checkin(self) -> dict:
        resp = await self.http.get(f"https://api-checkin.goatsbot.xyz/checkin/user")
        resp = self.decode_json(await resp.text())
        if resp.get("statusCode"):
            logger.error(
                f"{self.user_id} | Error getting check-in data | {resp['message']}"
            )
            return False
        else:
            for day in resp["result"]:
                if not day.get("status"):
                    return day

    async def checkin(self, checkin_data: dict) -> dict:
        resp = await self.http.post(
            f"https://api-checkin.goatsbot.xyz/checkin/action/{checkin_data['_id']}"
        )
        resp = self.decode_json(await resp.text())
        if resp.get("statusCode"):
            logger.error(f"{self.user_id} | Error checking in | {resp['message']}")
            return False
        else:
            if resp.get("status"):
                logger.success(
                    f"{self.user_id} | Checked in for day {checkin_data['day']} | Bonus: {checkin_data['reward']}"
                )
                return True
            else:
                logger.error(f"{self.user_id} | Failed to checkin. Try again later.")
                return False

    async def spin_wheel(self, bet_amount: int) -> dict:
        resp = await self.http.post(
            "https://api-wheel.goatsbot.xyz/wheel/action",
            json={"bet_amount": bet_amount, "wheel_seg": "Low"},
        )
        resp = self.decode_json(await resp.text())
        if resp.get("statusCode"):
            logger.error(
                f"{self.user_id} | Error playing spin wheel | {resp['message']}"
            )
            return False
        else:
            if wheel := resp.get("wheel"):
                return wheel

    async def run(self):
        if not await self.login():
            await self.http.close()
            return

        missions_to_complete = await self.get_missions()
        if missions_to_complete:
            for mission_data in missions_to_complete:
                await self.complete_mission(mission_data)
                await asyncio.sleep(random.randint(1, 5))

        checkin_data = await self.get_checkin()
        if checkin_data:
            await self.checkin(checkin_data)
        profile_data = await self.profile_data()
        if profile_data:
            logger.info(
                f"Account ID: {self.user_id} | Balance: {profile_data.get('balance')} | Age: {profile_data.get('age')} years"
            )
        if play_spin_wheel and min_amount_for_spin < int(profile_data.get("balance")):
            current_balance = profile_data.get("balance")
            won, lost = 0, 0
            total_profit = 0
            max_losses = 2

            while True:
                bet_amount = random.randint(
                    ceil((current_balance * 0.1) / 100),
                    ceil((current_balance * 1) / 100),
                )
                result = await self.spin_wheel(bet_amount)
                if not result.get("is_win"):
                    total_profit -= bet_amount
                    logger.error(
                        f"{self.user_id} | Lost {bet_amount}/{bet_amount} coins | Won: {won} | Lost: {lost} | Profit: {total_profit}"
                    )
                    lost += 1
                    if lost >= max_losses:
                        logger.error(f"Lost {lost} bets. Will try later.")
                        break
                else:
                    total_profit += result.get("reward") - bet_amount
                    won += 1
                    logger.success(
                        f"{self.user_id} | Won {result.get('reward') - bet_amount}/{bet_amount} coins | Won: {won} | Lost: {lost} | Profit: {total_profit}"
                    )

                await asyncio.sleep(random.randint(6, 12))
            profile_data = await self.profile_data()
            logger.info(
                f"{self.user_id} | Game Over. Final Balance: {profile_data.get('balance')} | Profit: {total_profit}"
            )
        await self.http.close()


async def main():
    while True:
        with open("data.txt", "r", encoding="utf-8") as file:
            accounts = [line.strip() for line in file if line.strip()]
        for _, auth_data in enumerate(accounts, start=1):
            sleep_between_login = random.randint(10, 20)
            logger.info(f"Sleeping for {sleep_between_login}s before login")
            await asyncio.sleep(sleep_between_login)
            logger.info(f"Account {_}/{len(accounts)}")
            bot = GoatsBot(auth_data.strip())
            await bot.run()
        retry_sleep = random.randint(60, 90)
        logger.info(f"Sleeping for {retry_sleep} minutes.")
        await asyncio.sleep(retry_sleep * 60)


asyncio.run(main())
