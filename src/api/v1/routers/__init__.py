from fastapi import APIRouter
from .temperature import router as temperature_router
from .websocket import router as websocket_router
from .health import router as health_router
from .query import router as query_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(temperature_router, tags=["temperature"])
api_v1_router.include_router(health_router, tags=["health"])
api_v1_router.include_router(query_router, tags=["query"], prefix="/query")
