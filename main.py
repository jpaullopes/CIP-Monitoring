# main.py
"""LEGACY ENTRYPOINT

Este arquivo foi mantido apenas como referência após a reorganização do projeto.
O novo ponto de entrada da aplicação é: app/main.py (uvicorn app.main:app)

Remova este arquivo se não for mais necessário.
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
