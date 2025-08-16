from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    API_KEY: str | None = None
    API_KEY_WS: str | None = None
    INFLUX_HOST: str = "localhost"
    INFLUX_PORT: int = 8181
    INFLUX_TOKEN: str | None = None
    INFLUX_DATABASE: str = "database"
    MAX_WS_CONNECTIONS_PER_KEY: int = 0

    class Config:
        env_file = ".env"
        case_sensitive = True

class AppState:
    def __init__(self):
        self.influx_is_connected: bool = False

app_state = AppState()

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
