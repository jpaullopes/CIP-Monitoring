from fastapi import Header, HTTPException, status
from src.infrastructure.config.settings import settings

async def verify_api_key(x_api_key: str = Header(...)):
    if not settings.API_KEY or x_api_key != settings.API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")

async def verify_ws_api_key(api_key: str):
    if not settings.API_KEY_WS or api_key != settings.API_KEY_WS:
        return False
    return True
