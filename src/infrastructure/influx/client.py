from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timezone
from src.infrastructure.config.settings import settings, app_state
from src.infrastructure.logging.config import get_logger

logger = get_logger(__name__)
_client: InfluxDBClient | None = None
_write_api = None

def initialize_influx():
    global _client, _write_api
    if _client is not None:
        return _client
    try:
        # Create InfluxDB client with correct URL format
        url = f"http://{settings.INFLUX_HOST}:{settings.INFLUX_PORT}"
        _client = InfluxDBClient(
            url=url,
            token=settings.INFLUX_TOKEN,
            org=settings.INFLUX_ORG
        )
        
        # Create write API
        _write_api = _client.write_api(write_options=SYNCHRONOUS)
        
        # Test connection
        health = _client.health()
        if health.status == "pass":
            # Test write
            test_point = Point("startup_test").field("value", 1).time(datetime.now(timezone.utc))
            _write_api.write(bucket=settings.INFLUX_DATABASE, record=test_point)
            
            app_state.influx_is_connected = True
            logger.info("InfluxDB initialized successfully.")
        else:
            app_state.influx_is_connected = False
            logger.error(f"InfluxDB health check failed: {health.message}")
            
    except Exception as e:
        app_state.influx_is_connected = False
        logger.error(f"Failed to initialize InfluxDB: {e}")
        _client = None
        _write_api = None
    return _client

def get_client() -> InfluxDBClient | None:
    return _client if app_state.influx_is_connected else None

def write_sensor_data(temperature: float, humidity: float, pressure: float, sensor_id: str, client_ip: str | None):
    if not app_state.influx_is_connected or _client is None or _write_api is None:
        logger.warning("Influx unavailable, skipping write.")
        return False
    try:
        point = (
            Point("sensor_readings")
            .tag("sensor_id", sensor_id)
            .tag("client_ip", client_ip or "unknown")
            .field("temperature", float(temperature))
            .field("humidity", float(humidity))
            .field("pressure", float(pressure))
            .time(datetime.now(timezone.utc))
        )
        _write_api.write(bucket=settings.INFLUX_DATABASE, record=point)
        return True
    except Exception as e:
        logger.error(f"Write failed: {e}")
        app_state.influx_is_connected = False
        return False

def close_influx_connection():
    """Close InfluxDB connection."""
    global _client, _write_api
    
    if _client:
        _client.close()
        app_state.influx_is_connected = False
        _client = None
        _write_api = None
        logger.info("InfluxDB connection closed")