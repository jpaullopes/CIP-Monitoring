from datetime import datetime
import pytz
from src.api.schemas.temperature import SensorDataPayload, SensorDataResponse
from src.core.protocols import SensorDataRepository, CipIdService, PersistenceService
from src.infrastructure.logging.config import get_logger

logger = get_logger(__name__)


class SensorDataService:
    """Service for handling sensor data operations."""
    
    def __init__(
        self,
        repository: SensorDataRepository,
        cip_service: CipIdService,
        persistence_service: PersistenceService
    ):
        self._repository = repository
        self._cip_service = cip_service
        self._persistence_service = persistence_service
        self._brasilia_tz = pytz.timezone('America/Sao_Paulo')
    
    async def process_sensor_data(self, payload: SensorDataPayload) -> SensorDataResponse:
        """Process incoming sensor data and return response."""
        logger.info(
            f"Sensor data received: temp={payload.temperature} "
            f"cond={payload.conductivity} flow={payload.flow}"
        )
        
        # Update CIP ID and get active status based on timeout logic
        current_cip_id, is_active = self._cip_service.update_cip_id()
        
        # Create response with current timestamp and active status
        response = self._create_response(payload, current_cip_id, is_active)
        
        # Save to repository
        await self._repository.save_latest(response)
        
        # Save state to persistent storage (antifail)
        await self._persistence_service.save_state(
            cip_id=current_cip_id,
            active=is_active,
            timestamp=response.timestamp.isoformat()
        )
        
        
        return response
    
    async def get_latest_sensor_data(self) -> SensorDataResponse:
        """Get the latest sensor data or default values."""
        # Check timeout and update status WITHOUT incrementing CIP ID
        is_active = self._cip_service.check_active_status()
        current_cip_id = self._cip_service.get_current_cip_id()
        
        # Save updated state if status changed
        await self._persistence_service.save_state(
            cip_id=current_cip_id,
            active=is_active,
            timestamp=datetime.now(self._brasilia_tz).isoformat()
        )
        
        latest_data = await self._repository.get_latest()
        
        if latest_data is not None:
            # Update the active status in the latest data
            latest_data.active = is_active
            latest_data.cip_id = current_cip_id
            return latest_data
        
        # Return default data if no data available
        return self._create_default_response()
    
    def _create_response(self, payload: SensorDataPayload, cip_id: int, active: bool) -> SensorDataResponse:
        """Create a sensor data response from payload."""
        brasilia_now = datetime.now(self._brasilia_tz)
        
        return SensorDataResponse(
            temperature=payload.temperature,
            conductivity=payload.conductivity,
            flow=payload.flow,
            timestamp=brasilia_now,
            cip_id=cip_id,
            active=active
        )
    
    def _create_default_response(self) -> SensorDataResponse:
        """Create a default sensor data response."""
        brasilia_now = datetime.now(self._brasilia_tz)
        # Check timeout and update status WITHOUT incrementing CIP ID
        is_active = self._cip_service.check_active_status()
        current_cip_id = self._cip_service.get_current_cip_id()
        
        return SensorDataResponse(
            temperature=0.0,
            conductivity=0.0,
            flow=0.0,
            timestamp=brasilia_now,
            cip_id=current_cip_id,
            active=is_active
        )
    
    async def initialize_from_persistence(self) -> None:
        """Initialize service from persistent storage on startup."""
        saved_state = await self._persistence_service.load_state()
        
        if saved_state:
            logger.info(f"Restoring CIP state from persistence: {saved_state}")
            self._cip_service.restore_state(
                cip_id=saved_state["cip_id"],
                active=saved_state["active"],
                last_update=saved_state["last_update"]
            )