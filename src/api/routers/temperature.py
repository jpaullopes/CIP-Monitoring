from fastapi import APIRouter, status, Depends, Request
from datetime import datetime, timedelta, timezone
import pytz

from src.api.schemas.temperature import SensorDataPayload, SensorDataResponse
from src.infrastructure.config.settings import app_state, settings
from src.infrastructure.security.api_key import verify_api_key
from src.infrastructure.websocket.manager import manager
from src.infrastructure.logging.config import get_logger

router = APIRouter()
logger = get_logger(__name__)

# Armazenamento temporário dos dados mais recentes
latest_sensor_data: SensorDataResponse = None

# Controle do CIP ID
current_cip_id: int = 1
last_data_timestamp: datetime = None
CIP_TIMEOUT_MINUTES = 10

@router.post(
    "/sensor_data",
    response_model=SensorDataResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_key)]
)
async def submit_sensor_data(
    payload: SensorDataPayload,
    request: Request
):
    """Endpoint para a placa enviar dados dos sensores"""
    global latest_sensor_data, current_cip_id, last_data_timestamp
    
    utc_now = datetime.now(timezone.utc)
    brasilia_tz = pytz.timezone('America/Sao_Paulo')
    brasilia_now = utc_now.astimezone(brasilia_tz)

    # Lógica para incrementar cip_id baseado no tempo
    if last_data_timestamp is not None:
        time_diff = brasilia_now - last_data_timestamp
        if time_diff > timedelta(minutes=CIP_TIMEOUT_MINUTES):
            current_cip_id += 1
            logger.info(f"CIP ID incrementado para {current_cip_id} - último dado há {time_diff.total_seconds()/60:.1f} minutos")
    
    # Atualiza o timestamp do último dado
    last_data_timestamp = brasilia_now

    logger.info(f"Sensor data received: temp={payload.temperature} press={payload.pressure} conc={payload.concentration} flow={payload.flow} cip_id={current_cip_id}")

    data_to_broadcast = SensorDataResponse(
        temperature=payload.temperature,
        pressure=payload.pressure,
        concentration=payload.concentration,
        flow=payload.flow,
        timestamp=brasilia_now,
        cip_id=current_cip_id
    )

    # Armazena os dados mais recentes em memória
    latest_sensor_data = data_to_broadcast

    await manager.broadcast_json(data_to_broadcast.model_dump())
    return data_to_broadcast

@router.get(
    "/sensor_data",
    response_model=SensorDataResponse,
    status_code=status.HTTP_200_OK
)
async def get_latest_sensor_data():
    """Endpoint para outras aplicações consultarem os dados mais recentes (sem autenticação)"""
    if latest_sensor_data is None:
        # Retorna dados padrão se ainda não há dados disponíveis
        return SensorDataResponse(
            temperature=0.0,
            pressure=0.0,
            concentration=0.0,
            flow=0.0,
            timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')),
            cip_id=current_cip_id
        )
    
    return latest_sensor_data
