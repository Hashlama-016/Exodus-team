from dotenv import load_dotenv
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict()

    # fastapi
    port: int = 8080
    model_file: str
    api_key: str

    # s3
    aws_endpoint_url: str
    aws_access_key_id: str
    aws_secret_access_key: str
    bucket_name: str


@lru_cache
def get_conf():
    settings = Settings()
    return settings.dict()
