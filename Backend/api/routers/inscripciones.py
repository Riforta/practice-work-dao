from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any

from services import inscripciones_services

router = APIRouter()


@router.post("/inscripciones/", status_code=status.HTTP_201_CREATED)
def crear_inscripcion(payload: Dict[str, Any]):
    try:
        insc = inscripciones_services.crear_inscripcion(payload)
        return insc.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/inscripciones/", response_model=List[Dict[str, Any]])
def listar_inscripciones():
    insc = inscripciones_services.listar_inscripciones()
    return [i.to_dict() for i in insc]


@router.get("/inscripciones/{inscripcion_id}", response_model=Dict[str, Any])
def obtener_inscripcion(inscripcion_id: int):
    try:
        insc = inscripciones_services.obtener_inscripcion_por_id(inscripcion_id)
        return insc.to_dict()
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/inscripciones/{inscripcion_id}", response_model=Dict[str, Any])
def actualizar_inscripcion(inscripcion_id: int, payload: Dict[str, Any]):
    try:
        insc = inscripciones_services.actualizar_inscripcion(inscripcion_id, payload)
        return insc.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/inscripciones/{inscripcion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_inscripcion(inscripcion_id: int):
    try:
        inscripciones_services.eliminar_inscripcion(inscripcion_id)
        return None
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
