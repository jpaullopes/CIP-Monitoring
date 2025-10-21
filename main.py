import uvicorn
import os

if __name__ == "__main__":
    # Em produção (Docker), reload=False para melhor performance e segurança
    reload = os.getenv("ENVIRONMENT", "production") == "development"
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=reload)