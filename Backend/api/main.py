from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import (
    clientes,
    canchas,
    equipos,
    equipo_miembros,
    partidos,
    pedidos,
    pagos,
    inscripciones,
    servicios_adicionales,
    tarifas,
    torneos,
    roles,
    usuarios,
    turnos,
)


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

# Routers: the individual router modules already define their own path prefixes
app.include_router(clientes.router)
app.include_router(canchas.router)
app.include_router(equipos.router)
app.include_router(equipo_miembros.router)
app.include_router(partidos.router)
app.include_router(pedidos.router)
app.include_router(pagos.router)
app.include_router(inscripciones.router)
app.include_router(servicios_adicionales.router)
app.include_router(tarifas.router)
app.include_router(torneos.router)
app.include_router(roles.router)
app.include_router(usuarios.router)
app.include_router(turnos.router)

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
