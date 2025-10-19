# routers/clientes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas  # Usamos rutas relativas si es necesario
from databases.sqlconect import SessionLocal
from repository.clientes import create as crud_create, list_all as crud_list_all, get_by_dni as crud_get_by_dni, delete_by_dni as crud_delete_by_dni, update_contact as crud_update_cliente

# 1. Crea una instancia de APIRouter
router = APIRouter(
    prefix="/clientes",  # Todas las rutas aquí empezarán con /clientes
    tags=["Clientes"]    # Las agrupa en la documentación bajo "Clientes"
)

# --- Dependencia para obtener la sesión de la BD ---
# (Puedes moverla a un archivo crud.py o dejarla aquí si solo la usas para clientes)
def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

# 2. Define tus endpoints usando '@router'
@router.post("/", response_model=schemas.Cliente)
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    try:
        return crud_create(db, cliente)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[schemas.Cliente])
def read_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):  # el skip y limit son para paginación simple
    return crud_list_all(db, skip=skip, limit=limit)

@router.get("/{dni}", response_model=schemas.Cliente)
def read_cliente(dni: int, db: Session = Depends(get_db)):
    db_cliente = crud_get_by_dni(db, dni)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

@router.delete("/{dni}")
def delete_cliente(dni: int, db: Session = Depends(get_db)):
    db_cliente = crud_get_by_dni(db, dni)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    crud_delete_by_dni(db, dni)
    return {"message": "Cliente eliminado con éxito", "dni": dni}

@router.put("/{dni}", response_model=schemas.Cliente)
def update_cliente(dni: int, cliente: schemas.ClienteUpdate, db: Session = Depends(get_db)):
    db_cliente = crud_get_by_dni(db, dni)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    try:
        # Pasamos los datos del esquema Pydantic al CRUD
        return crud_update_cliente(db, dni, **cliente.model_dump(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))