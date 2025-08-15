# routes/api_routes.py
from fastapi import APIRouter, status, Depends, Request
from typing import Optional
from datetime import datetime
import pytz
import uuid

from ..models import TemperatureReadingPayload, TemperatureDataResponse
from ..database import write_sensor_data
from ..auth import verify_api_key
from ..config import app_state
from ..websocket_manager import manager
from ..logger_config import setup_logger

router = APIRouter()
logger = setup_logger(__name__)

# --- HTTP Endpoint to receive data ---
@router.post(
    "/api/temperature_reading",
    response_model=TemperatureDataResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_key)]
)
async def submit_temperature_reading_http(
    payload: TemperatureReadingPayload,
    request: Request
):
    """Submit temperature reading via HTTP."""
    client_ip = request.client.host if request.client else "unknown_ip"
    sensor_id = payload.sensor_id

    logger.info(f"HTTP: AUTHENTICATED request from {client_ip} (sensor: {sensor_id})")

    # Get current time in Brazil timezone
    utc_now = datetime.now(pytz.utc)
    brasilia_tz = pytz.timezone('America/Sao_Paulo')
    brasilia_now = utc_now.astimezone(brasilia_tz)
    date_to_store = brasilia_now.date()
    time_to_store = brasilia_now.time().replace(microsecond=0)

    # Log received data
    logger.info(
        f"HTTP: Dados recebidos de {sensor_id}: "
        f"Temp: {payload.temperature}°C, "
        f"Umidade: {payload.humidity}%, "
        f"Pressão: {payload.pressure} hPa"
    )

    data_saved = False
    record_id = None

    # Save to InfluxDB if connected
    if app_state.influx_is_connected:
        try:
            data_saved = write_sensor_data(
                temperature=payload.temperature,
                humidity=payload.humidity,
                pressure=payload.pressure,
                sensor_id=sensor_id,
                client_ip=client_ip
            )
            if data_saved:
                record_id = str(uuid.uuid4())  # Generate unique ID for response
                logger.info(f"HTTP: Data from {sensor_id} saved to InfluxDB. ID: {record_id}")

        except Exception as e:
            logger.error(f"HTTP: Error saving data to InfluxDB: {e}")
            data_saved = False
    else:
        logger.warning(f"WARNING: InfluxDB unavailable. Data from {sensor_id} will not be saved.")

    # Create response data
    data_to_broadcast = TemperatureDataResponse(
        id=record_id,
        temperature=payload.temperature,
        humidity=payload.humidity,
        pressure=payload.pressure,
        date_recorded=date_to_store,
        time_recorded=time_to_store,
        sensor_id=sensor_id,
        client_ip=client_ip
    )

    # Broadcast to WebSocket clients
    await manager.broadcast_json(data_to_broadcast.model_dump(mode='json'))
    logger.info(f"HTTP: Data from {sensor_id} broadcast to {len(manager.active_connections)} WebSocket clients.")

    return data_to_broadcast
