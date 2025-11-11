from fastapi import FastAPI

from api.routers import clientes

app = FastAPI(title="TP-DAO API (minimal)")

app.include_router(clientes.router, prefix="/clientes", tags=["clientes"])

@app.get("/health")
def health():
    return {"status": "ok"}
