from typing import Protocol, Any, Dict
from fastapi import WebSocket


class SensorDataRepository(Protocol):
    """Protocol for sensor data storage operations."""
    
    async def save_latest(self, data: Any) -> None:
        """Save the latest sensor data."""
        ...
    
    async def get_latest(self) -> Any | None:
        """Retrieve the latest sensor data."""
        ...


class ConnectionManagerProtocol(Protocol):
    """Protocol for managing WebSocket connections."""
    
    async def connect(self, websocket: WebSocket, api_key: str) -> bool:
        """Accept a new WebSocket connection."""
        ...
    
    def disconnect(self, websocket: WebSocket) -> None:
        """Disconnect a WebSocket connection."""
        ...
    
    async def broadcast_json(self, data: Dict[str, Any]) -> None:
        """Broadcast JSON data to all connections."""
        ...


class CipIdService(Protocol):
    """Protocol for managing CIP ID logic."""
    
    def get_current_cip_id(self) -> int:
        """Get the current CIP ID."""
        ...
    
    def update_cip_id(self) -> tuple[int, bool]:
        """Update and return the CIP ID and active status based on timeout logic."""
        ...
    
    def get_active_status(self) -> bool:
        """Get the current active status."""
        ...


class PersistenceService(Protocol):
    """Protocol for persisting CIP state to disk (antifail)."""
    
    async def save_state(self, cip_id: int, active: bool, timestamp: str) -> None:
        """Save CIP state to persistent storage."""
        ...
    
    async def load_state(self) -> Dict[str, Any] | None:
        """Load CIP state from persistent storage."""
        ...