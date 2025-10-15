# routers/clientes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, models  # Usamos rutas relativas si es necesario
from databases.sqlconect import SessionLocal

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
    # Revisa si el DNI ya existe
    db_cliente_existente = db.query(models.Cliente).filter(models.Cliente.DNI == cliente.DNI).first()
    if db_cliente_existente:
        raise HTTPException(status_code=400, detail="DNI ya registrado")
    
    # Revisar gmail duplicado si se proporciona
    db_cliente_email_existente = db.query(models.Cliente).filter(models.Cliente.Email == cliente.Email).first()
    if cliente.Email and db_cliente_email_existente:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    # Crea el nuevo cliente
    db_cliente = models.Cliente(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    print(db_cliente)
    return db_cliente

@router.get("/", response_model=list[schemas.Cliente])
def read_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clientes = db.query(models.Cliente).offset(skip).limit(limit).all()
    return clientes

@router.get("/{cliente_id}", response_model=schemas.Cliente)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.ID_Cliente == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente