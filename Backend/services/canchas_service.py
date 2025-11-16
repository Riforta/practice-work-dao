from typing import List, Dict, Any

from models.cancha import Cancha
from repositories.cancha_repository import CanchaRepository


def crear_cancha(data: Dict[str, Any]) -> Cancha:
    if not data.get('nombre'):
        raise ValueError('El nombre de la cancha es obligatorio')

    cancha = Cancha.from_dict(data)
    try:
        cancha.id = CanchaRepository.crear(cancha)
        return cancha
    except Exception as e:
        raise Exception(f'Error al crear cancha: {e}')


def obtener_cancha_por_id(cancha_id: int) -> Cancha:
    cancha = CanchaRepository.obtener_por_id(cancha_id)
    if cancha is None:
        raise LookupError(f'Cancha con ID {cancha_id} no encontrada')
    return cancha


def listar_canchas() -> List[Cancha]:
    return CanchaRepository.listar_todas()


def actualizar_cancha(cancha_id: int, data: Dict[str, Any]) -> Cancha:
    existente = CanchaRepository.obtener_por_id(cancha_id)
    if existente is None:
        raise LookupError(f'Cancha con ID {cancha_id} no encontrada')

    updated = existente.to_dict()
    updated.update(data)
    cancha_actualizada = Cancha.from_dict(updated)
    cancha_actualizada.id = cancha_id

    try:
        CanchaRepository.actualizar(cancha_actualizada)
        return cancha_actualizada
    except Exception as e:
        raise Exception(f'Error al actualizar cancha: {e}')


def eliminar_cancha(cancha_id: int) -> bool:
    try:
        CanchaRepository.eliminar(cancha_id)
        return True
    except Exception as e:
        raise Exception(f'Error al eliminar cancha: {e}')
