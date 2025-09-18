from fastapi import FastAPI
from app.lifecycle import on_startup, on_shutdown
from src.api.routers import api_router
from src.api.routers.websocket import router as ws_router

app = FastAPI(title="Resilient Sensor API - InfluxDB Edition", version="2.1.0")

@app.on_event("startup")
async def startup_event():
    await on_startup()

@app.on_event("shutdown")
async def shutdown_event():
    await on_shutdown()

app.include_router(api_router)
app.include_router(ws_router, prefix="/ws")
