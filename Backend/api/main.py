from fastapi import FastAPI

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
)


app = FastAPI(title="TP-DAO API (minimal)")

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

@app.get("/health")
def health():
    return {"status": "ok"}
