"""
Генерация клиентского WireGuard-конфига (.conf)
"""

from app.config import (WG_SERVER_PUBLIC_KEY, WG_SERVER_ENDPOINT, WG_ALLOWED_IPS, WG_PERSISTENT_KEEPALIVE, )


def generate_client_config(client_private_key: str, client_ip: str, ) -> str:
    """
    Генерирует WireGuard-конфиг для клиента.

    client_private_key — приватный ключ клиента
    client_ip          — IP клиента (10.8.0.X)

    Возвращает текст .conf файла
    """

    config = f"""
[Interface]
PrivateKey = {client_private_key}
Address = {client_ip}/32
DNS = 1.1.1.1

[Peer]
PublicKey = {WG_SERVER_PUBLIC_KEY}
Endpoint = {WG_SERVER_ENDPOINT}
AllowedIPs = {WG_ALLOWED_IPS}
PersistentKeepalive = {WG_PERSISTENT_KEEPALIVE}
""".strip()

    return config
