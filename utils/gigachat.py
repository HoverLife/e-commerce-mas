import base64
import uuid
from datetime import datetime, timedelta
import httpx

from config.configuration import Configuration

class GigaChatClient:
    def __init__(self):
        cfg = Configuration()
        #self.client_id = cfg.GIGA_CLIENT_ID
        #self.client_secret = cfg.GIGA_CLIENT_SECRET
        self.scope = cfg.GIGA_SCOPE
        self.auth_url = cfg.GIGACHAT_AUTH_URL
        self.api_url = cfg.GIGACHAT_API_URL.rstrip("/") + "/chat/completions"
        self.model = cfg.GIGA_MODEL
        self.verify_ssl = False
        self._token: str | None = None
        self._expiry: datetime | None = None

    async def get_token(self) -> str:
        if self._token and self._expiry and datetime.now() < self._expiry:
            return self._token

        basic = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "Authorization": f"Basic {basic}",
            "RqUID": str(uuid.uuid4()),
        }
        data = {"scope": self.scope}
        async with httpx.AsyncClient(verify=self.verify_ssl) as client:
            r = await client.post(self.auth_url, headers=headers, data=data)
        r.raise_for_status()
        js = r.json()
        token = js["access_token"]
        expires = js.get("expires_in", 1800)
        self._token = token
        self._expiry = datetime.now() + timedelta(seconds=expires - 60)
        return token

    async def chat(self, messages: list[dict]) -> dict:
        token = await self.get_token()
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
        }
        payload = {"model": self.model, "messages": messages}
        async with httpx.AsyncClient(verify=self.verify_ssl) as client:
            r = await client.post(self.api_url, headers=headers, json=payload)
        r.raise_for_status()
        return r.json()
