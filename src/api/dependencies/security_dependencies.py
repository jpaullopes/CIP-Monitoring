from fastapi import Depends, HTTPException, Header, status
from src.infrastructure.security.jwt_provider import JWTProviderImpl
from src.infrastructure.security.rate_limiter import RateLimiterImpl
from src.infrastructure.logging.secure_logger import SecureLoggerImpl


_jwt_provider = None
_rate_limiter = None
_secure_logger = None


def get_jwt_provider() -> JWTProviderImpl:
    global _jwt_provider
    if _jwt_provider is None:
        _jwt_provider = JWTProviderImpl()
    return _jwt_provider


def get_rate_limiter() -> RateLimiterImpl:
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiterImpl()
    return _rate_limiter


def get_secure_logger() -> SecureLoggerImpl:
    global _secure_logger
    if _secure_logger is None:
        _secure_logger = SecureLoggerImpl()
    return _secure_logger


async def get_current_device_id(
    authorization: str = Header(None),
    jwt_provider: JWTProviderImpl = Depends(get_jwt_provider),
    logger: SecureLoggerImpl = Depends(get_secure_logger),
) -> str:
    if not authorization:
        logger.log_authentication_failure(reason="Missing authorization header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header"
        )
    
    try:
        scheme, token = authorization.split(" ")
        if scheme.lower() != "bearer":
            logger.log_authentication_failure(reason="Invalid authorization scheme")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization scheme"
            )
    except ValueError:
        logger.log_authentication_failure(reason="Invalid authorization format")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization format"
        )
    
    if not jwt_provider.validate_token(token):
        logger.log_authentication_failure(reason="Invalid or expired token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    try:
        device_id = jwt_provider.get_device_id_from_token(token)
        return device_id
    except ValueError as e:
        logger.log_authentication_failure(reason=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token claims"
        )
