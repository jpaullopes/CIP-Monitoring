from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.lifecycle import on_startup, on_shutdown
from src.api.routers import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await on_startup()
    yield
    # Shutdown
    await on_shutdown()


app = FastAPI(
    title="CIP data collect API", 
    version="3.5",
    lifespan=lifespan
)

app.include_router(api_router)
