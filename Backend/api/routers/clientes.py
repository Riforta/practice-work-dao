from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional

from api.schemas.clientes import (
    ClienteResponse,
    ClienteCreateRequest,
    ClienteUpdateRequest
)
from services import clientes_service

router = APIRouter()


@router.post("/clientes/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def crear_cliente(cliente_data: ClienteCreateRequest):
    try:
        payload = cliente_data.model_dump()
        cliente = clientes_service.crear_cliente(payload)
        return ClienteResponse.model_validate(cliente)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/clientes/", response_model=List[ClienteResponse])
def listar_clientes():
    clientes = clientes_service.listar_clientes()
    return [ClienteResponse.model_validate(c) for c in clientes]


@router.get("/clientes/search", response_model=List[ClienteResponse])
def buscar_clientes(nombre: Optional[str] = Query(None, description="Nombre o apellido a buscar")):
    if not nombre:
        return []
    result = clientes_service.buscar_clientes_por_nombre(nombre)
    return [ClienteResponse.model_validate(c) for c in result]


@router.get("/clientes/{cliente_id}", response_model=ClienteResponse)
def obtener_cliente(cliente_id: int):
    try:
        cliente = clientes_service.obtener_cliente_por_id(cliente_id)
        return ClienteResponse.model_validate(cliente)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/clientes/{cliente_id}", response_model=ClienteResponse)
def actualizar_cliente(cliente_id: int, cliente_data: ClienteUpdateRequest):
    try:
        payload = cliente_data.model_dump(exclude_unset=True)
        cliente = clientes_service.actualizar_cliente(cliente_id, payload)
        return ClienteResponse.model_validate(cliente)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/clientes/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente(cliente_id: int):
    try:
        clientes_service.eliminar_cliente(cliente_id)
        return None
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
