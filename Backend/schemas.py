from pydantic import BaseModel
from datetime import date, time

# pydantic es una librería para validación de datos y creación de esquemas
# Validar automáticamente los datos que llegan en los requests (JSON).
# Definir qué estructura tendrán las respuestas.
# Generar documentación automática (Swagger/OpenAPI).
# Convertir entre diferentes formatos (JSON ↔ objetos Python ↔ objetos SQLAlchemy).

# =================================================================
#                         ESQUEMAS PARA CLIENTE
# =================================================================

class ClienteBase(BaseModel):
    """Esquema base con los campos comunes para un cliente."""
    Nombre: str
    Apellido: str
    DNI: int
    Telefono: str | None = None
    Email: str | None = None

class ClienteCreate(ClienteBase):
    """Esquema para la creación de un cliente. No incluye fecha de registro ya que se asigna automáticamente."""
    # a pesar de que parezca redundante, es útil tener este esquema separado ya que si despues 
    # queremos añadir más campos que solo se devuelven (como Fecha_Registro), no afectará a este esquema.
    pass

class ClienteUpdate(BaseModel):
    """Para actualizar: todos opcionales, solo se actualizan los campos enviados."""
    Nombre: str | None = None
    Apellido: str | None = None
    Telefono: str | None = None
    Email: str | None = None

class Cliente(ClienteBase):
    """Esquema para leer/devolver un cliente"""

    class Config:
        from_attributes = True # permite leer desde objetos ORM (SQLAlchemy)