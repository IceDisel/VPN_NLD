"""Для создания файла БД
выполнить python -m app.db.init_db !!! Не выполнять как python -m app/db/init_db.py
надо запустить модуль а не файл"""

import asyncio

from app.db.database import engine, Base
from app.db import models  # важно: регистрация моделей


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 🔴 ВАЖНО: закрываем engine
    await engine.dispose()
    print("✅ Database initialized")


if __name__ == "__main__":
    asyncio.run(init_db())
