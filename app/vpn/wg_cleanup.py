"""
Удаление WireGuard peer по подписке
"""

from app.vpn.docker_wg import DockerWG
from app.db.models import Subscription


async def remove_wg_for_subscription(subscription: Subscription):
    """
    Удаляет WireGuard peer,
    связанный с подпиской.
    """

    # Если это не WireGuard — ничего не делаем
    if subscription.vpn_type != "wireguard":
        return

    # Если peer уже не создан — выходим
    if not subscription.wg_public_key:
        return

    # Удаляем peer из WireGuard
    await DockerWG.remove_peer(subscription.wg_public_key)
