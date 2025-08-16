from fastapi import APIRouter, status, Depends, Request
from datetime import datetime
import pytz
import uuid

from src.api.v1.schemas.temperature import TemperatureReadingPayload, TemperatureDataResponse
from src.infrastructure.influx.client import write_sensor_data
from src.infrastructure.config.settings import app_state, settings
from src.infrastructure.security.api_key import verify_api_key
from src.infrastructure.websocket.manager import manager
from src.infrastructure.logging.config import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.post(
    "/temperature_reading",
    response_model=TemperatureDataResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_key)]
)
async def submit_temperature_reading_http(
    payload: TemperatureReadingPayload,
    request: Request
):
    client_ip = request.client.host if request.client else "unknown_ip"
    sensor_id = payload.sensor_id

    utc_now = datetime.utcnow()
    brasilia_tz = pytz.timezone('America/Sao_Paulo')
    brasilia_now = utc_now.astimezone(brasilia_tz)
    date_to_store = brasilia_now.date()
    time_to_store = brasilia_now.time().replace(microsecond=0)

    logger.info(f"HTTP: sensor={sensor_id} temp={payload.temperature} hum={payload.humidity} press={payload.pressure}")

    record_id = None
    if app_state.influx_is_connected:
        ok = write_sensor_data(
            temperature=payload.temperature,
            humidity=payload.humidity,
            pressure=payload.pressure,
            sensor_id=sensor_id,
            client_ip=client_ip
        )
        if ok:
            record_id = str(uuid.uuid4())

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

    await manager.broadcast_json(data_to_broadcast.model_dump())
    return data_to_broadcast
