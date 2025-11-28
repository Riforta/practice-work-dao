from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Dict, Any, Optional

from services import pagos_service
from api.dependencies.auth import get_current_user
from models.usuario import Usuario

router = APIRouter()


@router.get("/pagos/", response_model=List[Dict[str, Any]])
def listar_todos_pagos(
    current_user: Usuario = Depends(get_current_user)
):
    """Lista todos los pagos del sistema (para admin)"""
    try:
        pagos = pagos_service.listar_todos_pagos()
        return [p.to_dict() for p in pagos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pagos/manual", status_code=status.HTTP_201_CREATED)
def crear_pago_manual(
    payload: Dict[str, Any],
    current_user: Usuario = Depends(get_current_user)
):
    """
    Crea un pago manual (por admin, para pagos en efectivo u otros).
    
    Body esperado:
    {
        "id_cliente": 1,
        "id_turno": 123,  // opcional
        "monto_turno": 5000.0,
        "monto_servicios": 0.0,
        "monto_total": 5000.0,
        "metodo_pago": "efectivo",
        "estado": "completado"  // iniciado, completado, fallido
    }
    """
    try:
        pago = pagos_service.crear_pago_manual(
            id_cliente=payload['id_cliente'],
            id_turno=payload.get('id_turno'),
            monto_turno=payload.get('monto_turno', 0.0),
            monto_servicios=payload.get('monto_servicios', 0.0),
            monto_total=payload['monto_total'],
            metodo_pago=payload.get('metodo_pago'),
            estado=payload.get('estado', 'confirmado'),
            id_usuario_registro=current_user.id
        )
        return pago.to_dict()
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f'Campo requerido faltante: {e}')
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pagos/turno", status_code=status.HTTP_201_CREATED)
def crear_pago_para_turno(
    payload: Dict[str, Any],
    current_user: Usuario = Depends(get_current_user)
):
    """
    Crea un pago para reservar un turno.
    
    Body esperado:
    {
        "id_turno": 123,
        "id_cliente": 1,
        "monto_turno": 5000.0,
        "monto_servicios": 1500.0,
        "servicios": [  // opcional
            {
                "id_servicio": 1,
                "cantidad": 2,
                "precio_unitario": 750.0
            }
        ],
        "metodo_pago": "tarjeta"  // opcional
    }
    """
    try:
        pago = pagos_service.crear_pago_turno(
            id_turno=payload['id_turno'],
            id_cliente=payload['id_cliente'],
            monto_turno=payload['monto_turno'],
            monto_servicios=payload.get('monto_servicios', 0.0),
            servicios=payload.get('servicios'),
            id_usuario_registro=current_user.id,
            metodo_pago=payload.get('metodo_pago')
        )
        return pago.to_dict()
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f'Campo requerido faltante: {e}')
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pagos/inscripcion", status_code=status.HTTP_201_CREATED)
def crear_pago_para_inscripcion(
    payload: Dict[str, Any],
    current_user: Usuario = Depends(get_current_user)
):
    """
    Crea un pago para una inscripción de torneo.
    
    Body esperado:
    {
        "id_inscripcion": 456,
        "id_cliente": 1,
        "monto_total": 3000.0,
        "metodo_pago": "efectivo"  // opcional
    }
    """
    try:
        pago = pagos_service.crear_pago_inscripcion(
            id_inscripcion=payload['id_inscripcion'],
            id_cliente=payload['id_cliente'],
            monto_total=payload['monto_total'],
            id_usuario_registro=current_user.id,
            metodo_pago=payload.get('metodo_pago')
        )
        return pago.to_dict()
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f'Campo requerido faltante: {e}')
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pagos/{pago_id}/confirmar", status_code=status.HTTP_200_OK)
def confirmar_pago(
    pago_id: int,
    payload: Dict[str, Any],
    current_user: Usuario = Depends(get_current_user)
):
    """
    Confirma un pago y marca el turno/inscripción como pagado.
    
    Body esperado:
    {
        "metodo_pago": "tarjeta",  // opcional
        "id_gateway_externo": "TXN123456"  // opcional
    }
    """
    try:
        pago = pagos_service.confirmar_pago(
            pago_id=pago_id,
            metodo_pago=payload.get('metodo_pago'),
            id_gateway_externo=payload.get('id_gateway_externo')
        )
        return pago.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pagos/{pago_id}/marcar-fallido", status_code=status.HTTP_200_OK)
def marcar_pago_fallido_endpoint(
    pago_id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Marca un pago como fallido y libera el turno/inscripción.
    """
    try:
        resultado = pagos_service.marcar_pago_fallido(pago_id)
        return {"success": resultado, "mensaje": "Pago marcado como fallido"}
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pagos/procesar-expirados", status_code=status.HTTP_200_OK)
def procesar_pagos_expirados_endpoint(
    current_user: Usuario = Depends(get_current_user)
):
    """
    Procesa todos los pagos expirados (debe ejecutarse periódicamente).
    Requiere permisos de admin.
    """
    # TODO: Agregar validación de rol admin si es necesario
    try:
        cantidad = pagos_service.procesar_pagos_expirados()
        return {"procesados": cantidad, "mensaje": f"{cantidad} pagos expirados procesados"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pagos/cliente/{id_cliente}", response_model=List[Dict[str, Any]])
def listar_pagos_por_cliente(
    id_cliente: int,
    current_user: Usuario = Depends(get_current_user)
):
    """Lista todos los pagos de un cliente"""
    pagos = pagos_service.listar_pagos_por_cliente(id_cliente)
    return [p.to_dict() for p in pagos]


@router.get("/pagos/turno/{id_turno}", response_model=Dict[str, Any])
def obtener_pago_por_turno(
    id_turno: int,
    current_user: Usuario = Depends(get_current_user)
):
    """Obtiene el pago asociado a un turno"""
    pago = pagos_service.obtener_pago_por_turno(id_turno)
    if not pago:
        raise HTTPException(status_code=404, detail="No se encontró pago para este turno")
    return pago.to_dict()


@router.get("/pagos/inscripcion/{id_inscripcion}", response_model=Dict[str, Any])
def obtener_pago_por_inscripcion(
    id_inscripcion: int,
    current_user: Usuario = Depends(get_current_user)
):
    """Obtiene el pago asociado a una inscripción"""
    pago = pagos_service.obtener_pago_por_inscripcion(id_inscripcion)
    if not pago:
        raise HTTPException(status_code=404, detail="No se encontró pago para esta inscripción")
    return pago.to_dict()


@router.get("/pagos/{pago_id}", response_model=Dict[str, Any])
def obtener_pago(
    pago_id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """Obtiene un pago por su ID"""
    try:
        pago = pagos_service.obtener_pago_por_id(pago_id)
        return pago.to_dict()
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/pagos/{pago_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_pago(
    pago_id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """Elimina un pago (usar con precaución)"""
    # TODO: Agregar validación de rol admin
    try:
        pagos_service.eliminar_pago(pago_id)
        return None
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
