from src.infrastructure.influx.client import initialize_influx, close_influx_connection
from src.infrastructure.logging.config import get_logger

logger = get_logger(__name__)

async def on_startup():
    logger.info("🚀 Starting SensorFlow API - InfluxDB Edition")
    initialize_influx()
    logger.info("✅ Application startup completed")

async def on_shutdown():
    logger.info("🛑 Shutting down SensorFlow API")
    close_influx_connection()
    logger.info("✅ Application shutdown completed")
