from typing import Dict, List
from fastapi import WebSocket
from src.infrastructure.config.settings import settings
from src.infrastructure.logging.config import get_logger

logger = get_logger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connections_per_key: Dict[str, int] = {}

    async def connect(self, websocket: WebSocket, api_key: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connections_per_key[api_key] = self.connections_per_key.get(api_key, 0) + 1
        logger.info(f"WebSocket connected. Total: {len(self.active_connections)}")
        return True

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket disconnected. Total: {len(self.active_connections)}")

    async def broadcast_json(self, data):
        stale = []
        for ws in self.active_connections:
            try:
                await ws.send_json(data)
            except Exception:
                stale.append(ws)
        for s in stale:
            self.disconnect(s)

manager = ConnectionManager()
