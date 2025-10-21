from datetime import datetime, timedelta, timezone
from typing import Optional
import pytz
from src.infrastructure.logging.config import get_logger

logger = get_logger(__name__)


class CipIdManager:
    """Service responsible for managing CIP ID logic."""
    
    def __init__(self, timeout_minutes: int = 10):
        self._current_cip_id: int = 1
        self._last_data_timestamp: Optional[datetime] = None
        self._timeout_minutes = timeout_minutes
        self._brasilia_tz = pytz.timezone('America/Sao_Paulo')
        self._active: bool = True
    
    def get_current_cip_id(self) -> int:
        """Get the current CIP ID without updating it."""
        return self._current_cip_id
    
    def update_cip_id(self) -> tuple[int, bool]:
        """Update CIP ID based on timeout logic and return the current value and active status."""
        current_time = self._get_brasilia_now()
        
        if self._should_increment_cip_id(current_time):
            self._current_cip_id += 1
            self._active = False  # Mark as inactive when timeout occurs
            time_diff = current_time - self._last_data_timestamp
            logger.info(
                f"CIP ID incrementado para {self._current_cip_id} - "
                f"último dado há {time_diff.total_seconds()/60:.1f} minutos - CIP marked as inactive"
            )
        else:
            self._active = True  # Mark as active when receiving data
        
        self._last_data_timestamp = current_time
        return self._current_cip_id, self._active
    
    def get_active_status(self) -> bool:
        """Get the current active status."""
        return self._active
    
    def check_active_status(self) -> bool:
        """Check if CIP should be active based on timeout, without updating CIP ID."""
        if self._last_data_timestamp is None:
            return True 
        
        current_time = self._get_brasilia_now()
        time_diff = current_time - self._last_data_timestamp
        if time_diff > timedelta(minutes=self._timeout_minutes):
            self._active = False
        else:
            self._active = True
            
        return self._active
    
    def restore_state(self, cip_id: int, active: bool, last_update: str) -> None:
        """Restore CIP state from persistent storage."""
        self._current_cip_id = cip_id
        self._active = active
        # Parse the timestamp and set as last data timestamp
        try:
            self._last_data_timestamp = datetime.fromisoformat(last_update.replace('Z', '+00:00'))
            logger.info(f"CIP state restored: cip_id={cip_id}, active={active}")
        except ValueError:
            logger.warning(f"Could not parse timestamp: {last_update}")
            self._last_data_timestamp = self._get_brasilia_now()
    
    def _should_increment_cip_id(self, current_time: datetime) -> bool:
        """Check if CIP ID should be incremented based on timeout."""
        if self._last_data_timestamp is None:
            return False
        
        time_diff = current_time - self._last_data_timestamp
        return time_diff > timedelta(minutes=self._timeout_minutes)
    
    def _get_brasilia_now(self) -> datetime:
        """Get current time in Brasilia timezone."""
        utc_now = datetime.now(timezone.utc)
        return utc_now.astimezone(self._brasilia_tz)