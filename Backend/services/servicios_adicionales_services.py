from typing import List, Dict, Any, Optional

from models.servicio_adicional import ServicioAdicional
from repository.servicio_adicional_repository import ServicioAdicionalRepository


def crear_servicio(data: Dict[str, Any]) -> ServicioAdicional:
    if not data.get('nombre'):
        raise ValueError('El nombre del servicio es obligatorio')

    servicio = ServicioAdicional.from_dict(data)
    if ServicioAdicionalRepository.existe_nombre(servicio.nombre):
        raise ValueError(f'Ya existe un servicio con nombre {servicio.nombre}')

    try:
        servicio.id = ServicioAdicionalRepository.crear(servicio)
        return servicio
    except Exception as e:
        raise Exception(f'Error al crear servicio adicional: {e}')


def obtener_servicio_por_id(servicio_id: int) -> ServicioAdicional:
    servicio = ServicioAdicionalRepository.obtener_por_id(servicio_id)
    if servicio is None:
        raise LookupError(f'Servicio con ID {servicio_id} no encontrado')
    return servicio


def listar_servicios(activos: Optional[bool] = None) -> List[ServicioAdicional]:
    return ServicioAdicionalRepository.obtener_todos(activos=activos)


def buscar_servicios(nombre: str) -> List[ServicioAdicional]:
    if not nombre:
        return []
    return ServicioAdicionalRepository.buscar_por_nombre(nombre)


def actualizar_servicio(servicio_id: int, data: Dict[str, Any]) -> ServicioAdicional:
    existente = ServicioAdicionalRepository.obtener_por_id(servicio_id)
    if existente is None:
        raise LookupError(f'Servicio con ID {servicio_id} no encontrado')

    if 'nombre' in data and ServicioAdicionalRepository.existe_nombre(data['nombre'], excluir_id=servicio_id):
        raise ValueError(f'Otro servicio ya tiene el nombre {data["nombre"]}')

    updated = existente.to_dict()
    updated.update(data)
    servicio_actualizado = ServicioAdicional.from_dict(updated)
    servicio_actualizado.id = servicio_id

    try:
        ok = ServicioAdicionalRepository.actualizar(servicio_actualizado)
        if not ok:
            raise Exception('No se actualizó el servicio')
        return servicio_actualizado
    except Exception as e:
        raise Exception(f'Error al actualizar servicio: {e}')


def eliminar_servicio(servicio_id: int) -> bool:
    try:
        return ServicioAdicionalRepository.eliminar(servicio_id)
    except Exception as e:
        raise Exception(f'Error al eliminar servicio: {e}')
