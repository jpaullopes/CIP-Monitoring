from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    api_key: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
