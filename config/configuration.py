import os
from pydantic import BaseSettings

class Configuration(BaseSettings):
    gigi_auth_header: str = os.getenv("GIGA_AUTH_HEADER")
    giga_client_id: str = os.getenv("GIGA_CLIENT_ID")
    giga_client_secret: str = os.getenv("GIGA_CLIENT_SECRET")
    giga_scope: str = os.getenv("GIGA_SCOPE")

    db_host: str = os.getenv("DB_HOST")
    db_port: int = int(os.getenv("DB_PORT", 3306))
    db_user: str = os.getenv("DB_USER")
    db_password: str = os.getenv("DB_PASSWORD")
    db_name: str = os.getenv("DB_NAME")

    class Config:
        env_file = ".env"