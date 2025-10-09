import json
import os
from datetime import datetime
from typing import Dict, Any
from pathlib import Path
from src.infrastructure.logging.config import get_logger

logger = get_logger(__name__)


class FilePersistenceService:
    """Service for persisting CIP state to a JSON file."""
    
    def __init__(self, file_path: str = "data/cip_state.json"):
        self.file_path = Path(file_path)
        # Ensure directory exists
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def save_state(self, cip_id: int, active: bool, timestamp: str) -> None:
        """Save CIP state to JSON file."""
        try:
            state = {
                "cip_id": cip_id,
                "active": active,
                "last_update": timestamp
            }
            
            with open(self.file_path, 'w') as f:
                json.dump(state, f, indent=2)
            
            logger.info(f"CIP state saved: cip_id={cip_id}, active={active}")
            
        except Exception as e:
            logger.error(f"Failed to save CIP state: {e}")
    
    async def load_state(self) -> Dict[str, Any] | None:
        """Load CIP state from JSON file."""
        try:
            if not self.file_path.exists():
                logger.info("No CIP state file found, starting fresh")
                return None
            
            with open(self.file_path, 'r') as f:
                state = json.load(f)
            
            logger.info(f"CIP state loaded: {state}")
            return state
            
        except Exception as e:
            logger.error(f"Failed to load CIP state: {e}")
            return None