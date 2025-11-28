"""
Router para gestionar la relación EquipoXTorneo (inscripciones de equipos en torneos).
"""
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from services.equipo_torneo_service import (
    inscribir_equipo_a_torneo,
    inscribir_equipos_masivo,
    desinscribir_equipo_de_torneo,
    desinscribir_equipos_masivo,
    obtener_equipos_de_torneo,
    obtener_torneos_de_equipo,
    contar_equipos_en_torneo,
    eliminar_inscripciones_de_torneo,
    eliminar_inscripciones_de_equipo,
)

router = APIRouter(
    prefix="/equipo-torneo",
    tags=["Equipo-Torneo"]
)


@router.post("/inscribir")
def inscribir_equipo(payload: Dict[str, Any]):
    """Inscribe un equipo a un torneo"""
    try:
        id_equipo = payload.get('id_equipo')
        id_torneo = payload.get('id_torneo')
        
        if not id_equipo or not id_torneo:
            raise HTTPException(status_code=400, detail="id_equipo e id_torneo son requeridos")
        
        equipo_torneo = inscribir_equipo_a_torneo(
            id_equipo=id_equipo,
            id_torneo=id_torneo
        )
        return {"message": "Equipo inscrito correctamente", "data": equipo_torneo.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al inscribir equipo: {e}")


@router.post("/inscribir-masivo")
def inscribir_equipos_masivo_route(payload: Dict[str, Any]):
    """Inscribe múltiples equipos a un torneo"""
    try:
        ids_equipos = payload.get('ids_equipos', [])
        id_torneo = payload.get('id_torneo')
        
        if not id_torneo:
            raise HTTPException(status_code=400, detail="id_torneo es requerido")
        if not ids_equipos:
            raise HTTPException(status_code=400, detail="ids_equipos no puede estar vacío")
        
        count = inscribir_equipos_masivo(
            ids_equipos=ids_equipos,
            id_torneo=id_torneo
        )
        return {"message": f"{count} equipos inscritos correctamente", "count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al inscribir equipos: {e}")


@router.delete("/desinscribir")
def desinscribir_equipo(id_equipo: int, id_torneo: int):
    """Desinscribe un equipo de un torneo"""
    try:
        success = desinscribir_equipo_de_torneo(id_equipo, id_torneo)
        if not success:
            raise HTTPException(status_code=404, detail="La inscripción no existe")
        return {"message": "Equipo desinscrito correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al desinscribir equipo: {e}")


@router.delete("/desinscribir-masivo")
def desinscribir_equipos_masivo_route(payload: Dict[str, Any]):
    """Desinscribe múltiples equipos de torneos"""
    try:
        inscripciones = payload.get('inscripciones', [])
        if not inscripciones:
            raise HTTPException(status_code=400, detail="inscripciones no puede estar vacío")
        
        count = desinscribir_equipos_masivo(inscripciones)
        return {"message": f"{count} equipos desinscritos correctamente", "count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al desinscribir equipos: {e}")


@router.get("/torneo/{id_torneo}")
def listar_equipos_por_torneo(id_torneo: int):
    """Lista todos los equipos inscritos en un torneo"""
    try:
        equipos = obtener_equipos_de_torneo(id_torneo)
        return {"items": [eq.to_dict() for eq in equipos], "count": len(equipos)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener equipos del torneo: {e}")


@router.get("/equipo/{id_equipo}")
def listar_torneos_por_equipo(id_equipo: int):
    """Lista todos los torneos en los que está inscrito un equipo"""
    try:
        torneos = obtener_torneos_de_equipo(id_equipo)
        return {"items": [t.to_dict() for t in torneos], "count": len(torneos)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener torneos del equipo: {e}")


@router.get("/torneo/{id_torneo}/count")
def contar_equipos_torneo(id_torneo: int):
    """Cuenta cuántos equipos están inscritos en un torneo"""
    try:
        count = contar_equipos_en_torneo(id_torneo)
        return {"count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al contar equipos: {e}")


@router.delete("/torneo/{id_torneo}/all")
def eliminar_todas_inscripciones_torneo(id_torneo: int):
    """Elimina todas las inscripciones de un torneo"""
    try:
        count = eliminar_inscripciones_de_torneo(id_torneo)
        return {"message": f"{count} inscripciones eliminadas", "count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar inscripciones: {e}")


@router.delete("/equipo/{id_equipo}/all")
def eliminar_todas_inscripciones_equipo(id_equipo: int):
    """Elimina todas las inscripciones de un equipo"""
    try:
        count = eliminar_inscripciones_de_equipo(id_equipo)
        return {"message": f"{count} inscripciones eliminadas", "count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar inscripciones: {e}")
