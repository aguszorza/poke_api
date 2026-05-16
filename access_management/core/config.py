from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    SECRET_KEY: SecretStr = "my-super-secret-key"
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]
    ACCESS_TOKEN_LIFETIME_MINUTES: int = 60
    DEBUG: bool = False
