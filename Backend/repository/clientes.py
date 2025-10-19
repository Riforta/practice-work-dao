from typing import Optional, List
from sqlalchemy.orm import Session

from models.clientes import Cliente
from schemas import ClienteCreate


def get_by_dni(db: Session, dni: int) -> Optional[Cliente]:
    return db.query(Cliente).filter(Cliente.DNI == dni).first()


def get_by_email(db: Session, email: Optional[str]) -> Optional[Cliente]:
    if not email:
        return None
    return db.query(Cliente).filter(Cliente.Email == email).first()


def list_all(db: Session, skip: int = 0, limit: int = 100) -> List[Cliente]:
    return db.query(Cliente).offset(skip).limit(limit).all()


def create(db: Session, data: ClienteCreate) -> Cliente:
    if get_by_dni(db, data.DNI):
        raise ValueError("DNI ya registrado")
    if data.Email and get_by_email(db, data.Email):
        raise ValueError("Email ya registrado")

    obj = Cliente(**data.model_dump()) # model_dump() convierte pydantic a dict y el ** hace que se pasen de dic a kwargs
    db.add(obj)
    db.commit()
    db.refresh(obj) # en este caso sirve porque SQLite asigna Fecha_Registro automáticamente
    return obj


def update_contact(
    db: Session,
    dni: int,
    *,
    Nombre: Optional[str] = None,
    Apellido: Optional[str] = None,
    Telefono: Optional[str] = None,
    Email: Optional[str] = None,
) -> Optional[Cliente]:
    """Actualiza campos del cliente por DNI (solo los que se pasen).

    - Valida que el nuevo Email no esté asignado a otro cliente.
    - Devuelve el objeto actualizado o None si no existe.
    """
    obj = get_by_dni(db, dni)
    if not obj:
        return None
    
    # Actualizamos solo los campos que se pasaron
    if Nombre is not None:
        obj.Nombre = Nombre
    
    if Apellido is not None:
        obj.Apellido = Apellido

    if Email is not None:
        # Si cambia el email, validar duplicado
        if Email != obj.Email and get_by_email(db, Email):
            raise ValueError("Email ya registrado")
        obj.Email = Email

    if Telefono is not None:
        obj.Telefono = Telefono

    db.commit()
    db.refresh(obj)
    return obj


def delete_by_dni(db: Session, dni: int) -> bool:
    """Elimina un cliente por DNI. Devuelve True si borró, False si no existe."""
    obj = get_by_dni(db, dni)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
