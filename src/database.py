# database.py
from influxdb_client_3 import InfluxDBClient3, Point
from typing import Optional
import datetime

from .config import INFLUX_HOST, INFLUX_TOKEN, INFLUX_DATABASE, app_state
from .logger_config import setup_logger

logger = setup_logger(__name__)

# --- Global Variables for InfluxDB (will be initialized on startup) ---
client = None

def initialize_database():
    """Initialize InfluxDB connection."""
    global client
    
    if not INFLUX_HOST:
        app_state.influx_is_connected = False
        logger.warning("INFLUX_HOST not defined. The application will continue without saving data.")
        return

    try:
        logger.info("Configuring the InfluxDB client...")
        client = InfluxDBClient3(host=INFLUX_HOST, token=INFLUX_TOKEN, database=INFLUX_DATABASE)

        logger.info("Attempting to connect to InfluxDB...")
        # Test connection by attempting to write a test point
        test_point = Point("connection_test") \
            .field("value", 1) \
            .time(datetime.datetime.now(datetime.timezone.utc))
        
        client.write(record=test_point)
        logger.info(f"InfluxDB connection established successfully at {INFLUX_HOST}")

        app_state.influx_is_connected = True

    except Exception as e:
        app_state.influx_is_connected = False
        logger.error("STARTUP ERROR: Could not configure or connect to InfluxDB.")
        logger.warning("The application will continue to receive data, but NOTHING will be saved.")
        logger.error(f"Error detail: {e}")
        client = None

def get_influx_client():
    """Get InfluxDB client."""
    if not app_state.influx_is_connected or not client:
        return None
    return client

def write_sensor_data(temperature: float, humidity: float, pressure: float, sensor_id: str, client_ip: str = None):
    """Write sensor data to InfluxDB."""
    if not app_state.influx_is_connected or not client:
        logger.warning("InfluxDB not available. Data will not be saved.")
        return False

    try:
        point = Point("sensor_readings") \
            .tag("sensor_id", sensor_id) \
            .tag("client_ip", client_ip or "unknown") \
            .field("temperature", float(temperature)) \
            .field("humidity", float(humidity)) \
            .field("pressure", float(pressure)) \
            .time(datetime.datetime.now(datetime.timezone.utc))

        client.write(record=point)
        logger.info(f"Data from sensor {sensor_id} written to InfluxDB successfully")
        return True

    except Exception as e:
        logger.error(f"Error writing to InfluxDB: {e}")
        app_state.influx_is_connected = False
        return False
