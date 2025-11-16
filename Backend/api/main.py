import sys
from pathlib import Path

# Agregar el directorio Backend al path ANTES de cualquier import relativo
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.routers import register_routers


app = FastAPI(
    title="TP-DAO API - Sistema de Alquiler de Canchas",
    description="API REST para gestión de canchas deportivas, reservas, torneos y pagos",
    version="1.0.0"
)

# Configuración de CORS para permitir conexiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # React dev server alternativo
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Permite todos los headers
)

# Registrar todos los routers (cada uno ya define su propio prefix)
register_routers(app)

@app.get("/")
def root():
    return {
        "message": "TP-DAO API - Sistema de Alquiler de Canchas",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

# Línea final para ejecutar la app
if __name__ == "__main__":
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)