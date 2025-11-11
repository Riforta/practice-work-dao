import uvicorn
from fastapi import FastAPI

# Importamos el nuevo enrutador de turnos
from routes.turno_routes import router as turno_router
# (Aquí importarías otros enrutadores, ej: routes.cliente_routes)

app = FastAPI(
    title="API de Gestión de Canchas",
    version="1.0.0"
)

# ===== Incluir Rutas =====

# Le decimos a la app principal que use las rutas de turno_routes
# Todo lo definido en turno_routes ahora estará bajo el prefijo /api
app.include_router(turno_router, prefix="/api")

# (Aquí incluirías otros routers)
# app.include_router(cliente_router, prefix="/api")


@app.get("/", tags=["Root"])
def read_root():
    return {"mensaje": "Bienvenido a la API de Gestión de Canchas"}

# Línea final para ejecutar la app
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)