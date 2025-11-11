from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any

from services import servicios_adicionales_services

router = APIRouter()


@router.post("/servicios_adicionales/", status_code=status.HTTP_201_CREATED)
def crear_servicio(payload: Dict[str, Any]):
    try:
        s = servicios_adicionales_services.crear_servicio_adicional(payload)
        return s.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/servicios_adicionales/", response_model=List[Dict[str, Any]])
def listar_servicios():
    items = servicios_adicionales_services.listar_servicios()
    return [i.to_dict() for i in items]


@router.get("/servicios_adicionales/{servicio_id}", response_model=Dict[str, Any])
def obtener_servicio(servicio_id: int):
    try:
        s = servicios_adicionales_services.obtener_servicio_por_id(servicio_id)
        return s.to_dict()
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/servicios_adicionales/{servicio_id}", response_model=Dict[str, Any])
def actualizar_servicio(servicio_id: int, payload: Dict[str, Any]):
    try:
        s = servicios_adicionales_services.actualizar_servicio(servicio_id, payload)
        return s.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/servicios_adicionales/{servicio_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_servicio(servicio_id: int):
    try:
        servicios_adicionales_services.eliminar_servicio(servicio_id)
        return None
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
