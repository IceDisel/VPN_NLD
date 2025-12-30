"""
Подготовка WireGuard-данных для пользователя:
- конфиг
- QR-код
"""

from app.vpn.wg_service import create_wg_client
from app.vpn.wg_config import generate_client_config
from app.vpn.qr import generate_qr_code


async def prepare_wg_for_user() -> dict:
    """
    Полный пайплайн подготовки WireGuard для пользователя.

    Возвращает:
    {
        config_text,
        qr_buffer
    }
    """

    # 1️⃣ Создаём WireGuard-клиента
    client = await create_wg_client()

    # 2️⃣ Генерируем конфиг
    config_text = generate_client_config(
        client_private_key=client["private_key"],
        client_ip=client["ip"]
    )

    # 3️⃣ Генерируем QR
    qr_buffer = generate_qr_code(config_text)

    return {
        "config_text": config_text,
        "qr_buffer": qr_buffer
    }
