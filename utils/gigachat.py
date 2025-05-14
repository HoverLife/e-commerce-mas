import base64
import uuid
from datetime import datetime, timedelta
import httpx
from typing import List, Dict, Any
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GIGA_CLIENT_ID: str
    GIGA_CLIENT_SECRET: str
    GIGA_SCOPE: str
    GIGACHAT_AUTH_URL: str
    GIGACHAT_API_URL: str
    GIGA_MODEL: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

class GigaChatClient:
    def __init__(self):
        cfg = Settings()
        self.client_id = cfg.GIGA_CLIENT_ID
        self.client_secret = cfg.GIGA_CLIENT_SECRET
        self.scope = cfg.GIGA_SCOPE
        self.auth_url = cfg.GIGACHAT_AUTH_URL
        self.api_url = cfg.GIGACHAT_API_URL
        self.model = cfg.GIGA_MODEL
        self._token = None
        self._expiry = None

    async def _refresh_token(self):
        basic = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": f"Basic {basic}", "RqUID": str(uuid.uuid4())}
        data = {"scope": self.scope}
        async with httpx.AsyncClient(verify=False) as client:
            resp = await client.post(self.auth_url, headers=headers, data=data)
        resp.raise_for_status()
        j = resp.json()
        self._token = j["access_token"]
        expires = j.get("expires_in", 1800)
        self._expiry = datetime.utcnow() + timedelta(seconds=expires - 60)
        print ('AAAAAAA')

    async def get_token(self):
        if not self._token or datetime.utcnow() >= self._expiry:
            await self._refresh_token()
            print('BBBBBBB')
        return self._token

    async def chat(self, messages: List[Dict[str, Any]], functions: List[Dict]=None) -> Dict[str, Any]:
        token = await self.get_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        payload = {"model": self.model, "messages": messages}
        if functions:
            payload["functions"] = functions
        async with httpx.AsyncClient(verify=False) as client:
            resp = await client.post(self.api_url, headers=headers, json=payload)
        resp.raise_for_status()
        return resp.json()