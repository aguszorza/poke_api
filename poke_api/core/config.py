from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    SECRET_KEY: SecretStr = "my-poke-api-secret"
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]
    AUTH_API_BASE_URL: str
    DEBUG: bool = False
