# routes/api_routes.py
from fastapi import APIRouter, status, Depends, Request
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import pytz

from ..models import TemperatureReadingPayload, TemperatureDataResponse, DataDB
from ..database import get_db
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
    request: Request,
    db: Optional[Session] = Depends(get_db)
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

    db_data_entry = None

    # Save to database if connected
    if app_state.db_is_connected and db:
        try:
            db_data_entry = DataDB(
                temperature=payload.temperature,
                humidity=payload.humidity,
                pressure=payload.pressure,
                date_recorded=date_to_store,
                time_recorded=time_to_store,
                sensor_id=sensor_id,
                client_ip=client_ip
            )
            db.add(db_data_entry)
            db.commit()
            db.refresh(db_data_entry)
            logger.info(f"HTTP: Data from {sensor_id} saved to database. ID: {db_data_entry.id}")

        except Exception as e:
            if db: 
                db.rollback()
            app_state.db_is_connected = False
            logger.error("REAL-TIME ERROR: Database connection lost. Data not saved.")
            logger.error(f"Error detail: {e}")
            db_data_entry = None
    else:
        logger.warning(f"WARNING: Database unavailable. Data from {sensor_id} will not be saved.")

    # Create response data
    data_to_broadcast = TemperatureDataResponse(
        id=db_data_entry.id if db_data_entry else None,
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
