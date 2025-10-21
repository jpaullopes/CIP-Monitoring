from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.lifecycle import on_startup, on_shutdown
from src.api.routers import api_router
from src.api.middleware.payload_middleware import PayloadSizeMiddleware
from src.api.middleware.ip_filter_middleware import IPFilterMiddleware
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

# IPs permitidos 
allowed_ips = [ip.strip() for ip in settings.ALLOWED_POST_IPS.split(",")]

# Middleware de filtro de IP 
app.add_middleware(IPFilterMiddleware, allowed_ips=allowed_ips)

# Middleware CORS para permitir requisições de outros domínios
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(PayloadSizeMiddleware)
app.include_router(api_router)
