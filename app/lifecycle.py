from src.infrastructure.influx.client import initialize_influx
from src.infrastructure.logging.config import get_logger

logger = get_logger(__name__)

async def on_startup():
    logger.info("Application starting (lifecycle)...")
    initialize_influx()

async def on_shutdown():
    logger.info("Application shutdown (lifecycle)...")
