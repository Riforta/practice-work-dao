from typing import List, Dict, Any

from models.equipo import Equipo
from repository.equipo_repository import EquipoRepository


def crear_equipo(data: Dict[str, Any]) -> Equipo:
    if not data.get('nombre_equipo'):
        raise ValueError('El nombre del equipo es obligatorio')

    equipo = Equipo.from_dict(data)
    try:
        equipo.id = EquipoRepository.crear(equipo)
        return equipo
    except Exception as e:
        raise Exception(f'Error al crear equipo: {e}')


def obtener_equipo_por_id(equipo_id: int) -> Equipo:
    equipo = EquipoRepository.obtener_por_id(equipo_id)
    if equipo is None:
        raise LookupError(f'Equipo con ID {equipo_id} no encontrado')
    return equipo


def listar_equipos() -> List[Equipo]:
    return EquipoRepository.obtener_todos()


def buscar_equipos(nombre: str) -> List[Equipo]:
    if not nombre:
        return []
    return EquipoRepository.buscar_por_nombre(nombre)


def actualizar_equipo(equipo_id: int, data: Dict[str, Any]) -> Equipo:
    existente = EquipoRepository.obtener_por_id(equipo_id)
    if existente is None:
        raise LookupError(f'Equipo con ID {equipo_id} no encontrado')

    updated = existente.to_dict()
    updated.update(data)
    equipo_actualizado = Equipo.from_dict(updated)
    equipo_actualizado.id = equipo_id

    try:
        ok = EquipoRepository.actualizar(equipo_actualizado)
        if not ok:
            raise Exception('No se actualizó el equipo')
        return equipo_actualizado
    except Exception as e:
        raise Exception(f'Error al actualizar equipo: {e}')


def eliminar_equipo(equipo_id: int) -> bool:
    try:
        return EquipoRepository.eliminar(equipo_id)
    except Exception as e:
        raise Exception(f'Error al eliminar equipo: {e}')
