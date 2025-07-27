# routes/__init__.py
from .api_routes import router as api_router
from .websocket_routes import router as websocket_router

__all__ = ["api_router", "websocket_router"]
