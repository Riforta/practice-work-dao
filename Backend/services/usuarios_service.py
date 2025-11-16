from typing import List, Dict, Any

from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository
from passlib.hash import pbkdf2_sha256


def crear_usuario(data: Dict[str, Any]) -> Usuario:
    """
    Crea un nuevo usuario con validación mínima y hashing de contraseña.
    Acepta keys flexibles: 'username' o 'nombre_usuario' para el nombre, y 'password' para la contraseña.
    """
    username = data.get('username') or data.get('nombre_usuario') or data.get('nombreUsuario')
    email = data.get('email')
    password = data.get('password') or data.get('password_hash')

    # Require both username and email to match DB constraints (both NOT NULL in schema)
    if not username:
        raise ValueError('Se requiere nombre de usuario (username)')
    if not email:
        raise ValueError('Se requiere email')

    if not password:
        raise ValueError('Se requiere contraseña')

    # validar unicidad
    if username and UsuarioRepository.existe_nombre_usuario(username):
        raise ValueError('El nombre de usuario ya existe')
    if email and UsuarioRepository.existe_email(email):
        raise ValueError('El email ya está registrado')

    # hashear la contraseña (usamos pbkdf2_sha256 para evitar dependencias de bcrypt nativas)
    hashed = pbkdf2_sha256.hash(password)

    usuario = Usuario(
        nombre_usuario=username or '',
        email=email or '',
        password_hash=hashed,
        id_rol=data.get('id_rol'),
        activo=data.get('activo', 1),
    )

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
