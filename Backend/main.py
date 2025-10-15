from fastapi import FastAPI
from routes import clientes  

app = FastAPI(
    title="API de Clientes",
    description="API para gestión de clientes",
    version="1.0.0"
)

# Incluye el router de clientes
app.include_router(clientes.router)

# Opcional: endpoint raíz
@app.get("/")
def read_root():
    return {"msg": "API funcionando"}

