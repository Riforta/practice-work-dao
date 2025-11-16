from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Dict, Any, Optional

from services import pedidos_service

router = APIRouter()


@router.post("/pedidos/", status_code=status.HTTP_201_CREATED)
def crear_pedido(payload: Dict[str, Any]):
    try:
        pedido = pedidos_service.crear_pedido(payload)
        return pedido.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pedidos/", response_model=List[Dict[str, Any]])
def listar_pedidos(cliente_id: Optional[int] = Query(None)):
    if cliente_id:
        pedidos = pedidos_service.listar_pedidos_por_cliente(cliente_id)
    else:
        # if no specific listing available, return empty or consider exposing all
        pedidos = []
    return [p.to_dict() for p in pedidos]


@router.get("/pedidos/{pedido_id}", response_model=Dict[str, Any])
def obtener_pedido(pedido_id: int):
    try:
        pedido = pedidos_service.obtener_pedido_por_id(pedido_id)
        return pedido.to_dict()
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/pedidos/{pedido_id}", response_model=Dict[str, Any])
def actualizar_pedido(pedido_id: int, payload: Dict[str, Any]):
    try:
        pedido = pedidos_service.actualizar_pedido(pedido_id, payload)
        return pedido.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/pedidos/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_pedido(pedido_id: int):
    try:
        pedidos_service.eliminar_pedido(pedido_id)
        return None
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
