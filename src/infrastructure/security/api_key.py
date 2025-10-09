from fastapi import Header, HTTPException, status
from src.infrastructure.config.settings import get_settings

async def verify_api_key(api_key: str = Header(...)):
    settings = get_settings()
    if not settings.API_KEY or api_key != settings.API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")


