"""Router FastAPI para gestión de Turnos y Reservas."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Dict, Any

from api.dependencies.auth import require_role, require_admin
from models.usuario import Usuario
from services import turnos_service, turno_servicios_service, reservas_service

router = APIRouter()


# ====================================================
# ENDPOINTS DE RESERVAS (CU-1 a CU-4)
# ====================================================

@router.post("/turnos/{turno_id}/reservar", status_code=status.HTTP_200_OK)
def reservar_turno_endpoint(turno_id: int, request: Dict[str, Any],
                            current_user: Usuario = Depends(require_role("cliente")),
                            admin_check: Usuario = Depends(require_admin)):
    """CU-1: Registra una reserva sobre un turno disponible."""
    try:
        turno = reservas_service.ReservasService.registrar_reserva(
            turno_id=turno_id,
            id_cliente=request.get("id_cliente"),
            id_usuario_registro=request.get("id_usuario_registro")
        )
        return turno.to_dict()
    except ValueError as ve:
        raise HTTPException(status_code=409, detail=str(ve))
    except LookupError as le:
        raise HTTPException(status_code=404, detail=str(le))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")


@router.get("/turnos/{turno_id}/detalle")
def consultar_reserva_endpoint(
    turno_id: int,
    id_cliente: Optional[int] = Query(None, description="Validar pertenencia al cliente"),
    current_user: Usuario = Depends(require_role("cliente"))
):
    """CU-2a: Consulta un turno/reserva por ID con validación opcional de cliente."""
    try:
        turno = reservas_service.ReservasService.consultar_turno_por_id(turno_id, id_cliente=id_cliente)
        return turno.to_dict()
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))
    except LookupError as le:
        raise HTTPException(status_code=404, detail=str(le))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")


@router.get("/turnos/reservas/cliente")
def listar_reservas_cliente_endpoint(
    id_cliente: int = Query(..., description="ID del cliente (obligatorio)"),
    id_cancha: Optional[int] = Query(None, description="Filtrar por cancha"),
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    current_user: Usuario = Depends(require_role("cliente"))
):
    """CU-2b/2c: Lista reservas de un cliente con filtros opcionales."""
    try:
        turnos = reservas_service.ReservasService.listar_reservas_cliente(
            id_cliente=id_cliente,
            id_cancha=id_cancha,
            estado=estado
        )
        return [t.to_dict() for t in turnos]
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")


@router.patch("/turnos/{turno_id}/reserva")
@router.patch("/turnos/{turno_id}")  # Alias para compatibilidad con tests
def modificar_reserva_endpoint(turno_id: int, request: Dict[str, Any], current_user: Usuario = Depends(require_role("cliente"))):
    """CU-3: Modifica una reserva existente."""
    try:
        id_usuario_mod = request.pop("id_usuario_mod", None)
        nuevos_datos = request
        
        if not nuevos_datos:
            raise HTTPException(status_code=400, detail="Debe enviar al menos un campo modificable")
        
        turno = reservas_service.ReservasService.modificar_reserva(
            turno_id=turno_id,
            nuevos_datos=nuevos_datos,
            id_usuario_mod=id_usuario_mod
        )
        return turno.to_dict()
    except HTTPException:
        raise
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except LookupError as le:
        raise HTTPException(status_code=404, detail=str(le))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")


@router.post("/turnos/{turno_id}/cancelar-reserva")
@router.post("/turnos/{turno_id}/cancelar")  # Alias para compatibilidad
def cancelar_reserva_endpoint(turno_id: int, request: Optional[Dict[str, Any]] = None, current_user: Usuario = Depends(require_role("cliente")),
                            admin_check: Usuario = Depends(require_admin)):
    """CU-4: Cancela una reserva y devuelve el turno a disponible."""
    try:
        id_usuario_cancelacion = request.get("id_usuario_cancelacion") if request else None
        if id_usuario_cancelacion:
            turno = reservas_service.ReservasService.cancelar_reserva(
                turno_id=turno_id,
                id_usuario_cancelacion=id_usuario_cancelacion
            )
        else:
            turno = turnos_service.cancelar_reserva(turno_id)
        return turno.to_dict()
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except LookupError as le:
        raise HTTPException(status_code=404, detail=str(le))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")



# ====================================================
# ENDPOINTS CRUD GENERAL DE TURNOS
# ====================================================


@router.post("/turnos/", status_code=status.HTTP_201_CREATED)
def crear_turno(turno_data: Dict[str, Any], current_user: Usuario = Depends(require_admin)):
    """Crea un nuevo turno/slot de cancha."""
    try:
        turno = turnos_service.crear_turno(turno_data)
        return turno.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/turnos/")
def listar_turnos(id_cliente: Optional[int] = Query(None, description="Filtrar por cliente (legacy)")):
    """Lista turnos. Si se proporciona id_cliente, lista reservas de ese cliente."""
    if id_cliente is not None:
        # Delegar a la lógica de reservas para mantener compatibilidad con tests
        try:
            turnos = reservas_service.ReservasService.listar_reservas_cliente(id_cliente=id_cliente)
            return [t.to_dict() for t in turnos]
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))
    
    turnos = turnos_service.listar_turnos()
    return [t.to_dict() for t in turnos]


@router.get("/turnos/cancha/{id_cancha}")
def listar_turnos_por_cancha(id_cancha: int):
    """Lista turnos de una cancha específica."""
    turnos = turnos_service.listar_turnos_por_cancha(id_cancha)
    return [t.to_dict() for t in turnos]


@router.get("/turnos/cliente/{id_cliente}")
def listar_turnos_por_cliente(id_cliente: int):
    """Lista turnos de un cliente específico."""
    turnos = turnos_service.listar_turnos_por_cliente(id_cliente)
    return [t.to_dict() for t in turnos]


@router.get("/turnos/estado/{estado}")
def listar_turnos_por_estado(estado: str):
    """Lista turnos por estado (disponible, reservado, bloqueado, cancelado, finalizado)."""
    turnos = turnos_service.listar_turnos_por_estado(estado)
    return [t.to_dict() for t in turnos]


@router.get("/turnos/disponibles")
def buscar_turnos_disponibles(
    id_cancha: int = Query(..., description="ID de la cancha"),
    fecha_inicio: str = Query(..., description="Fecha/hora inicio (ISO format)"),
    fecha_fin: str = Query(..., description="Fecha/hora fin (ISO format)")
):
    """Busca turnos disponibles en un rango de fechas para una cancha."""
    turnos = turnos_service.buscar_disponibles(id_cancha, fecha_inicio, fecha_fin)
    return [t.to_dict() for t in turnos]


@router.get("/turnos/{turno_id}")
def obtener_turno(turno_id: int, id_cliente: Optional[int] = Query(None, description="Validar pertenencia (opcional)")):
    """Obtiene un turno por su ID. Si se proporciona id_cliente, valida pertenencia."""
    try:
        if id_cliente is not None:
            # Usar el servicio de reservas para validar pertenencia
            turno = reservas_service.ReservasService.consultar_turno_por_id(turno_id, id_cliente=id_cliente)
        else:
            turno = turnos_service.obtener_turno_por_id(turno_id)
        return turno.to_dict()
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/turnos/{turno_id}/precio-total")
def calcular_precio_total(turno_id: int):
    """Calcula el precio total de un turno (precio base + servicios)."""
    try:
        total = turnos_service.calcular_precio_total_turno(turno_id)
        return {"turno_id": turno_id, "precio_total": total}
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/turnos/{turno_id}")
def actualizar_turno(turno_id: int, turno_data: Dict[str, Any], admin_check: Usuario = Depends(require_admin)):
    """Actualiza un turno existente."""
    try:
        turno = turnos_service.actualizar_turno(turno_id, turno_data)
        return turno.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/turnos/{turno_id}/estado")
def cambiar_estado(turno_id: int, payload: Dict[str, str], admin_check: Usuario = Depends(require_admin)):
    """Cambia el estado de un turno."""
    try:
        nuevo_estado = payload.get('estado')
        if not nuevo_estado:
            raise ValueError("El campo 'estado' es requerido")
        
        success = turnos_service.cambiar_estado_turno(turno_id, nuevo_estado)
        return {"success": success, "turno_id": turno_id, "nuevo_estado": nuevo_estado}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


'''@router.post("/turnos/{turno_id}/reservar-simple")
def reservar_turno_simple(turno_id: int, payload: Dict[str, Any]):
    """Reserva un turno para un cliente (versión legacy con Dict)."""
    try:
        id_cliente = payload.get('id_cliente')
        if not id_cliente:
            raise ValueError("El campo 'id_cliente' es requerido")
        
        id_usuario_registro = payload.get('id_usuario_registro')
        turno = turnos_service.reservar_turno(turno_id, id_cliente, id_usuario_registro)
        return turno.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/turnos/{turno_id}/cancelar")
def cancelar_turno_simple(turno_id: int):
    """Cancela una reserva (versión legacy sin body)."""
    try:
        turno = turnos_service.cancelar_reserva(turno_id)
        return turno.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))'''


@router.post("/turnos/{turno_id}/bloquear")
def bloquear_turno(turno_id: int, payload: Dict[str, Any], admin_check: Usuario = Depends(require_admin)):
    """Bloquea un turno (admin/operador)."""
    try:
        id_usuario = payload.get('id_usuario')
        motivo = payload.get('motivo', 'Sin motivo especificado')
        
        if not id_usuario:
            raise ValueError("El campo 'id_usuario' es requerido")
        
        turno = turnos_service.bloquear_turno(turno_id, id_usuario, motivo)
        return turno.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/turnos/{turno_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_turno(turno_id: int, admin_check: Usuario = Depends(require_admin)):
    """Elimina un turno."""
    try:
        turnos_service.eliminar_turno(turno_id)
        return None
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === Endpoints para Servicios Adicionales de Turnos ===

@router.post("/turnos/{turno_id}/servicios", status_code=status.HTTP_201_CREATED)
def agregar_servicio_a_turno(turno_id: int, payload: Dict[str, Any], current_user: Usuario = Depends(require_role("cliente"))):
    """Agrega un servicio adicional a un turno."""
    try:
        payload['id_turno'] = turno_id
        turno_servicio = turno_servicios_service.agregar_servicio_a_turno(payload)
        return turno_servicio.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/turnos/{turno_id}/servicios", response_model=List[Dict[str, Any]])
def listar_servicios_turno(turno_id: int, current_user: Usuario = Depends(require_role("cliente"))):
    """Lista servicios adicionales de un turno."""
    servicios = turno_servicios_service.listar_servicios_por_turno(turno_id)
    return [s.to_dict() for s in servicios]

'''
@router.get("/turnos/{turno_id}/servicios/total")
def calcular_total_servicios(turno_id: int):
    """Calcula el total de servicios adicionales de un turno."""
    total = turno_servicios_service.calcular_total_servicios_turno(turno_id)
    return {"turno_id": turno_id, "total_servicios": total}
''' # No es necesario, ya se calcula en el precio total del turno

@router.delete("/turnos/servicios/{registro_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_servicio_turno(registro_id: int, current_user: Usuario = Depends(require_role("cliente"))):
    """Elimina un servicio adicional de un turno."""
    try:
        turno_servicios_service.eliminar_servicio_turno(registro_id)
        return None
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
