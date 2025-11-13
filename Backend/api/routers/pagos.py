from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Dict, Any, Optional

from services import pagos_services

router = APIRouter()


@router.post("/pagos/", status_code=status.HTTP_201_CREATED)
def crear_pago(payload: Dict[str, Any]):
    try:
        pago = pagos_services.crear_pago(payload)
        return pago.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pagos/", response_model=List[Dict[str, Any]])
def listar_pagos(pedido_id: Optional[int] = Query(None)):
    if not pedido_id:
        return []
    pagos = pagos_services.listar_pagos_por_pedido(pedido_id)
    return [p.to_dict() for p in pagos]


@router.get("/pagos/{pago_id}", response_model=Dict[str, Any])
def obtener_pago(pago_id: int):
    try:
        pago = pagos_services.obtener_pago_por_id(pago_id)
        return pago.to_dict()
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/pagos/{pago_id}", response_model=Dict[str, Any])
def actualizar_pago(pago_id: int, payload: Dict[str, Any]):
    try:
        pago = pagos_services.actualizar_pago(pago_id, payload)
        return pago.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/pagos/{pago_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_pago(pago_id: int):
    try:
        pagos_services.eliminar_pago(pago_id)
        return None
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
