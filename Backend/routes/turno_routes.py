from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

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
    
    # Migración a estilo Pydantic v2
    model_config = {
        'from_attributes': True
    }

# Body para el CU-3: Modificar Reserva
# Todos los campos son opcionales para un PATCH
class ReservaModificarRequest(BaseModel):
    id_cliente: Optional[int] = None
    precio_final: Optional[float] = None
    # ID del admin que está realizando la modificación
    id_usuario_mod: int

# Body para el CU-4: Cancelar Reserva
class ReservaCancelarRequest(BaseModel):
    id_usuario_cancelacion: int # ID del admin que cancela

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
    
    # ========================================================
# CU-2a: CONSULTAR UN TURNO POR ID
# ========================================================
@router.get("/{turno_id}", response_model=TurnoResponse)
def endpoint_consultar_turno(turno_id: int, id_cliente: Optional[int] = Query(None, description="Opcional: validar que la reserva pertenezca a este cliente")):
    """
    Obtiene el detalle de un turno (reserva) específico por su ID.
    Si se informa id_cliente, la validación de pertenencia se realiza en el servicio
    (permite centralizar la regla de negocio y reutilizar en otros contextos).
    """
    try:
        turno = TurnoService.consultar_turno_por_id(turno_id, id_cliente=id_cliente)
        return turno.to_dict()
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))
    except LookupError as le:
        raise HTTPException(status_code=404, detail=str(le))
    except Exception as e:
        print(f"Error interno: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor.")


# ========================================================
# CU-2b/2c: LISTAR TODOS LOS TURNOS (CON FILTROS)
# ========================================================
@router.get("/", response_model=List[TurnoResponse])
def endpoint_listar_turnos_cliente(
    id_cliente: int = Query(..., description="ID del cliente cuyas reservas se consultan (obligatorio)"),
    id_cancha: Optional[int] = Query(None, description="Filtrar además por ID de cancha"),
    estado: Optional[str] = Query(None, description="Filtrar por estado opcional (reservado, disponible, etc.)")
):
    """Lista reservas asociadas a un cliente.
    La regla de negocio (cliente debe existir, estado válido) se ejecuta en el servicio.
    """
    try:
        turnos = TurnoService.listar_reservas_cliente(
            id_cliente=id_cliente,
            id_cancha=id_cancha,
            estado=estado
        )
        return [t.to_dict() for t in turnos]
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        print(f"Error interno: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor.")
    
# ========================================================
# CU-3: MODIFICAR UNA RESERVA (PATCH)
# ========================================================
@router.patch("/{turno_id}", response_model=TurnoResponse)
def endpoint_modificar_reserva(
    turno_id: int, 
    request: ReservaModificarRequest
):
    """
    Modifica datos de una reserva existente (ej: cambiar el cliente).
    Solo aplica a turnos que estén 'reservado'.
    """
    try:
        # Convertimos el modelo Pydantic a un diccionario,
        # excluyendo los campos que no se enviaron (exclude_unset=True)
        # y el id_usuario_mod que se pasa por separado.
        nuevos_datos = request.model_dump(exclude_unset=True, exclude={'id_usuario_mod'})

        # Validaciones previas simples
        if not nuevos_datos:
            # Forzamos que al menos un campo modificable venga en el body
            raise HTTPException(status_code=400, detail="Debe enviar al menos un campo modificable (id_cliente o precio_final).")

        if "precio_final" in nuevos_datos and nuevos_datos["precio_final"] is not None:
            try:
                # Convertimos a float por si viene como int
                precio_val = float(nuevos_datos["precio_final"])
            except (TypeError, ValueError):
                raise HTTPException(status_code=400, detail="precio_final debe ser un número válido.")
            if precio_val < 0:
                raise HTTPException(status_code=400, detail="precio_final debe ser >= 0.")
            nuevos_datos["precio_final"] = precio_val

        turno_actualizado = TurnoService.modificar_reserva(
            turno_id=turno_id,
            nuevos_datos=nuevos_datos,
            id_usuario_mod=request.id_usuario_mod
        )
        # Respuesta consistente con otros endpoints
        return turno_actualizado.to_dict()
    except HTTPException as he:
        # Propagar directamente las validaciones propias sin convertirlas en 500
        raise he
    except ValueError as ve:
        # Error de negocio (ej. "No se puede modificar", "Cliente no existe")
        raise HTTPException(status_code=400, detail=str(ve)) # 400 Bad Request
    except LookupError as le:
        # Error: No encontrado (ej. "Turno no existe")
        raise HTTPException(status_code=404, detail=str(le))
    except Exception as e:
        # Otro error (ej. DB)
        print(f"Error interno: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor.")
    
# ========================================================
# CU-4: CANCELAR UNA RESERVA (Reset a 'disponible')
# ========================================================
@router.post("/{turno_id}/cancelar", response_model=TurnoResponse)
def endpoint_cancelar_reserva(
    turno_id: int, 
    request: ReservaCancelarRequest
):
    """
    Cancela una reserva activa (un turno 'reservado') y
    lo revierte a 'disponible'.
    """
    try:
        turno_actualizado = TurnoService.cancelar_reserva(
            turno_id=turno_id,
            id_usuario_cancelacion=request.id_usuario_cancelacion
        )
        # Alineamos el formato de respuesta con otros endpoints
        return turno_actualizado.to_dict()
    except ValueError as ve:
        # Error de negocio (ej. "No se puede cancelar", "Usuario no existe")
        raise HTTPException(status_code=400, detail=str(ve)) # 400 Bad Request
    except LookupError as le:
        # Error: No encontrado (ej. "Turno no existe")
        raise HTTPException(status_code=404, detail=str(le))
    except Exception as e:
        # Otro error (ej. DB)
        print(f"Error interno: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor.")