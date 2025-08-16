from fastapi import APIRouter
from .temperature import router as temperature_router
from .websocket import router as websocket_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(temperature_router, tags=["temperature"])
