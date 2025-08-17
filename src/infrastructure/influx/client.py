from influxdb_client_3 import InfluxDBClient3, Point
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
        # URL baseado no protocolo HTTP direto para InfluxDB v3
        influx_url = f"http://{settings.INFLUX_HOST}:{settings.INFLUX_PORT}"
        
        _client = InfluxDBClient3(
            host=influx_url,
            token=settings.INFLUX_TOKEN, 
            database=settings.INFLUX_DATABASE
        )
        
        # Test write para verificar conectividade
        test_point = Point("startup_test").field("value", 1).time(datetime.now(timezone.utc))
        _client.write(record=test_point)
        
        app_state.influx_is_connected = True
        logger.info("InfluxDB v3 initialized successfully with SQL support.")
        
    except Exception as e:
        app_state.influx_is_connected = False
        logger.error(f"Failed to initialize InfluxDB v3: {e}")
        _client = None
        
    return _client

def get_client() -> InfluxDBClient3 | None:
    return _client if app_state.influx_is_connected else None

def write_sensor_data(temperature: float, humidity: float, pressure: float, sensor_id: str, client_ip: str | None):
    if not app_state.influx_is_connected or _client is None:
        logger.warning("InfluxDB v3 unavailable, skipping write.")
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
        logger.info(f"Data written to InfluxDB v3: sensor={sensor_id}, temp={temperature}")
        return True
        
    except Exception as e:
        logger.error(f"InfluxDB v3 write failed: {e}")
        app_state.influx_is_connected = False
        return False

def query_sensor_data_sql(sql_query: str):
    """Executa consulta SQL no InfluxDB v3"""
    if not app_state.influx_is_connected or _client is None:
        logger.warning("InfluxDB v3 unavailable, cannot execute query.")
        return None
    
    try:
        # InfluxDB v3 suporta consultas SQL nativas!
        result = _client.query(sql=sql_query)
        logger.info(f"SQL query executed successfully: {sql_query[:100]}...")
        return result
        
    except Exception as e:
        logger.error(f"SQL query failed: {e}")
        return None

def close_influx_connection():
    """Close InfluxDB connection."""
    global _client
    
    if _client:
        _client.close()
        app_state.influx_is_connected = False
        _client = None
        logger.info("InfluxDB v3 connection closed")