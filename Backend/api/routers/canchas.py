from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any

from services import canchas_service

router = APIRouter()


@router.post("/canchas/", status_code=status.HTTP_201_CREATED)
def crear_cancha(cancha_data: Dict[str, Any]):
    try:
        cancha = canchas_service.crear_cancha(cancha_data)
        return cancha.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/canchas/")
def listar_canchas():
    canchas = canchas_service.listar_canchas()
    return [c.to_dict() for c in canchas]


@router.get("/canchas/{cancha_id}")
def obtener_cancha(cancha_id: int):
    try:
        cancha = canchas_service.obtener_cancha_por_id(cancha_id)
        return cancha.to_dict()
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/canchas/{nombre}", response_model=Dict[str, Any])
def obtener_cancha_por_nombre(nombre: str):
    try:
        cancha = canchas_service.obtener_cancha_por_nombre(nombre)
        return cancha.to_dict()
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/canchas/{cancha_id}")
def actualizar_cancha(cancha_id: int, cancha_data: Dict[str, Any]):
    try:
        cancha = canchas_service.actualizar_cancha(cancha_id, cancha_data)
        return cancha.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/canchas/{cancha_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cancha(cancha_id: int):
    try:
        canchas_service.eliminar_cancha(cancha_id)
        return None
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
