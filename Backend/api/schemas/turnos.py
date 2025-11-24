"""Schemas Pydantic para turnos y reservas."""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


# ===== Request Schemas =====

class TurnoCreateRequest(BaseModel):
    """Schema para crear un turno."""
    id_cancha: int = Field(..., gt=0, description="ID de la cancha")
    fecha_hora_inicio: str = Field(..., description="Fecha y hora de inicio (formato: YYYY-MM-DD HH:MM:SS)")
    fecha_hora_fin: str = Field(..., description="Fecha y hora de fin (formato: YYYY-MM-DD HH:MM:SS)")
    precio_final: float = Field(default=0.0, ge=0, description="Precio del turno")
    estado: Optional[str] = Field(default="disponible", description="Estado del turno")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id_cancha": 1,
                "fecha_hora_inicio": "2025-01-15 10:00:00",
                "fecha_hora_fin": "2025-01-15 11:00:00",
                "precio_final": 5000.0,
                "estado": "disponible"
            }
        }
    )


class TurnoUpdateRequest(BaseModel):
    """Schema para actualizar un turno."""
    id_cancha: Optional[int] = Field(None, gt=0)
    fecha_hora_inicio: Optional[str] = None
    fecha_hora_fin: Optional[str] = None
    precio_final: Optional[float] = Field(None, ge=0)
    estado: Optional[str] = None
    id_cliente: Optional[int] = None
    id_usuario_bloqueo: Optional[int] = None
    motivo_bloqueo: Optional[str] = None


class ReservaRequest(BaseModel):
    """Schema para registrar una reserva."""
    id_cliente: int = Field(..., gt=0, description="ID del cliente que reserva")
    id_usuario_registro: int = Field(..., gt=0, description="ID del usuario que registra la reserva")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id_cliente": 5,
                "id_usuario_registro": 1
            }
        }
    )


class ReservaModificarRequest(BaseModel):
    """Schema para modificar una reserva."""
    id_cliente: Optional[int] = Field(None, gt=0, description="Nuevo ID de cliente")
    precio_final: Optional[float] = Field(None, ge=0, description="Nuevo precio")
    id_usuario_mod: int = Field(..., gt=0, description="ID del usuario que modifica")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id_cliente": 5,
                "precio_final": 6000.0,
                "id_usuario_mod": 1
            }
        }
    )


class ReservaCancelarRequest(BaseModel):
    """Schema para cancelar una reserva."""
    id_usuario_cancelacion: int = Field(..., gt=0, description="ID del usuario que cancela")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id_usuario_cancelacion": 1
            }
        }
    )


# ===== Response Schemas =====

class TurnoResponse(BaseModel):
    """Schema para respuesta de turno."""
    id: int
    id_cancha: int
    fecha_hora_inicio: str
    fecha_hora_fin: str
    estado: str
    precio_final: float
    id_cliente: Optional[int] = None
    id_usuario_registro: Optional[int] = None
    reserva_created_at: Optional[str] = None
    id_usuario_bloqueo: Optional[int] = None
    motivo_bloqueo: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
