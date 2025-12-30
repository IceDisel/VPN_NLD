"""
Генерация QR-кода для WireGuard-конфига
"""

import qrcode
from io import BytesIO


def generate_qr_code(config_text: str) -> BytesIO:
    """
    Генерирует QR-код из текста конфига.

    Возвращает BytesIO (готово для Telegram)
    """

    qr = qrcode.make(config_text)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer
