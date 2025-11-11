from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

# Importamos el servicio
from services.turno_service import TurnoService

# Creamos un "enrutador" específico para turnos
router = APIRouter(
    prefix="/turnos",  # Todos los endpoints aquí empezarán con /api/turnos
    tags=["Turnos y Reservas"]  # Etiqueta para la documentación de FastAPI
)

# ----- Definimos los "Request Body" (Validadores de JSON) -----

# Body para el CU-1: Registrar Reserva
class ReservaRequest(BaseModel):
    id_cliente: int
    id_usuario_registro: int  # El admin que la registra


# Response model para Turno
class TurnoResponse(BaseModel):
    id: Optional[int]
    id_cancha: int
    fecha_hora_inicio: str
    fecha_hora_fin: str
    estado: str
    precio_final: float
    id_cliente: Optional[int]
    id_usuario_registro: Optional[int]
    reserva_created_at: Optional[str]
    id_usuario_bloqueo: Optional[int]
    motivo_bloqueo: Optional[str]
    
    class Config:
        from_attributes = True


# ========================================================
# CU-1: REGISTRAR RESERVA (sobre un turno existente)
# ========================================================
@router.post("/{turno_id}/reservar", response_model=TurnoResponse, status_code=200)
def endpoint_registrar_reserva(
    turno_id: int, 
    request: ReservaRequest
):
    """
    Toma un Turno 'disponible' y lo pasa a 'reservado',
    asignándole un cliente.
    """
    try:
        turno_actualizado = TurnoService.registrar_reserva(
            turno_id=turno_id,
            id_cliente=request.id_cliente,
            id_usuario_registro=request.id_usuario_registro
        )
        # Convertir el dataclass a dict para la respuesta
        return turno_actualizado.to_dict()
    except ValueError as ve:
        # Error de negocio (ej. "Turno no disponible", "Cliente no existe")
        raise HTTPException(status_code=409, detail=str(ve))  # 409 Conflict
    except LookupError as le:
        # Error: No encontrado (ej. "Turno no existe")
        raise HTTPException(status_code=404, detail=str(le))
    except Exception as e:
        # Otro error (ej. DB)
        print(f"Error interno: {e}") 
        raise HTTPException(status_code=500, detail="Error interno del servidor.")