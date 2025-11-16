from typing import List, Dict, Any

from models.pedido import Pedido
from repositories.pedido_repository import PedidoRepository


def crear_pedido(data: Dict[str, Any]) -> Pedido:
    pedido = Pedido.from_dict(data)
    try:
        pedido.id = PedidoRepository.crear(pedido)
        return pedido
    except Exception as e:
        raise Exception(f'Error al crear pedido: {e}')


def obtener_pedido_por_id(pedido_id: int) -> Pedido:
    pedido = PedidoRepository.obtener_por_id(pedido_id)
    if pedido is None:
        raise LookupError(f'Pedido con ID {pedido_id} no encontrado')
    return pedido


def listar_pedidos_por_cliente(cliente_id: int) -> List[Pedido]:
    return PedidoRepository.listar_por_cliente(cliente_id)


def actualizar_pedido(pedido_id: int, data: Dict[str, Any]) -> Pedido:
    existente = PedidoRepository.obtener_por_id(pedido_id)
    if existente is None:
        raise LookupError(f'Pedido con ID {pedido_id} no encontrado')

    updated = existente.to_dict()
    updated.update(data)
    pedido_actualizado = Pedido.from_dict(updated)
    pedido_actualizado.id = pedido_id

    try:
        ok = PedidoRepository.actualizar(pedido_actualizado)
        if not ok:
            raise Exception('No se actualizó el pedido')
        return pedido_actualizado
    except Exception as e:
        raise Exception(f'Error al actualizar pedido: {e}')


def cambiar_estado_pedido(pedido_id: int, nuevo_estado: str) -> bool:
    try:
        return PedidoRepository.cambiar_estado(pedido_id, nuevo_estado)
    except Exception as e:
        raise Exception(f'Error al cambiar estado del pedido: {e}')


def eliminar_pedido(pedido_id: int) -> bool:
    try:
        return PedidoRepository.eliminar(pedido_id)
    except Exception as e:
        raise Exception(f'Error al eliminar pedido: {e}')
