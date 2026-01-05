"""
Отправка WireGuard-конфига пользователю в Telegram.
"""

from aiogram import Bot
from aiogram.types import BufferedInputFile

from app.vpn.wg_delivery import prepare_wg_for_user


async def send_wg_to_user(bot: Bot, chat_id: int, ):
    """
    Полный сценарий:
    - создаёт WireGuard peer
    - генерирует конфиг
    - генерирует QR
    - отправляет всё пользователю
    """

    # 1️⃣ Подготавливаем WireGuard данные
    data = await prepare_wg_for_user()

    config_text = data["config_text"]
    qr_buffer = data["qr_buffer"]

    # 2️⃣ Отправляем инструкцию
    await bot.send_message(
        chat_id,
        (
            "✅ VPN настроен!\n\n"
            "📱 *Мобильный телефон*:\n"
            "1. Установите приложение WireGuard\n"
            "2. Нажмите «+» → «Сканировать QR-код»\n\n"
            "💻 *Компьютер*:\n"
            "1. Установите WireGuard\n"
            "2. Импортируйте файл конфигурации\n"
        ),
        parse_mode="Markdown"
    )

    # 3️⃣ Отправляем QR-код
    await bot.send_photo(chat_id, photo=BufferedInputFile(qr_buffer.getvalue(), filename="wireguard_qr.png"),
                         caption="📱 QR-код для подключения")

    # 4️⃣ Отправляем .conf файл
    await bot.send_document(chat_id, document=BufferedInputFile(config_text.encode(), filename="wireguard.conf"),
                            caption="💻 Файл конфигурации WireGuard")
