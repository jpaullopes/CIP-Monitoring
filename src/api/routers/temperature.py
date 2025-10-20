import time
from fastapi import APIRouter, status, Depends, HTTPException

from src.api.schemas.temperature import SensorDataPayload, SensorDataResponse
from src.infrastructure.logging.secure_logger import SecureLoggerImpl
from src.infrastructure.logging.secure_logger_protocol import LogLevel, LogContext
from src.infrastructure.security.rate_limiter import RateLimiterImpl
from src.api.dependencies.security_dependencies import (
    get_current_device_id,
    get_secure_logger,
    get_rate_limiter,
)
from src.core.dependencies import service_factory

router = APIRouter()


@router.post(
    "/sensor_data",
    response_model=SensorDataResponse,
    status_code=status.HTTP_201_CREATED,
)
async def submit_sensor_data(
    payload: SensorDataPayload,
    device_id: str = Depends(get_current_device_id),
    logger: SecureLoggerImpl = Depends(get_secure_logger),
    rate_limiter: RateLimiterImpl = Depends(get_rate_limiter),
):
    start_time = time.time()
    
    rate_limit_response = rate_limiter.check_rate_limit(device_id)
    if not rate_limit_response.is_allowed:
        current_requests = rate_limiter.limit_per_window - rate_limit_response.requests_remaining
        logger.log_rate_limit_exceeded(
            device_id=device_id,
            requests_made=current_requests,
            limit=rate_limiter.limit_per_window,
        )
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded",
            headers={"Retry-After": str(rate_limit_response.retry_after_seconds or 60)},
        )
    
    try:
        sensor_service = service_factory.get_sensor_service()
        result = await sensor_service.process_sensor_data(payload)
        
        latency_ms = (time.time() - start_time) * 1000
        logger.log_sensor_data_processed(
            device_id=device_id,
            latency_ms=latency_ms,
        )
        
        return result
    except Exception as e:
        logger.log_request(
            level=LogLevel.ERROR,
            message=str(e),
            context=LogContext(device_id=device_id, status_code=500),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process sensor data",
        )


@router.get(
    "/sensor_data",
    response_model=SensorDataResponse,
    status_code=status.HTTP_200_OK
)
async def get_latest_sensor_data(
    device_id: str = Depends(get_current_device_id),
    logger: SecureLoggerImpl = Depends(get_secure_logger),
):
    start_time = time.time()
    
    try:
        sensor_service = service_factory.get_sensor_service()
        result = await sensor_service.get_latest_sensor_data()
        
        latency_ms = (time.time() - start_time) * 1000
        logger.log_request(
            level=LogLevel.INFO,
            message="Latest sensor data retrieved",
            context=LogContext(
                device_id=device_id,
                endpoint="GET /sensor_data",
                status_code=200,
                latency_ms=latency_ms,
            ),
        )
        
        return result
    except Exception as e:
        logger.log_request(
            level=LogLevel.ERROR,
            message=str(e),
            context=LogContext(device_id=device_id, status_code=500),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve sensor data",
        )
