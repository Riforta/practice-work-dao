"""Schemas Pydantic para canchas."""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


# ===== Request Schemas =====

class CanchaCreateRequest(BaseModel):
    """Schema para crear una cancha."""
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre de la cancha")
    tipo_deporte: Optional[str] = Field(None, max_length=50, description="Tipo de deporte")
    descripcion: Optional[str] = Field(None, max_length=500, description="Descripción de la cancha")
    activa: Optional[int] = Field(default=1, description="Estado de la cancha (1=activa, 0=inactiva)")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": "Cancha 1",
                "tipo_deporte": "Fútbol 5",
                "descripcion": "Cancha de pasto sintético con iluminación",
                "activa": 1
            }
        }
    )


class CanchaUpdateRequest(BaseModel):
    """Schema para actualizar una cancha."""
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    tipo_deporte: Optional[str] = Field(None, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=500)
    activa: Optional[int] = None


# ===== Response Schemas =====

class CanchaResponse(BaseModel):
    """Schema para respuesta de cancha."""
    id: int
    nombre: str
    tipo_deporte: Optional[str] = None
    descripcion: Optional[str] = None
    activa: int
    
    model_config = ConfigDict(from_attributes=True)
