from typing import Protocol, Dict, Any
from enum import Enum


class RateLimitStatus(Enum):
    ALLOWED = "allowed"
    RATE_LIMITED = "rate_limited"


class RateLimitResponse:
    def __init__(
        self,
        status: RateLimitStatus,
        requests_remaining: int,
        retry_after_seconds: int | None = None
    ):
        self.status = status
        self.requests_remaining = requests_remaining
        self.retry_after_seconds = retry_after_seconds
    
    @property
    def is_allowed(self) -> bool:
        return self.status == RateLimitStatus.ALLOWED


class RateLimiter(Protocol):
    def check_rate_limit(self, device_id: str) -> RateLimitResponse:
        ...
    
    def get_requests_remaining(self, device_id: str) -> int:
        ...
    
    def reset_device_limit(self, device_id: str) -> None:
        ...
    
    def get_config(self) -> Dict[str, Any]:
        ...
