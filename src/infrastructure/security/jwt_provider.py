import jwt
from typing import Dict, Any
from datetime import datetime, timezone, timedelta
from src.infrastructure.security.security_settings import get_security_settings


class JWTProviderImpl:
    def __init__(self):
        self.settings = get_security_settings()
    
    def generate_token(
        self,
        device_id: str,
        additional_claims: Dict[str, Any] | None = None
    ) -> str:
        if not device_id or not device_id.strip():
            raise ValueError("device_id cannot be empty")
        
        now = datetime.now(timezone.utc)
        payload = {
            "sub": device_id,
            "device_id": device_id,
            "iat": now,
            "scope": "sensor:write"
        }
        
        if self.settings.JWT_EXPIRATION_HOURS > 0:
            payload["exp"] = now + timedelta(
                hours=self.settings.JWT_EXPIRATION_HOURS
            )
        
        if additional_claims:
            payload.update(additional_claims)
        
        token = jwt.encode(
            payload,
            self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_ALGORITHM
        )
        return token
    
    def validate_token(self, token: str) -> bool:
        try:
            jwt.decode(
                token,
                self.settings.JWT_SECRET_KEY,
                algorithms=[self.settings.JWT_ALGORITHM]
            )
            return True
        except jwt.InvalidTokenError:
            return False
    
    def decode_token(self, token: str) -> Dict[str, Any]:
        try:
            decoded = jwt.decode(
                token,
                self.settings.JWT_SECRET_KEY,
                algorithms=[self.settings.JWT_ALGORITHM]
            )
            return decoded
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Invalid token: {str(e)}")
    
    def get_device_id_from_token(self, token: str) -> str:
        try:
            decoded = self.decode_token(token)
            device_id = decoded.get("device_id")
            if not device_id:
                raise ValueError("device_id not found in token")
            return device_id
        except Exception as e:
            raise ValueError(f"Failed to extract device_id: {str(e)}")
