from fastapi import APIRouter, status, Request

from src.api.schemas.temperature import SensorDataPayload, SensorDataResponse
from src.infrastructure.logging.config import get_logger
from src.core.dependencies import service_factory

router = APIRouter()
logger = get_logger(__name__)

@router.post(
    "/sensor_data",
    response_model=SensorDataResponse,
    status_code=status.HTTP_201_CREATED,
)
async def submit_sensor_data(
    payload: SensorDataPayload,
    request: Request
):
    """Endpoint para a placa enviar dados dos sensores"""
    print(payload.model_dump_json(indent=4))
    
    sensor_service = service_factory.get_sensor_service()
    return await sensor_service.process_sensor_data(payload)

@router.get(
    "/sensor_data",
    response_model=SensorDataResponse,
    status_code=status.HTTP_200_OK
)
async def get_latest_sensor_data():
    """Endpoint para outras aplicações consultarem os dados mais recentes (sem autenticação)"""
    sensor_service = service_factory.get_sensor_service()
    return await sensor_service.get_latest_sensor_data()
