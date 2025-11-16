from typing import List, Dict, Any

from models.pago import Pago
from repositories.pago_repository import PagoRepository


def crear_pago(data: Dict[str, Any]) -> Pago:
    pago = Pago.from_dict(data)
    try:
        pago.id = PagoRepository.crear(pago)
        return pago
    except Exception as e:
        raise Exception(f'Error al crear pago: {e}')


def obtener_pago_por_id(pago_id: int) -> Pago:
    pago = PagoRepository.obtener_por_id(pago_id)
    if pago is None:
        raise LookupError(f'Pago con ID {pago_id} no encontrado')
    return pago


def listar_pagos_por_pedido(pedido_id: int) -> List[Pago]:
    return PagoRepository.listar_por_pedido(pedido_id)


def actualizar_pago(pago_id: int, data: Dict[str, Any]) -> Pago:
    existente = PagoRepository.obtener_por_id(pago_id)
    if existente is None:
        raise LookupError(f'Pago con ID {pago_id} no encontrado')

    updated = existente.to_dict()
    updated.update(data)
    pago_actualizado = Pago.from_dict(updated)
    pago_actualizado.id = pago_id

    try:
        ok = PagoRepository.actualizar(pago_actualizado)
        if not ok:
            raise Exception('No se actualizó el pago')
        return pago_actualizado
    except Exception as e:
        raise Exception(f'Error al actualizar pago: {e}')


def cambiar_estado_pago(pago_id: int, nuevo_estado: str) -> bool:
    try:
        return PagoRepository.cambiar_estado(pago_id, nuevo_estado)
    except Exception as e:
        raise Exception(f'Error al cambiar estado del pago: {e}')


def eliminar_pago(pago_id: int) -> bool:
    try:
        return PagoRepository.eliminar(pago_id)
    except Exception as e:
        raise Exception(f'Error al eliminar pago: {e}')
