import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config import TOKEN_API
from app.bot.handlers import router


async def main():
    bot = Bot(TOKEN_API, default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        ))
    dp = Dispatcher()

    dp.include_router(router)

    print("🚀 Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("⛔ Bot stopped")

