# main.py
from fastapi import FastAPI

from src.config import app_state, EXPECTED_API_KEY, EXPECTED_API_KEY_WS, MAX_WS_CONNECTIONS_PER_KEY
from src.database import initialize_database
from src.routes import api_router, websocket_router
from src.logger_config import setup_logger

# Setup logger
logger = setup_logger(__name__)

# Create FastAPI app
app = FastAPI(title="Resilient Sensor API")

# --- Robust Startup Logic ---
@app.on_event("startup")
async def on_startup():
    """Application startup event handler."""
    logger.info("Application starting...")

    # Check API key configurations
    if not EXPECTED_API_KEY:
        logger.warning("API_KEY (for HTTP endpoints) not defined. HTTP API endpoints might be unprotected or fail.")

    if not EXPECTED_API_KEY_WS:
        logger.warning("API_KEY_WS (for WebSocket endpoint) not defined. WebSocket endpoint might be unprotected or fail.")

    # Log WebSocket connection limits
    if MAX_WS_CONNECTIONS_PER_KEY == 0:
        logger.info("MAX_WS_CONNECTIONS_PER_KEY not defined or set to 0. WebSocket connections will be UNLIMITED per API Key.")
    else:
        logger.info(f"WebSocket connections limited to {MAX_WS_CONNECTIONS_PER_KEY} per API Key.")

    # Initialize database
    initialize_database()

# Include routers
app.include_router(api_router)
app.include_router(websocket_router)
