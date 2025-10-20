"""
Middleware simples para filtrar IPs permitidos
"""
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class IPFilterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, allowed_ips: list[str]):
        super().__init__(app)
        self.allowed_ips = allowed_ips
    
    def _get_client_ip(self, request: Request) -> str:
        """Extrai o IP do cliente."""
        # Headers de proxy
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip.strip()
        
        # IP direto
        if hasattr(request, "client") and request.client:
            return request.client.host
        
        return "unknown"
    
    async def dispatch(self, request: Request, call_next):
        # Só verificar IPs para métodos POST
        if request.method == "POST":
            client_ip = self._get_client_ip(request)
            
            # Verificar se IP está na lista permitida
            if client_ip not in self.allowed_ips:
                return JSONResponse(
                    status_code=403,
                    content={"detail": f"IP {client_ip} não autorizado para POST"}
                )
        
        response = await call_next(request)
        return response