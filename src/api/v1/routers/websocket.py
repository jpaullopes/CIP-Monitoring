from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status, Query
from src.infrastructure.websocket.manager import manager
from src.infrastructure.security.api_key import verify_ws_api_key
from src.infrastructure.config.settings import settings
from src.infrastructure.logging.config import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.websocket("/sensor_updates")
async def websocket_sensor_updates_endpoint(
    websocket: WebSocket,
    api_key: str = Query(..., alias="api-key")
):
    if not await verify_ws_api_key(api_key):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid or missing API Key.")
        return

    connection_accepted = await manager.connect(websocket, api_key)
    if not connection_accepted:
        return

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected.")
    finally:
        manager.disconnect(websocket)
