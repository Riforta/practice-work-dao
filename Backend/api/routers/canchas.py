from fastapi import APIRouter, HTTPException, status
from typing import List

from api.schemas.canchas import (
    CanchaResponse,
    CanchaCreateRequest,
    CanchaUpdateRequest
)
from services import canchas_service

router = APIRouter()


@router.post("/canchas/", response_model=CanchaResponse, status_code=status.HTTP_201_CREATED)
def crear_cancha(cancha_data: CanchaCreateRequest):
    try:
        payload = cancha_data.model_dump()
        cancha = canchas_service.crear_cancha(payload)
        return CanchaResponse.model_validate(cancha)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/canchas/", response_model=List[CanchaResponse])
def listar_canchas():
    canchas = canchas_service.listar_canchas()
    return [CanchaResponse.model_validate(c) for c in canchas]


@router.get("/canchas/{cancha_id}", response_model=CanchaResponse)
def obtener_cancha(cancha_id: int):
    try:
        cancha = canchas_service.obtener_cancha_por_id(cancha_id)
        return CanchaResponse.model_validate(cancha)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/canchas/{cancha_id}", response_model=CanchaResponse)
def actualizar_cancha(cancha_id: int, cancha_data: CanchaUpdateRequest):
    try:
        payload = cancha_data.model_dump(exclude_unset=True)
        cancha = canchas_service.actualizar_cancha(cancha_id, payload)
        return CanchaResponse.model_validate(cancha)
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
