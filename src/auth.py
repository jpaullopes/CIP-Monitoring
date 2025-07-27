# auth.py
from fastapi import HTTPException, status, Header
from .config import EXPECTED_API_KEY, EXPECTED_API_KEY_WS
from .logger_config import setup_logger

logger = setup_logger(__name__)

# --- Dependency to Verify API Key (for HTTP endpoint) ---
async def verify_api_key(api_key: str = Header(None, alias="X-API-Key")):
    """Verify API key for HTTP endpoints."""
    if not EXPECTED_API_KEY:
        logger.error("Server Error: Expected API key (HTTP) not configured.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Server configuration error."
        )
    if not api_key or api_key != EXPECTED_API_KEY:
        logger.warning("Attempt to access with invalid API Key (HTTP).")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid or missing API Key."
        )
    return api_key

def verify_websocket_api_key(api_key: str) -> bool:
    """Verify API key for WebSocket connections."""
    if not EXPECTED_API_KEY_WS:
        logger.error("Server Error: Expected API key (WebSocket) not configured.")
        return False
    
    if not api_key or api_key != EXPECTED_API_KEY_WS:
        logger.warning(f"Attempt to access WebSocket with invalid API Key: {api_key}")
        return False
    
    return True
