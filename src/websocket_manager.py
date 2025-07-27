# websocket_manager.py
from fastapi import WebSocket
from typing import List, Dict
from .config import MAX_WS_CONNECTIONS_PER_KEY
from .logger_config import setup_logger

logger = setup_logger(__name__)

class ConnectionManager:
    """WebSocket connection manager."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connections_per_key: Dict[str, int] = {}
        self.websocket_to_key_map: Dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket, api_key: str) -> bool:
        """Connect a new WebSocket client."""
        if (MAX_WS_CONNECTIONS_PER_KEY > 0 and 
            self.connections_per_key.get(api_key, 0) >= MAX_WS_CONNECTIONS_PER_KEY):
            logger.warning(
                f"WebSocket connection rejected for API Key '{api_key}': "
                f"max connections ({MAX_WS_CONNECTIONS_PER_KEY}) reached. "
                f"Client: {websocket.client.host}"
            )
            return False

        await websocket.accept()
        self.active_connections.append(websocket)
        self.connections_per_key[api_key] = self.connections_per_key.get(api_key, 0) + 1
        self.websocket_to_key_map[websocket] = api_key
        
        logger.info(
            f"New WebSocket client: {websocket.client.host} (Key: {api_key}). "
            f"Total connections for this key: {self.connections_per_key[api_key]}. "
            f"Global total: {len(self.active_connections)}"
        )
        return True

    def disconnect(self, websocket: WebSocket):
        """Disconnect a WebSocket client."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            api_key = self.websocket_to_key_map.pop(websocket, None)
            if api_key:
                self.connections_per_key[api_key] = self.connections_per_key.get(api_key, 1) - 1
                if self.connections_per_key[api_key] <= 0:
                    del self.connections_per_key[api_key]
                logger.warning(
                    f"WebSocket client disconnected. "
                    f"Total connections for key '{api_key}': {self.connections_per_key.get(api_key, 0)}. "
                    f"Global total: {len(self.active_connections)}"
                )
            else:
                logger.warning(
                    f"WebSocket client disconnected (key not mapped). "
                    f"Global total: {len(self.active_connections)}"
                )
        else:
            logger.warning("Attempted to disconnect a non-active WebSocket.")

    async def broadcast_json(self, data: dict):
        """Broadcast JSON data to all connected clients."""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except Exception:
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for ws_to_remove in disconnected:
            self.disconnect(ws_to_remove)

# Global connection manager instance
manager = ConnectionManager()
