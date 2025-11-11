from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any

from services import partidos_services

router = APIRouter()


@router.post("/partidos/", status_code=status.HTTP_201_CREATED)
def crear_partido(payload: Dict[str, Any]):
    try:
        partido = partidos_services.crear_partido(payload)
        return partido.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/partidos/", response_model=List[Dict[str, Any]])
def listar_partidos():
    partidos = partidos_services.listar_partidos()
    return [p.to_dict() for p in partidos]


@router.get("/partidos/{partido_id}", response_model=Dict[str, Any])
def obtener_partido(partido_id: int):
    try:
        partido = partidos_services.obtener_partido_por_id(partido_id)
        return partido.to_dict()
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/partidos/{partido_id}", response_model=Dict[str, Any])
def actualizar_partido(partido_id: int, payload: Dict[str, Any]):
    try:
        partido = partidos_services.actualizar_partido(partido_id, payload)
        return partido.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/partidos/{partido_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_partido(partido_id: int):
    try:
        partidos_services.eliminar_partido(partido_id)
        return None
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
