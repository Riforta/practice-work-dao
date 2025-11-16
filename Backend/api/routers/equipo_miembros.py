from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Dict, Any, Optional

from services import equipo_miembros_service

router = APIRouter()


@router.post("/equipo_miembros/", status_code=status.HTTP_201_CREATED)
def agregar_miembro(payload: Dict[str, Any]):
    try:
        equipo_miembros_service.agregar_miembro(payload)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/equipo_miembros/", response_model=List[Dict[str, Any]])
def listar_miembros(equipo_id: Optional[int] = Query(None)):
    if not equipo_id:
        return []
    miembros = equipo_miembros_service.listar_miembros_por_equipo(equipo_id)
    return [m.to_dict() for m in miembros]


@router.delete("/equipo_miembros/{equipo_id}/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_miembro(equipo_id: int, cliente_id: int):
    try:
        equipo_miembros_service.eliminar_miembro(equipo_id, cliente_id)
        return None
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
