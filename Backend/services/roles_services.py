from typing import List, Dict, Any

from models.rol import Rol
from repository.rol_repository import RolRepository


def crear_rol(data: Dict[str, Any]) -> Rol:
    if not data.get('nombre_rol'):
        raise ValueError('El nombre del rol es obligatorio')

    rol = Rol.from_dict(data)
    try:
        rol.id = RolRepository.crear(rol)
        return rol
    except Exception as e:
        raise Exception(f'Error al crear rol: {e}')


def obtener_rol_por_id(rol_id: int) -> Rol:
    rol = RolRepository.obtener_por_id(rol_id)
    if rol is None:
        raise LookupError(f'Rol con ID {rol_id} no encontrado')
    return rol


def listar_roles() -> List[Rol]:
    return RolRepository.obtener_todos()


def actualizar_rol(rol_id: int, data: Dict[str, Any]) -> Rol:
    existente = RolRepository.obtener_por_id(rol_id)
    if existente is None:
        raise LookupError(f'Rol con ID {rol_id} no encontrado')

    updated = existente.to_dict()
    updated.update(data)
    rol_actualizado = Rol.from_dict(updated)
    rol_actualizado.id = rol_id

    try:
        ok = RolRepository.actualizar(rol_actualizado)
        if not ok:
            raise Exception('No se actualizó el rol')
        return rol_actualizado
    except Exception as e:
        raise Exception(f'Error al actualizar rol: {e}')


def eliminar_rol(rol_id: int) -> bool:
    try:
        return RolRepository.eliminar(rol_id)
    except Exception as e:
        raise Exception(f'Error al eliminar rol: {e}')
