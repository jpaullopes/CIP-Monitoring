from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.lifecycle import on_startup, on_shutdown
from src.api.routers import api_router
from src.api.middleware.payload_middleware import PayloadSizeMiddleware
from src.infrastructure.security.security_settings import get_security_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await on_startup()
    yield
    await on_shutdown()


settings = get_security_settings()

app = FastAPI(
    title="CIP data collect API", 
    version="3.5",
    lifespan=lifespan
)

app.add_middleware(PayloadSizeMiddleware)
app.include_router(api_router)
