from typing import List, Dict, Any

from models.partido import Partido
from repository.partido_repository import PartidoRepository


def crear_partido(data: Dict[str, Any]) -> Partido:
    partido = Partido.from_dict(data)
    try:
        partido.id = PartidoRepository.crear(partido)
        return partido
    except Exception as e:
        raise Exception(f'Error al crear partido: {e}')


def obtener_partido_por_id(partido_id: int) -> Partido:
    partido = PartidoRepository.obtener_por_id(partido_id)
    if partido is None:
        raise LookupError(f'Partido con ID {partido_id} no encontrado')
    return partido


def listar_partidos() -> List[Partido]:
    return PartidoRepository.obtener_todos()


def listar_partidos_por_torneo(torneo_id: int) -> List[Partido]:
    return PartidoRepository.obtener_por_torneo(torneo_id)


def actualizar_partido(partido_id: int, data: Dict[str, Any]) -> Partido:
    existente = PartidoRepository.obtener_por_id(partido_id)
    if existente is None:
        raise LookupError(f'Partido con ID {partido_id} no encontrado')

    updated = existente.to_dict()
    updated.update(data)
    partido_actualizado = Partido.from_dict(updated)
    partido_actualizado.id = partido_id

    try:
        PartidoRepository.actualizar(partido_actualizado)
        return partido_actualizado
    except Exception as e:
        raise Exception(f'Error al actualizar partido: {e}')


def eliminar_partido(partido_id: int) -> bool:
    try:
        PartidoRepository.eliminar(partido_id)
        return True
    except Exception as e:
        raise Exception(f'Error al eliminar partido: {e}')
