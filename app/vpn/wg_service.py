"""
Сервисный слой WireGuard.

Здесь:
- генерация ключей
- выбор IP
- добавление peer
"""

from app.vpn.docker_wg import DockerWG
from app.vpn.ip_allocator import get_free_ip


async def create_wg_client() -> dict:
    """
    Создаёт нового WireGuard клиента.

    Возвращает:
    {
        private_key,
        public_key,
        ip
    }
    """

    # 1️⃣ Генерируем приватный ключ
    private_key = await DockerWG.generate_private_key()

    # 2️⃣ Получаем публичный ключ
    public_key = await DockerWG.generate_public_key(private_key)

    # 3️⃣ Получаем свободный IP
    ip = await get_free_ip()

    # 4️⃣ Добавляем peer в WireGuard Добавление peer (runtime)
    await DockerWG.add_peer(public_key, ip)

    # 4️⃣ 🔥 Сохраняем конфигурацию (КЛЮЧЕВО!)
    await DockerWG.save_config()

    return {
        "private_key": private_key,
        "public_key": public_key,
        "ip": ip,
    }
