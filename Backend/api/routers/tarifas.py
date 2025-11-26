from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Dict, Any, Optional

from services import tarifas_service

router = APIRouter()


@router.get("/tarifas/", response_model=List[Dict[str, Any]])
def listar_tarifas(id_cancha: Optional[int] = Query(None, description="Filtrar por cancha")):
    tarifas = tarifas_service.listar_tarifas(id_cancha=id_cancha)
    return [t.to_dict() for t in tarifas]


@router.get("/tarifas/{tarifa_id}", response_model=Dict[str, Any])
def obtener_tarifa(tarifa_id: int):
    try:
        tarifa = tarifas_service.obtener_tarifa_por_id(tarifa_id)
        return tarifa.to_dict()
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/tarifas/", status_code=status.HTTP_201_CREATED)
def crear_tarifa(payload: Dict[str, Any]):
    try:
        tarifa = tarifas_service.crear_tarifa(payload)
        return tarifa.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/tarifas/{tarifa_id}", response_model=Dict[str, Any])
def actualizar_tarifa(tarifa_id: int, payload: Dict[str, Any]):
    try:
        tarifa = tarifas_service.actualizar_tarifa(tarifa_id, payload)
        return tarifa.to_dict()
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
