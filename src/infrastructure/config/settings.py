from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    API_KEY: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache
def get_settings():
    return Settings()
