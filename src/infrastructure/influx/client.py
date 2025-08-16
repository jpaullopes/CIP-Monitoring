from influxdb3_python import InfluxDBClient3, Point
from datetime import datetime, timezone
from src.infrastructure.config.settings import settings, app_state
from src.infrastructure.logging.config import get_logger

logger = get_logger(__name__)
_client: InfluxDBClient3 | None = None

def initialize_influx():
    global _client
    if _client is not None:
        return _client
    try:
        _client = InfluxDBClient3(host=settings.INFLUX_HOST, token=settings.INFLUX_TOKEN, database=settings.INFLUX_DATABASE)
        # test write
        test_point = Point("startup_test").field("value", 1).time(datetime.now(timezone.utc))
        _client.write(record=test_point)
        app_state.influx_is_connected = True
        logger.info("InfluxDB initialized successfully.")
    except Exception as e:
        app_state.influx_is_connected = False
        logger.error(f"Failed to initialize InfluxDB: {e}")
        _client = None
    return _client

def get_client() -> InfluxDBClient3 | None:
    return _client if app_state.influx_is_connected else None

def write_sensor_data(temperature: float, humidity: float, pressure: float, sensor_id: str, client_ip: str | None):
    if not app_state.influx_is_connected or _client is None:
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
        _client.write(record=point)
        return True
    except Exception as e:
        logger.error(f"Write failed: {e}")
        app_state.influx_is_connected = False
        return False
