from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Dict, Any, Optional

from services import equipos_service

router = APIRouter()


@router.post("/equipos/", status_code=status.HTTP_201_CREATED)
def crear_equipo(payload: Dict[str, Any]):
    try:
        equipo = equipos_service.crear_equipo(payload)
        return equipo.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/equipos/", response_model=List[Dict[str, Any]])
def listar_equipos(nombre: Optional[str] = Query(None)):
    if nombre:
        equipos = equipos_service.buscar_equipos(nombre)
    else:
        equipos = equipos_service.listar_equipos()
    return [e.to_dict() for e in equipos]


@router.get("/equipos/{equipo_id}", response_model=Dict[str, Any])
def obtener_equipo(equipo_id: int):
    try:
        equipo = equipos_service.obtener_equipo_por_id(equipo_id)
        return equipo.to_dict()
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/equipos/nombre/{nombre}", response_model=Dict[str, Any])
def obtener_equipo_por_nombre(nombre: str):
    try:
        equipo = equipos_service.obtener_equipo_por_nombre(nombre)
        return equipo.to_dict()
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/equipos/{equipo_id}", response_model=Dict[str, Any])
def actualizar_equipo(equipo_id: int, payload: Dict[str, Any]):
    try:
        equipo = equipos_service.actualizar_equipo(equipo_id, payload)
        return equipo.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/equipos/{equipo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_equipo(equipo_id: int):
    try:
        equipos_service.eliminar_equipo(equipo_id)
        return None
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
