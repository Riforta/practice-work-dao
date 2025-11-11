from typing import List, Dict, Any

from models.usuario import Usuario
from repository.usuario_repository import UsuarioRepository


def crear_usuario(data: Dict[str, Any]) -> Usuario:
    if not data.get('username') and not data.get('email'):
        raise ValueError('Se requiere username o email para crear un usuario')

    usuario = Usuario.from_dict(data)
    try:
        usuario.id = UsuarioRepository.crear(usuario)
        return usuario
    except Exception as e:
        raise Exception(f'Error al crear usuario: {e}')


def obtener_usuario_por_id(usuario_id: int) -> Usuario:
    usuario = UsuarioRepository.obtener_por_id(usuario_id)
    if usuario is None:
        raise LookupError(f'Usuario con ID {usuario_id} no encontrado')
    return usuario


def listar_usuarios() -> List[Usuario]:
    return UsuarioRepository.obtener_todos()


def actualizar_usuario(usuario_id: int, data: Dict[str, Any]) -> Usuario:
    existente = UsuarioRepository.obtener_por_id(usuario_id)
    if existente is None:
        raise LookupError(f'Usuario con ID {usuario_id} no encontrado')

    updated = existente.to_dict()
    updated.update(data)
    usuario_actualizado = Usuario.from_dict(updated)
    usuario_actualizado.id = usuario_id

    try:
        ok = UsuarioRepository.actualizar(usuario_actualizado)
        if not ok:
            raise Exception('No se actualizó el usuario')
        return usuario_actualizado
    except Exception as e:
        raise Exception(f'Error al actualizar usuario: {e}')


def eliminar_usuario(usuario_id: int) -> bool:
    try:
        return UsuarioRepository.eliminar(usuario_id)
    except Exception as e:
        raise Exception(f'Error al eliminar usuario: {e}')
