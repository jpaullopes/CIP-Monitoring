from src.infrastructure.logging.config import get_logger
from src.core.dependencies import service_factory

logger = get_logger(__name__)

async def on_startup():
    logger.info("Starting SensorFlow API")
    
    # Initialize sensor service from persistent storage
    sensor_service = service_factory.get_sensor_service()
    await sensor_service.initialize_from_persistence()
    
    logger.info("Application startup completed")

async def on_shutdown():
    logger.info("Shutting down SensorFlow API")
    logger.info("Application shutdown completed")
