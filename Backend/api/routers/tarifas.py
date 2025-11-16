from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any

from services import tarifas_service

router = APIRouter()


@router.post("/tarifas/", status_code=status.HTTP_201_CREATED)
def crear_tarifa(payload: Dict[str, Any]):
    try:
        t = tarifas_service.crear_tarifa(payload)
        return t.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tarifas/", response_model=List[Dict[str, Any]])
def listar_tarifas():
    items = tarifas_service.listar_tarifas()
    return [i.to_dict() for i in items]


@router.get("/tarifas/{tarifa_id}", response_model=Dict[str, Any])
def obtener_tarifa(tarifa_id: int):
    try:
        t = tarifas_service.obtener_tarifa_por_id(tarifa_id)
        return t.to_dict()
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/tarifas/{tarifa_id}", response_model=Dict[str, Any])
def actualizar_tarifa(tarifa_id: int, payload: Dict[str, Any]):
    try:
        t = tarifas_service.actualizar_tarifa(tarifa_id, payload)
        return t.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/tarifas/{tarifa_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tarifa(tarifa_id: int):
    try:
        tarifas_service.eliminar_tarifa(tarifa_id)
        return None
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
