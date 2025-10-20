from src.infrastructure.security.payload_validator_protocol import PayloadSizeValidator
from src.infrastructure.security.security_settings import get_security_settings
from typing import Dict, Any


class PayloadValidatorImpl:
    def __init__(self):
        self.settings = get_security_settings()
    
    def validate_request_size(self, body_size_bytes: int) -> bool:
        return body_size_bytes <= self.settings.MAX_REQUEST_BODY_SIZE
    
    def validate_field_size(self, field_name: str, field_size_bytes: int) -> bool:
        return field_size_bytes <= self.settings.MAX_FIELD_SIZE
    
    def get_max_request_size(self) -> int:
        return self.settings.MAX_REQUEST_BODY_SIZE
    
    def get_max_field_size(self) -> int:
        return self.settings.MAX_FIELD_SIZE
    
    def get_validation_config(self) -> Dict[str, Any]:
        return {
            "max_request_size_bytes": self.settings.MAX_REQUEST_BODY_SIZE,
            "max_field_size_bytes": self.settings.MAX_FIELD_SIZE,
            "max_request_size_mb": self.settings.MAX_REQUEST_BODY_SIZE / (1024 * 1024),
            "max_field_size_kb": self.settings.MAX_FIELD_SIZE / 1024,
        }
