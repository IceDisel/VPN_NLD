"""
Обёртка для выполнения WireGuard-команд
ВНУТРИ docker-контейнера wg-easy.

Мы используем:
    docker exec wg-easy <command>

Почему так:
- WireGuard работает в контейнере
- wg-easy использует тот же wg0
- UI wg-easy автоматически видит изменения
"""

import asyncio
import re
from typing import List

# Имя контейнера wg-easy
WG_CONTAINER_NAME = "wg-easy"


class DockerWG:
    """
    Класс-обёртка для работы с WireGuard
    через docker exec.
    """

    @staticmethod
    async def _run(cmd: List[str]) -> str:
        """
        Низкоуровневая функция запуска команды.

        cmd — список аргументов БЕЗ docker exec
        пример: ["wg", "show"]

        Возвращает stdout (str)
        """
        process = await asyncio.create_subprocess_exec(
            "docker",
            "exec",
            WG_CONTAINER_NAME,
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise RuntimeError(
                f"Ошибка выполнения команды:\n"
                f"CMD: {' '.join(cmd)}\n"
                f"STDERR: {stderr.decode()}"
            )

        return stdout.decode()

    # =========================
    # WireGuard команды
    # =========================

    @classmethod
    async def wg_show(cls) -> str:
        """
        Аналог:
            docker exec wg-easy wg show
        """
        return await cls._run(["wg", "show"])

    @classmethod
    async def wg_show_conf(cls, interface: str = "wg0") -> str:
        """
        Получить текущий конфиг интерфейса.

        Аналог:
            wg showconf wg0
        """
        return await cls._run(["wg", "showconf", interface])

    @classmethod
    async def generate_private_key(cls) -> str:
        """
        Генерация приватного ключа WireGuard.

        wg genkey
        """
        return (await cls._run(["wg", "genkey"])).strip()

    @classmethod
    async def generate_public_key(cls, private_key: str) -> str:
        """
        Получить публичный ключ из приватного.

        echo <priv> | wg pubkey
        """
        process = await asyncio.create_subprocess_exec(
            "docker",
            "exec",
            WG_CONTAINER_NAME,
            "sh",
            "-c",
            f"echo '{private_key}' | wg pubkey",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise RuntimeError(stderr.decode())

        return stdout.decode().strip()

    @classmethod
    async def get_used_ips(cls, interface: str = "wg0") -> set[str]:
        """
        Возвращает множество занятых IPv4 адресов
        из вывода `wg show`.

        Пример строки:
            allowed ips: 10.8.0.2/32, ...
        """
        output = await cls.wg_show()

        # Регулярка для IPv4 вида 10.8.0.X
        ips = set(
            re.findall(r"10\.8\.0\.\d+", output)
        )

        return ips

    @classmethod
    async def add_peer(
            cls,
            public_key: str,
            ip: str,
            interface: str = "wg0"
    ):
        """
        Добавляет peer в WireGuard.

        Аналог команды:
        wg set wg0 peer <PUBKEY> allowed-ips 10.8.0.X/32
        """
        await cls._run([
            "wg",
            "set",
            interface,
            "peer",
            public_key,
            "allowed-ips",
            f"{ip}/32"
        ])

    @classmethod
    async def save_config(cls, interface: str = "wg0"):
        """
        Сохраняет runtime-конфигурацию WireGuard
        в /etc/wireguard/wg0.conf

        Аналог:
            wg-quick save wg0
        """
        await cls._run([
            "wg-quick",
            "save",
            interface
        ])
