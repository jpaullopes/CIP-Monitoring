from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.infrastructure.security.payload_validator import PayloadValidatorImpl
from src.infrastructure.logging.secure_logger import SecureLoggerImpl
from src.infrastructure.logging.secure_logger_protocol import LogLevel
import json


class PayloadSizeMiddleware:
    def __init__(self, app, validator: PayloadValidatorImpl = None, logger: SecureLoggerImpl = None):
        self.app = app
        self.validator = validator or PayloadValidatorImpl()
        self.logger = logger or SecureLoggerImpl()
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        request_method = scope.get("method", "").upper()
        if request_method not in ["POST", "PUT", "PATCH"]:
            await self.app(scope, receive, send)
            return
        
        content_length = 0
        for header_name, header_value in scope.get("headers", []):
            if header_name.lower() == b"content-length":
                try:
                    content_length = int(header_value.decode())
                except (ValueError, UnicodeDecodeError):
                    pass
                break
        
        max_size = self.validator.get_max_request_size()
        if content_length > max_size:
            device_id = "unknown"
            for header_name, header_value in scope.get("headers", []):
                if header_name.lower() == b"authorization":
                    try:
                        from src.api.dependencies.security_dependencies import get_jwt_provider
                        jwt_provider = get_jwt_provider()
                        token = header_value.decode().split(" ")[-1]
                        device_id = jwt_provider.get_device_id_from_token(token)
                    except Exception:
                        pass
                    break
            
            self.logger.log_payload_validation_failure(
                device_id=device_id,
                reason="Request body exceeds maximum allowed size",
                size_bytes=content_length,
            )
            
            response_data = {
                "detail": "Request body size exceeds maximum allowed (10 MB)"
            }
            
            await send({
                "type": "http.response.start",
                "status": 413,
                "headers": [
                    [b"content-type", b"application/json"],
                    [b"content-length", str(len(json.dumps(response_data))).encode()],
                ],
            })
            await send({
                "type": "http.response.body",
                "body": json.dumps(response_data).encode(),
            })
            return
        
        await self.app(scope, receive, send)
