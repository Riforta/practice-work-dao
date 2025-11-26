from typing import List, Dict, Any

from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository
from passlib.hash import pbkdf2_sha256


def registrar_usuario(data: Dict[str, Any]) -> Usuario:
    """
    Registra un nuevo usuario en el sistema.
    
    Args:
        data: Diccionario con datos de usuario:
            - nombre_usuario: Nombre de usuario único (mínimo 3 caracteres)
            - email: Email válido y único
            - password: Contraseña en texto plano (mínimo 6 caracteres)
            - id_rol: ID del rol a asignar (opcional, default: 2 = Cliente)
    
    Returns:
        Usuario creado con su ID asignado
    
    Raises:
        ValueError: Si hay errores de validación o datos duplicados
    """
    # Extraer y validar datos
    nombre_usuario = data.get('nombre_usuario')
    email = data.get('email')
    password = data.get('password')
    id_rol = data.get('id_rol', 2)  # Por defecto rol cliente
    
    # Validar campos requeridos
    if not nombre_usuario or len(nombre_usuario) < 3:
        raise ValueError('El nombre de usuario debe tener al menos 3 caracteres')
    if not email or '@' not in email:
        raise ValueError('Email inválido')
    if not password or len(password) < 6:
        raise ValueError('La contraseña debe tener al menos 6 caracteres')
    
    # Verificar unicidad
    if UsuarioRepository.existe_nombre_usuario(nombre_usuario):
        raise ValueError(f'El nombre de usuario "{nombre_usuario}" ya está en uso')
    if UsuarioRepository.existe_email(email):
        raise ValueError(f'El email "{email}" ya está registrado')
    
    # Crear usuario
    hashed = pbkdf2_sha256.hash(password)
    usuario = Usuario(
        nombre_usuario=nombre_usuario,
        email=email,
        password_hash=hashed,
        id_rol=id_rol,
        activo=1,  # Activo al registrarse
    )
    
    try:
        # Guardar usuario
        usuario.id = UsuarioRepository.crear(usuario)
        return usuario
        
    except Exception as e:
        raise Exception(f'Error al registrar usuario: {e}')


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
