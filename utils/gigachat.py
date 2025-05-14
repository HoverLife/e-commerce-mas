# utils/gigachat.py
import base64
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List

import httpx

from config.configuration import Settings

class GigaChatClient:
    """
    Асинхронный клиент для GigaChat с поддержкой OAuth2 и function calling.
    """
    def __init__(self):
        cfg = Settings()
        self.client_id = cfg.GIGA_CLIENT_ID
        self.client_secret = cfg.GIGA_CLIENT_SECRET
        self.scope = cfg.GIGA_SCOPE
        self.auth_url = cfg.GIGACHAT_AUTH_URL
        self.api_url = cfg.GIGACHAT_API_URL
        self.model = cfg.GIGA_MODEL
        self._token: str | None = None
        self._expiry: datetime | None = None

    async def _refresh_token(self) -> None:
        basic = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {basic}",
            "RqUID": str(uuid.uuid4()),
        }
        data = {"scope": self.scope}
        async with httpx.AsyncClient(verify=False) as client:
            resp = await client.post(self.auth_url, headers=headers, data=data)
        resp.raise_for_status()
        j = resp.json()
        self._token = j["access_token"]
        expires_in = j.get("expires_in", 1800)
        self._expiry = datetime.utcnow() + timedelta(seconds=expires_in - 60)

    async def get_token(self) -> str:
        if not self._token or not self._expiry or datetime.utcnow() >= self._expiry:
            await self._refresh_token()
        return self._token  # type: ignore

    async def chat(self, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        token = await self.get_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        payload = {"model": self.model, "messages": history}
        async with httpx.AsyncClient(verify=False) as client:
            resp = await client.post(self.api_url, headers=headers, json=payload)
        resp.raise_for_status()
        return resp.json()
