from fastapi import APIRouter, status, Depends, Request
from datetime import datetime
import pytz
import uuid

from src.api.v1.schemas.temperature import TemperatureReadingPayload, CipDataResponse
from src.infrastructure.influx.client import write_cip_data
from src.infrastructure.config.settings import app_state, settings
from src.infrastructure.security.api_key import verify_api_key
from src.infrastructure.websocket.manager import manager
from src.infrastructure.logging.config import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.post(
    "/temperature_reading",
    response_model=CipDataResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_key)]
)
async def submit_temperature_reading_http(
    payload: TemperatureReadingPayload,
    request: Request
):
    client_ip = request.client.host if request.client else "unknown_ip"
    id_sensor = payload.id_sensor

    utc_now = datetime.utcnow()
    brasilia_tz = pytz.timezone('America/Sao_Paulo')
    brasilia_now = utc_now.astimezone(brasilia_tz)
    date_to_store = brasilia_now.date()
    time_to_store = brasilia_now.time().replace(microsecond=0)

    logger.info(f"HTTP CIP: sensor={id_sensor} cip_id={payload.cip_id} temp={payload.temperature} press={payload.pressure} conc={payload.concentration}")

    record_id = None
    if app_state.influx_is_connected:
        ok = write_cip_data(
            temperature=payload.temperature,
            pressure=payload.pressure,
            concentration=payload.concentration,
            id_sensor=id_sensor,
            cip_id=payload.cip_id,
            status_cip=payload.status_cip,
            client_ip=client_ip
        )
        if ok:
            record_id = str(uuid.uuid4())

    data_to_broadcast = CipDataResponse(
        id=record_id,
        temperature=payload.temperature,
        pressure=payload.pressure,
        concentration=payload.concentration,
        date_recorded=date_to_store,
        time_recorded=time_to_store,
        id_sensor=id_sensor,
        cip_id=payload.cip_id,
        status_cip=payload.status_cip,
        client_ip=client_ip
    )

    await manager.broadcast_json(data_to_broadcast.model_dump())
    return data_to_broadcast
