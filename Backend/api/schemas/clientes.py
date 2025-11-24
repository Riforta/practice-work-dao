"""Schemas Pydantic para clientes."""

from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional


# ===== Request Schemas =====

class ClienteCreateRequest(BaseModel):
    """Schema para crear un cliente."""
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del cliente")
    apellido: Optional[str] = Field(None, max_length=100, description="Apellido del cliente")
    dni: Optional[str] = Field(None, max_length=20, description="DNI del cliente")
    telefono: str = Field(..., min_length=1, max_length=20, description="Teléfono del cliente")
    email: Optional[EmailStr] = Field(None, description="Email del cliente")
    id_usuario: Optional[int] = Field(None, description="ID del usuario asociado al cliente")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": "Juan",
                "apellido": "Pérez",
                "dni": "12345678",
                "telefono": "3512345678",
                "email": "juan.perez@example.com",
                "id_usuario": None
            }
        }
    )


class ClienteUpdateRequest(BaseModel):
    """Schema para actualizar un cliente."""
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    apellido: Optional[str] = Field(None, max_length=100)
    dni: Optional[str] = Field(None, max_length=20)
    telefono: Optional[str] = Field(None, min_length=1, max_length=20)
    email: Optional[EmailStr] = None
    id_usuario: Optional[int] = None


# ===== Response Schemas =====

class ClienteResponse(BaseModel):
    """Schema para respuesta de cliente."""
    id: int
    nombre: str
    apellido: Optional[str] = None
    dni: Optional[str] = None
    telefono: str
    email: Optional[str] = None
    id_usuario: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)
