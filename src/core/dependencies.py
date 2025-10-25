from src.core.services.cip_service import CipIdManager
from src.core.repositories.sensor_repository import InMemorySensorRepository
from src.core.services.sensor_service import SensorDataService
from src.core.services.persistence_service import FilePersistenceService


class ServiceFactory:
    """Factory for creating and configuring application services."""
    
    def __init__(self):
        self._cip_service = None
        self._repository = None
        self._broadcast_service = None
        self._persistence_service = None
        self._sensor_service = None
    
    def get_cip_service(self) -> CipIdManager:
        """Get or create CIP ID service."""
        if self._cip_service is None:
            self._cip_service = CipIdManager(timeout_minutes=15)
        return self._cip_service
    
    def get_sensor_repository(self) -> InMemorySensorRepository:
        """Get or create sensor data repository."""
        if self._repository is None:
            self._repository = InMemorySensorRepository()
        return self._repository

    
    def get_persistence_service(self) -> FilePersistenceService:
        """Get or create persistence service."""
        if self._persistence_service is None:
            self._persistence_service = FilePersistenceService()
        return self._persistence_service
    
    def get_sensor_service(self) -> SensorDataService:
        """Get or create sensor data service with all dependencies."""
        if self._sensor_service is None:
            self._sensor_service = SensorDataService(
                repository=self.get_sensor_repository(),
                cip_service=self.get_cip_service(),
                persistence_service=self.get_persistence_service()
            )
        return self._sensor_service


# Global factory instance
service_factory = ServiceFactory()