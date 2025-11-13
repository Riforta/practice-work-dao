from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Dict, Any, Optional

from services import clientes_services

router = APIRouter()


@router.post("/clientes/", status_code=status.HTTP_201_CREATED)
def crear_cliente(payload: Dict[str, Any]):
    try:
        cliente = clientes_services.crear_cliente(payload)
        return cliente.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/clientes/", response_model=List[Dict[str, Any]])
def listar_clientes():
    clientes = clientes_services.listar_clientes()
    return [c.to_dict() for c in clientes]


@router.get("/clientes/search", response_model=List[Dict[str, Any]])
def buscar_clientes(nombre: Optional[str] = Query(None, description="Nombre o apellido a buscar")):
    if not nombre:
        return []
    result = clientes_services.buscar_clientes_por_nombre(nombre)
    return [c.to_dict() for c in result]


@router.get("/clientes/{cliente_id}", response_model=Dict[str, Any])
def obtener_cliente(cliente_id: int):
    try:
        cliente = clientes_services.obtener_cliente_por_id(cliente_id)
        return cliente.to_dict()
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/clientes/{cliente_id}", response_model=Dict[str, Any])
def actualizar_cliente(cliente_id: int, payload: Dict[str, Any]):
    try:
        cliente = clientes_services.actualizar_cliente(cliente_id, payload)
        return cliente.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/clientes/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente(cliente_id: int):
    try:
        clientes_services.eliminar_cliente(cliente_id)
        return None
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
