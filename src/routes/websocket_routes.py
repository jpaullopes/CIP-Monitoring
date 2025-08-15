# routes/websocket_routes.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status, Query
from typing import Optional

from ..models import TemperatureDataResponse
from ..database import get_influx_client
from ..auth import verify_websocket_api_key
from ..config import app_state, MAX_WS_CONNECTIONS_PER_KEY
from ..websocket_manager import manager
from ..logger_config import setup_logger

router = APIRouter()
logger = setup_logger(__name__)

# --- WebSocket Endpoint for clients to listen ---
@router.websocket("/ws/sensor_updates")
async def websocket_sensor_updates_endpoint(
    websocket: WebSocket,
    api_key: str = Query(..., alias="api-key")
):
    """WebSocket endpoint for real-time sensor updates."""
    
    # Verify API key
    if not verify_websocket_api_key(api_key):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid or missing API Key.")
        return

    # Check connection limits
    if (MAX_WS_CONNECTIONS_PER_KEY > 0 and 
        manager.connections_per_key.get(api_key, 0) >= MAX_WS_CONNECTIONS_PER_KEY):
        logger.warning(
            f"WebSocket connection rejected for API Key '{api_key}': "
            f"max connections ({MAX_WS_CONNECTIONS_PER_KEY}) reached. "
            f"Client: {websocket.client.host}"
        )
        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION, 
            reason=f"Max connections ({MAX_WS_CONNECTIONS_PER_KEY}) for this API Key reached."
        )
        return

    # Connect the WebSocket
    connection_accepted = await manager.connect(websocket, api_key)
    if not connection_accepted:
        return

    # Note: InfluxDB doesn't have a simple "get last record" like SQL
    # If you need this functionality, you would need to implement a query
    # For now, we'll skip sending last data and just wait for new data
    logger.info(f"WebSocket connected. Waiting for real-time sensor data...")

    # Keep connection alive
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected gracefully.")
        pass
    except Exception as e:
        logger.exception(f"Unexpected error in WebSocket: {e}")
    finally:
        manager.disconnect(websocket)
