from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Dict, Any

from api.dependencies.auth import require_admin, require_role
from models.usuario import Usuario
from services import clientes_service

router = APIRouter()


@router.post("/clientes/", status_code=status.HTTP_201_CREATED)
def crear_cliente(cliente_data: Dict[str, Any], admin_check: Usuario = Depends(require_admin)):
    try:
        cliente = clientes_service.crear_cliente(cliente_data)
        return cliente.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/clientes/")
def listar_clientes():
    clientes = clientes_service.listar_clientes()
    return [c.to_dict() for c in clientes]


@router.get("/clientes/search")
def buscar_clientes(nombre: Optional[str] = Query(None, description="Nombre o apellido a buscar")):
    if not nombre:
        return []
    result = clientes_service.buscar_clientes_por_nombre(nombre)
    return [c.to_dict() for c in result]


@router.get("/clientes/{cliente_id}")
def obtener_cliente(cliente_id: int):
    try:
        cliente = clientes_service.obtener_cliente_por_id(cliente_id)
        return cliente.to_dict()
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/clientes/{cliente_id}")
def actualizar_cliente(cliente_id: int, cliente_data: Dict[str, Any], current_user: Usuario = Depends(require_role("cliente"))):
    try:
        cliente = clientes_service.actualizar_cliente(cliente_id, cliente_data)
        return cliente.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/clientes/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente(cliente_id: int, current_user: Usuario = Depends(require_admin)):
    try:
        clientes_service.eliminar_cliente(cliente_id)
        return None
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
