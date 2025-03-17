from dotenv import load_dotenv
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict()

    # fastapi
    port: int = 8080


@lru_cache
def get_conf():
    settings = Settings()
    return settings.dict()
