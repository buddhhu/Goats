

# Goats Miner 🐐

¡Bienvenido al repositorio de **Goats Miner**! Goats Miner es una mini aplicación en Telegram que recompensa a los usuarios con tokens Goats por completar tareas. En el futuro, estos tokens serán convertibles a tokens de criptomonedas. A continuación, encontrarás instrucciones sobre cómo comenzar y ejecutar el auto-minero.

## Características ✨

- **Registro diario** 📅
- **Completado automático de misiones** 🚀

## Requisitos previos ⚙️

Asegúrate de tener Python 3 instalado en tu máquina. Puedes descargarlo desde [python.org](https://www.python.org/downloads/). En Linux, puedes instalar Python 3 utilizando los siguientes comandos:

### Instalación en Linux (Usando `apt`) 🐧

```bash
sudo apt update
sudo apt install python3
sudo apt install python3-pip
```

## Instalación 🔧

1. Clona el repositorio:  
   `git clone https://github.com/buddhhu/Goats`

2. Navega al directorio del proyecto:  
   `cd Goats`

3. Instala los paquetes de Python requeridos:  
   `pip3 install -r requirements.txt`

## Configuración 🛠️

Antes de ejecutar el proyecto, debes agregar tus datos de autenticación al archivo `data.txt`. Sigue estos pasos para obtener los datos de autenticación:

1. Abre Telegram en tu navegador web.
2. Abre la mini aplicación de Goats.
3. Abre las herramientas de desarrollo en tu navegador (generalmente con `Ctrl+Shift+I` o `Cmd+Option+I`).
4. Ve a la pestaña **Application**.
5. Ve a **Session Storage**, `https://dev.goatsbot.xyz` y busca `telegram-apps/launch-params`.
6. Se verá como `tgWebAppPlatform=weba&tgWebAppThemeParams=...`.
7. Busca `query_id` en el valor y cópialo completo.
8. Decodifica el valor copiado una vez, utilizando una herramienta en línea.
9. Obtendrás `query_id=...`.

Agrega estos datos al archivo `data.txt`. Si tienes varias cuentas, agrega cada una en una nueva línea con el siguiente formato:

```
query_id=<your_query_id_1>
query_id=<your_query_id_2>
...
```

## Uso 🚀

Para ejecutar el proyecto, utiliza el siguiente comando:  
`python3 bot.py`

¡Feliz minería! 🌟
