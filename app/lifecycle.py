from src.infrastructure.logging.config import get_logger

logger = get_logger(__name__)

async def on_startup():
    logger.info("Starting SensorFlow API - Node-RED Edition")
    logger.info("Application startup completed")

async def on_shutdown():
    logger.info("Shutting down SensorFlow API")
    logger.info("Application shutdown completed")
