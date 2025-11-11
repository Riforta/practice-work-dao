from typing import List, Dict, Any

from models.torneo import Torneo
from repository.torneo_repository import TorneoRepository


def crear_torneo(data: Dict[str, Any]) -> Torneo:
    if not data.get('nombre'):
        raise ValueError('El nombre del torneo es obligatorio')

    torneo = Torneo.from_dict(data)
    try:
        torneo.id = TorneoRepository.crear(torneo)
        return torneo
    except Exception as e:
        raise Exception(f'Error al crear torneo: {e}')


def obtener_torneo_por_id(torneo_id: int) -> Torneo:
    torneo = TorneoRepository.obtener_por_id(torneo_id)
    if torneo is None:
        raise LookupError(f'Torneo con ID {torneo_id} no encontrado')
    return torneo


def listar_torneos() -> List[Torneo]:
    return TorneoRepository.obtener_todos()


def actualizar_torneo(torneo_id: int, data: Dict[str, Any]) -> Torneo:
    existente = TorneoRepository.obtener_por_id(torneo_id)
    if existente is None:
        raise LookupError(f'Torneo con ID {torneo_id} no encontrado')

    updated = existente.to_dict()
    updated.update(data)
    torneo_actualizado = Torneo.from_dict(updated)
    torneo_actualizado.id = torneo_id

    try:
        ok = TorneoRepository.actualizar(torneo_actualizado)
        if not ok:
            raise Exception('No se actualizó el torneo')
        return torneo_actualizado
    except Exception as e:
        raise Exception(f'Error al actualizar torneo: {e}')


def eliminar_torneo(torneo_id: int) -> bool:
    try:
        return TorneoRepository.eliminar(torneo_id)
    except Exception as e:
        raise Exception(f'Error al eliminar torneo: {e}')
