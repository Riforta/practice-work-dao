from typing import List, Dict, Any, Optional

from models.tarifa import Tarifa
from repository.tarifa_repository import TarifaRepository


def crear_tarifa(data: Dict[str, Any]) -> Tarifa:
    if not data.get('nombre'):
        raise ValueError('El nombre de la tarifa es obligatorio')

    tarifa = Tarifa.from_dict(data)
    try:
        tarifa.id = TarifaRepository.crear(tarifa)
        return tarifa
    except Exception as e:
        raise Exception(f'Error al crear tarifa: {e}')


def obtener_tarifa_por_id(tarifa_id: int) -> Tarifa:
    tarifa = TarifaRepository.obtener_por_id(tarifa_id)
    if tarifa is None:
        raise LookupError(f'Tarifa con ID {tarifa_id} no encontrada')
    return tarifa


def listar_tarifas() -> List[Tarifa]:
    return TarifaRepository.obtener_todas()


def actualizar_tarifa(tarifa_id: int, data: Dict[str, Any]) -> Tarifa:
    existente = TarifaRepository.obtener_por_id(tarifa_id)
    if existente is None:
        raise LookupError(f'Tarifa con ID {tarifa_id} no encontrada')

    updated = existente.to_dict()
    updated.update(data)
    tarifa_actualizada = Tarifa.from_dict(updated)
    tarifa_actualizada.id = tarifa_id

    try:
        ok = TarifaRepository.actualizar(tarifa_actualizada)
        if not ok:
            raise Exception('No se actualizó la tarifa')
        return tarifa_actualizada
    except Exception as e:
        raise Exception(f'Error al actualizar tarifa: {e}')


def eliminar_tarifa(tarifa_id: int) -> bool:
    try:
        return TarifaRepository.eliminar(tarifa_id)
    except Exception as e:
        raise Exception(f'Error al eliminar tarifa: {e}')
