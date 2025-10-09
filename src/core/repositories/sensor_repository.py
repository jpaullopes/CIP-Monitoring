from typing import Optional, Any
from threading import Lock


class InMemorySensorRepository:
    """Repository for storing sensor data in memory."""
    
    def __init__(self):
        self._latest_data: Optional[Any] = None
        self._lock = Lock()
    
    async def save_latest(self, data: Any) -> None:
        """Save the latest sensor data thread-safely."""
        with self._lock:
            self._latest_data = data
    
    async def get_latest(self) -> Optional[Any]:
        """Retrieve the latest sensor data thread-safely."""
        with self._lock:
            return self._latest_data
    
    def has_data(self) -> bool:
        """Check if repository has any data."""
        with self._lock:
            return self._latest_data is not None
    
    async def clear_data(self) -> None:
        """Clear all stored data (useful when CIP becomes inactive)."""
        with self._lock:
            self._latest_data = None