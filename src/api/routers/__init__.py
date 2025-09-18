from fastapi import APIRouter
from .temperature import router as temperature_router
from .health import router as health_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(temperature_router, tags=["sensor"])
api_router.include_router(health_router, tags=["health"])
