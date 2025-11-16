from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Dict, Any, Optional

from services import usuarios_service

router = APIRouter()


@router.post("/usuarios/", status_code=status.HTTP_201_CREATED)
def crear_usuario(payload: Dict[str, Any]):
    try:
        u = usuarios_service.crear_usuario(payload)
        d = u.to_dict()
        d.pop('password_hash', None)
        return d
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/usuarios/", response_model=List[Dict[str, Any]])
def listar_usuarios():
    items = usuarios_service.listar_usuarios()
    results = []
    for i in items:
        d = i.to_dict()
        d.pop('password_hash', None)
        results.append(d)
    return results


@router.get("/usuarios/{usuario_id}", response_model=Dict[str, Any])
def obtener_usuario(usuario_id: int):
    try:
        u = usuarios_service.obtener_usuario_por_id(usuario_id)
        d = u.to_dict()
        d.pop('password_hash', None)
        return d
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/usuarios/{usuario_id}", response_model=Dict[str, Any])
def actualizar_usuario(usuario_id: int, payload: Dict[str, Any]):
    try:
        u = usuarios_service.actualizar_usuario(usuario_id, payload)
        return u.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(usuario_id: int):
    try:
        usuarios_service.eliminar_usuario(usuario_id)
        return None
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
