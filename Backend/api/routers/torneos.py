from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any

from services import torneos_services

router = APIRouter()


@router.post("/torneos/", status_code=status.HTTP_201_CREATED)
def crear_torneo(payload: Dict[str, Any]):
    try:
        t = torneos_services.crear_torneo(payload)
        return t.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/torneos/", response_model=List[Dict[str, Any]])
def listar_torneos():
    items = torneos_services.listar_torneos()
    return [i.to_dict() for i in items]


@router.get("/torneos/{torneo_id}", response_model=Dict[str, Any])
def obtener_torneo(torneo_id: int):
    try:
        t = torneos_services.obtener_torneo_por_id(torneo_id)
        return t.to_dict()
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/torneos/{torneo_id}", response_model=Dict[str, Any])
def actualizar_torneo(torneo_id: int, payload: Dict[str, Any]):
    try:
        t = torneos_services.actualizar_torneo(torneo_id, payload)
        return t.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/torneos/{torneo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_torneo(torneo_id: int):
    try:
        torneos_services.eliminar_torneo(torneo_id)
        return None
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
