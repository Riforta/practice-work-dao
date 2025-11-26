'''
from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any

from services import roles_service

router = APIRouter()


@router.post("/roles/", status_code=status.HTTP_201_CREATED)
def crear_rol(payload: Dict[str, Any]):
    try:
        r = roles_service.crear_rol(payload)
        return r.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/roles/", response_model=List[Dict[str, Any]])
def listar_roles():
    items = roles_service.listar_roles()
    return [i.to_dict() for i in items]


@router.get("/roles/{rol_id}", response_model=Dict[str, Any])
def obtener_rol(rol_id: int):
    try:
        r = roles_service.obtener_rol_por_id(rol_id)
        return r.to_dict()
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/roles/{rol_id}", response_model=Dict[str, Any])
def actualizar_rol(rol_id: int, payload: Dict[str, Any]):
    try:
        r = roles_service.actualizar_rol(rol_id, payload)
        return r.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/roles/{rol_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_rol(rol_id: int):
    try:
        roles_service.eliminar_rol(rol_id)
        return None
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
'''