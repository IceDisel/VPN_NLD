"""
Модуль для выбора свободного IP
в WireGuard-сети.
"""

from app.vpn.docker_wg import DockerWG


async def get_free_ip() -> str:
    """
    Возвращает первый свободный IP
    из диапазона 10.8.0.2–254.
    """
    used_ips = await DockerWG.get_used_ips()

    for i in range(2, 255):
        ip = f"10.8.0.{i}"
        if ip not in used_ips:
            return ip

    raise RuntimeError("❌ Нет свободных IP в пуле")
