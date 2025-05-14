# config/configuration.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int = 5432
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    GIGA_CLIENT_ID: str
    GIGA_CLIENT_SECRET: str
    GIGA_SCOPE: str = "GIGACHAT_API_PERS"
    GIGACHAT_AUTH_URL: str
    GIGACHAT_API_URL: str
    GIGA_MODEL: str = "GigaChat"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
