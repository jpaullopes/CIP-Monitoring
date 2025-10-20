from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Literal


class SecuritySettings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 0
    
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 20
    RATE_LIMIT_REQUESTS_PER_HOUR: int = 1000
    RATE_LIMIT_WINDOW_MINUTES: int = 1
    
    MAX_REQUEST_BODY_SIZE: int = 10485760
    MAX_FIELD_SIZE: int = 1024
    ENABLE_PAYLOAD_VALIDATION_MIDDLEWARE: bool = True
    
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    ENABLE_JSON_LOGGING: bool = True
    LOG_DIR: str = "./logs"
    LOG_FILE_NAME: str = "app.log"
    LOG_MAX_SIZE_BYTES: int = 10485760
    LOG_BACKUP_COUNT: int = 10
    LOG_SENSOR_DATA: bool = False
    
    ENVIRONMENT: str = "production"
    API_KEY: str | None = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_security_settings() -> SecuritySettings:
    return SecuritySettings()
