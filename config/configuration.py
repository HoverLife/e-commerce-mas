from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GIGA_CLIENT_ID: str
    GIGA_CLIENT_SECRET: str
    GIGA_SCOPE: str = "GIGACHAT_API_PERS"
    GIGACHAT_AUTH_URL: str = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    GIGACHAT_API_URL: str = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    GIGA_MODEL: str = "GigaChat"

    DB_HOST: str
    DB_PORT: int = 5432
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
