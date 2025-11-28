from typing import List, Dict, Any
from models.equipo_torneo import EquipoTorneo
from repositories.equipo_torneo_repository import EquipoTorneoRepository


def inscribir_equipo_a_torneo(id_equipo: int, id_torneo: int) -> EquipoTorneo:
    """Inscribe un equipo a un torneo"""
    # Validar que no exista ya la inscripción
    if EquipoTorneoRepository.existe_inscripcion(id_equipo, id_torneo):
        raise ValueError(f'El equipo {id_equipo} ya está inscrito en el torneo {id_torneo}')
    
    equipo_torneo = EquipoTorneo(id_equipo=id_equipo, id_torneo=id_torneo)
    try:
        return EquipoTorneoRepository.inscribir_equipo(equipo_torneo)
    except Exception as e:
        raise Exception(f'Error al inscribir equipo al torneo: {e}')


def inscribir_equipos_masivo(id_torneo: int, ids_equipos: List[int]) -> Dict[str, Any]:
    """Inscribe múltiples equipos a un torneo
    
    Returns:
        Dict con el número de equipos inscritos y errores si los hay
    """
    if not ids_equipos:
        return {'inscritos': 0, 'errores': []}
    
    # Filtrar equipos que ya están inscritos
    equipos_a_inscribir = []
    errores = []
    
    for id_equipo in ids_equipos:
        if EquipoTorneoRepository.existe_inscripcion(id_equipo, id_torneo):
            errores.append(f'Equipo {id_equipo} ya inscrito')
        else:
            equipos_a_inscribir.append(id_equipo)
    
    if not equipos_a_inscribir:
        return {'inscritos': 0, 'errores': errores}
    
    try:
        inscritos = EquipoTorneoRepository.inscribir_equipos_masivo(id_torneo, equipos_a_inscribir)
        return {'inscritos': inscritos, 'errores': errores}
    except Exception as e:
        raise Exception(f'Error al inscribir equipos masivamente: {e}')


def obtener_equipos_de_torneo(id_torneo: int) -> List[EquipoTorneo]:
    """Obtiene todos los equipos inscritos en un torneo"""
    try:
        return EquipoTorneoRepository.obtener_equipos_por_torneo(id_torneo)
    except Exception as e:
        raise Exception(f'Error al obtener equipos del torneo: {e}')


def obtener_torneos_de_equipo(id_equipo: int) -> List[EquipoTorneo]:
    """Obtiene todos los torneos en los que participa un equipo"""
    try:
        return EquipoTorneoRepository.obtener_torneos_por_equipo(id_equipo)
    except Exception as e:
        raise Exception(f'Error al obtener torneos del equipo: {e}')


def desinscribir_equipo_de_torneo(id_equipo: int, id_torneo: int) -> bool:
    """Elimina la inscripción de un equipo a un torneo"""
    if not EquipoTorneoRepository.existe_inscripcion(id_equipo, id_torneo):
        raise LookupError(f'No existe inscripción del equipo {id_equipo} en el torneo {id_torneo}')
    
    try:
        return EquipoTorneoRepository.eliminar_inscripcion(id_equipo, id_torneo)
    except Exception as e:
        raise Exception(f'Error al desinscribir equipo del torneo: {e}')


def desinscribir_equipos_masivo(inscripciones: List[tuple]) -> int:
    """Elimina múltiples inscripciones
    
    Args:
        inscripciones: Lista de tuplas (id_equipo, id_torneo)
    
    Returns:
        Número de inscripciones eliminadas
    """
    try:
        return EquipoTorneoRepository.eliminar_inscripciones_masivo(inscripciones)
    except Exception as e:
        raise Exception(f'Error al desinscribir equipos masivamente: {e}')


def contar_equipos_en_torneo(id_torneo: int) -> int:
    """Cuenta cuántos equipos están inscritos en un torneo"""
    try:
        return EquipoTorneoRepository.contar_equipos_en_torneo(id_torneo)
    except Exception as e:
        raise Exception(f'Error al contar equipos del torneo: {e}')


def eliminar_inscripciones_de_torneo(id_torneo: int) -> int:
    """Elimina todas las inscripciones asociadas a un torneo"""
    try:
        return EquipoTorneoRepository.eliminar_por_torneo(id_torneo)
    except Exception as e:
        raise Exception(f'Error al eliminar inscripciones del torneo: {e}')


def eliminar_inscripciones_de_equipo(id_equipo: int) -> int:
    """Elimina todas las inscripciones de un equipo"""
    try:
        return EquipoTorneoRepository.eliminar_por_equipo(id_equipo)
    except Exception as e:
        raise Exception(f'Error al eliminar inscripciones del equipo: {e}')
