from typing import Protocol, Dict, Any


class JWTProvider(Protocol):
    def generate_token(self, device_id: str, additional_claims: Dict[str, Any] | None = None) -> str:
        ...
    
    def validate_token(self, token: str) -> bool:
        ...
    
    def decode_token(self, token: str) -> Dict[str, Any]:
        ...
    
    def get_device_id_from_token(self, token: str) -> str:
        ...
