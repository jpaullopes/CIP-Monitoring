from typing import Protocol, Any, Dict
from enum import Enum


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogContext:
    def __init__(
        self,
        device_id: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
        latency_ms: float | None = None,
        error_reason: str | None = None,
        user_agent: str | None = None,
    ):
        self.device_id = device_id
        self.endpoint = endpoint
        self.status_code = status_code
        self.latency_ms = latency_ms
        self.error_reason = error_reason
        self.user_agent = user_agent
    
    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}


class SecureLogger(Protocol):
    def log_request(
        self,
        level: LogLevel,
        message: str,
        context: LogContext,
    ) -> None:
        ...
    
    def log_authentication_failure(
        self,
        reason: str,
        device_id: str | None = None,
    ) -> None:
        ...
    
    def log_rate_limit_exceeded(
        self,
        device_id: str,
        requests_made: int,
        limit: int,
    ) -> None:
        ...
    
    def log_payload_validation_failure(
        self,
        device_id: str,
        reason: str,
        size_bytes: int | None = None,
    ) -> None:
        ...
    
    def log_sensor_data_processed(
        self,
        device_id: str,
        latency_ms: float,
    ) -> None:
        ...
