"""
Модуль для работы с wg-easy API.

Здесь:
- создание клиента
- получение конфигурации
- удаление клиента

Клиент для wg-easy API.

ВАЖНО:
wg-easy использует cookie-сессию, а НЕ Basic Auth.
"""

import httpx
from app.config import WG_API_URL, WG_API_PASSWORD


class WGEasyClient:
    def __init__(self):
        self.base_url = WG_API_URL
        self.api_url = f"{WG_API_URL}/api"

        # HTTP клиент с поддержкой cookies
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=10.0,
            follow_redirects=True,  # важно!
        )

    async def login(self):
        """
        Логинимся в wg-easy и получаем cookie-сессию.
        """
        """
                Логин в wg-easy.

                ВАЖНО:
                wg-easy принимает password ТОЛЬКО как form-data,
                JSON вызывает 400 Validation Error.
                """
        response = await self.client.post(
            "/api/session",
            data={  # <-- НЕ json
                "password": WG_API_PASSWORD
            }
        )
        response.raise_for_status()

    async def get_clients(self) -> list[dict]:
        """
        Получить список клиентов WireGuard.
        """
        response = await self.client.get("/api/client")
        response.raise_for_status()
        return response.json()

    async def create_client(self, name: str) -> dict:
        """
        Создать нового WireGuard клиента.
        """
        response = await self.client.post(
            "/api/client",
            json={"name": name},
        )
        response.raise_for_status()
        return response.json()

    async def delete_client(self, client_id: str):
        """
        Удалить клиента по ID.
        """
        response = await self.client.delete(f"/api/client/{client_id}")
        response.raise_for_status()

    async def close(self):
        """
        Закрыть HTTP-сессию.
        """
        await self.client.aclose()
