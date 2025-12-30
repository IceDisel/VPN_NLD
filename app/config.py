from dotenv import load_dotenv
import os

load_dotenv()

TOKEN_API = os.getenv("BOT_TOKEN")
# YOOTOKEN = '381764678:TEST:53426'

WG_API_URL = os.getenv("WG_API_URL")
WG_API_USERNAME = os.getenv("WG_API_USERNAME")
WG_API_PASSWORD = os.getenv("WG_API_PASSWORD")

WG_SERVER_PUBLIC_KEY = os.getenv("WG_SERVER_PUBLIC_KEY")
WG_SERVER_ENDPOINT = os.getenv("WG_SERVER_ENDPOINT")
WG_ALLOWED_IPS = os.getenv("WG_ALLOWED_IPS", "0.0.0.0/0")
WG_PERSISTENT_KEEPALIVE = int(os.getenv("WG_PERSISTENT_KEEPALIVE", 25))

HELP_CMD = """
<b>/start</b> - <em>Запуск бота</em>
<b>/help</b> - <em>Справка</em>
<b>/description</b> - <em>Описание бота</em>
"""

DESCRIPTION = """
VPN сервис
Тут описание бота...
"""

CONNECT_VPN = """
Протоколы для полключения:
"""