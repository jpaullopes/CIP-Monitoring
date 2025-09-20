from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    API_KEY: str | None = None
    API_KEY_WS: str | None = None
    MAX_WS_CONNECTIONS_PER_KEY: int = 0

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
