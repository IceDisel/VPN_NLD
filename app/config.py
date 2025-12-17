from dotenv import load_dotenv
import os

load_dotenv()

TOKEN_API = os.getenv("BOT_TOKEN")
# YOOTOKEN = '381764678:TEST:53426'

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