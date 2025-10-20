from time import time
from collections import defaultdict
from src.infrastructure.security.rate_limit_protocol import (
    RateLimiter,
    RateLimitResponse,
    RateLimitStatus,
)
from src.infrastructure.security.security_settings import get_security_settings
from typing import Dict, Any


class RateLimiterImpl:
    def __init__(self):
        self.settings = get_security_settings()
        self.requests: Dict[str, list] = defaultdict(list)
        self.window_minutes = self.settings.RATE_LIMIT_WINDOW_MINUTES
        self.limit_per_window = self.settings.RATE_LIMIT_REQUESTS_PER_MINUTE
    
    def check_rate_limit(self, device_id: str) -> RateLimitResponse:
        now = time()
        window_start = now - (self.window_minutes * 60)
        
        if device_id not in self.requests:
            self.requests[device_id] = []
        
        self.requests[device_id] = [
            timestamp for timestamp in self.requests[device_id]
            if timestamp > window_start
        ]
        
        if len(self.requests[device_id]) >= self.limit_per_window:
            oldest_request = min(self.requests[device_id])
            retry_after = int((oldest_request + (self.window_minutes * 60)) - now) + 1
            return RateLimitResponse(
                status=RateLimitStatus.RATE_LIMITED,
                requests_remaining=0,
                retry_after_seconds=retry_after,
            )
        
        self.requests[device_id].append(now)
        requests_remaining = self.limit_per_window - len(self.requests[device_id])
        
        return RateLimitResponse(
            status=RateLimitStatus.ALLOWED,
            requests_remaining=requests_remaining,
        )
    
    def get_requests_remaining(self, device_id: str) -> int:
        now = time()
        window_start = now - (self.window_minutes * 60)
        
        if device_id not in self.requests:
            return self.limit_per_window
        
        valid_requests = [
            timestamp for timestamp in self.requests[device_id]
            if timestamp > window_start
        ]
        
        return max(0, self.limit_per_window - len(valid_requests))
    
    def reset_device_limit(self, device_id: str) -> None:
        if device_id in self.requests:
            self.requests[device_id] = []
    
    def get_config(self) -> Dict[str, Any]:
        return {
            "requests_per_minute": self.limit_per_window,
            "window_minutes": self.window_minutes,
            "requests_per_hour": self.settings.RATE_LIMIT_REQUESTS_PER_HOUR,
        }
