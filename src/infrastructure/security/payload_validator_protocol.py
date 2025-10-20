from typing import Protocol


class PayloadSizeValidator(Protocol):
    def validate_request_size(self, body_size_bytes: int) -> bool:
        ...
    
    def validate_field_size(self, field_name: str, field_size_bytes: int) -> bool:
        ...
    
    def get_max_request_size(self) -> int:
        ...
    
    def get_max_field_size(self) -> int:
        ...
    
    def get_validation_config(self) -> dict:
        ...
