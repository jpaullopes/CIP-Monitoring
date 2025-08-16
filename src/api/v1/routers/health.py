from fastapi import APIRouter, status
from src.infrastructure.config.settings import app_state, settings
from src.infrastructure.logging.config import get_logger
from datetime import datetime

router = APIRouter()
logger = get_logger(__name__)

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint for monitoring and load balancers."""
    
    # Basic application info
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.1.0",
        "service": "SensorFlow API - InfluxDB Edition"
    }
    
    # Check InfluxDB connectivity
    influx_status = {
        "connected": app_state.influx_is_connected,
        "host": settings.INFLUX_HOST,
        "database": settings.INFLUX_DATABASE
    }
    
    # Check API keys configuration
    auth_status = {
        "api_key_configured": bool(settings.API_KEY),
        "websocket_api_key_configured": bool(settings.API_KEY_WS)
    }
    
    # Overall health determination
    if not app_state.influx_is_connected:
        health_status["status"] = "degraded"
        health_status["warnings"] = ["InfluxDB connection unavailable"]
    
    if not settings.API_KEY or not settings.API_KEY_WS:
        if "warnings" not in health_status:
            health_status["warnings"] = []
        health_status["warnings"].append("API keys not fully configured")
    
    # Combine all status info
    health_status.update({
        "dependencies": {
            "influxdb": influx_status,
            "authentication": auth_status
        }
    })
    
    return health_status

@router.get("/ping", status_code=status.HTTP_200_OK)
async def ping():
    """Simple ping endpoint for basic connectivity checks."""
    return {"message": "pong", "timestamp": datetime.utcnow().isoformat()}
