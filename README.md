# Goats Miner 🐐

Welcome to the **Goats Miner** repository! Goats Miner is a mini app on Telegram that rewards users with Goats tokens for completing tasks. In the future, these tokens will be convertible to cryptocurrency tokens. Below you'll find instructions on how to get started and run the auto-miner.

## Features ✨

- **Daily Check-In** 📅
- **Auto Mission Completion** 🚀

## Prerequisites ⚙️

Make sure you have Python 3 installed on your machine. You can download it from [python.org](https://www.python.org/downloads/). On Linux, you can install Python 3 using the following commands:

### Installation on Linux (Using `apt`) 🐧

```bash
sudo apt update
sudo apt install python3
sudo apt install python3-pip
```

## Installation 🔧

1. Clone the repository:  
   `git clone https://github.com/buddhhu/Goats`

2. Navigate into the project directory:  
   `cd Goats`

3. Install the required Python packages:  
   `pip3 install -r requirements.txt`

## Setup 🛠️

Before running the project, you need to add your authentication data to the `data.txt` file. Follow these steps to get the auth data:

1. Open Telegram in your web browser.
2. Open the Goats mini-app.
3. Open the DevTools in your browser (usually with `Ctrl+Shift+I` or `Cmd+Option+I`).
4. Go to the **Application** tab.
5. Go to **Session Storage**, `https://dev.goatsbot.xyz` and find `telegram-apps/launch-params`.
6. It will look like `tgWebAppPlatform=weba&tgWebAppThemeParams=...`.
7. Find `query_id` in the value and copy it to the end.
8. Unquote the copied value once, using an online tool.
9. You will get `query_id=...`.

Add this data to the `data.txt` file. If you have multiple accounts, add each account on a new line in the following format:

```
query_id=<your_query_id_1>
query_id=<your_query_id_2>
...
```

## Usage 🚀

To run the project, use the following command:  
`python3 bot.py`

Happy mining! 🌟
