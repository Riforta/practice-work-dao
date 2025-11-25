"""Servicio de autenticación y manejo de tokens JWT."""

from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.hash import pbkdf2_sha256

from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository

# Configuración JWT (en producción, usar variables de entorno)
SECRET = "dev-secret-key-change-me"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas


class AuthService:
    """Servicio para operaciones de autenticación."""
    
    @staticmethod
    def autenticar_usuario(usuario_field: str, password: str) -> Optional[Usuario]:
        """
        Autentica un usuario con credenciales.
        
        Args:
            usuario_field: Nombre de usuario o email
            password: Contraseña en texto plano
            
        Returns:
            Usuario autenticado o None si las credenciales son inválidas
        """
        # Buscar por nombre de usuario primero, luego por email
        user = UsuarioRepository.obtener_por_nombre_usuario(usuario_field)
        if not user:
            user = UsuarioRepository.obtener_por_email(usuario_field)
        
        if not user:
            return None
        
        # Verificar password
        try:
            password_ok = pbkdf2_sha256.verify(password, user.password_hash)
        except Exception:
            password_ok = False
        
        if not password_ok:
            return None
        
        # Verificar que el usuario esté activo
        if not user.activo:
            return None
        
        return user
    
    @staticmethod
    def generar_token(usuario: Usuario) -> str:
        """
        Genera un token JWT para el usuario.
        
        Args:
            usuario: Usuario autenticado
            
        Returns:
            Token JWT como string
        """
        now = datetime.utcnow()
        payload = {
            "sub": usuario.nombre_usuario,  # Subject (identificador único)
            "user_id": usuario.id,
            "id_rol": usuario.id_rol,
            "iat": now,  # Issued at
            "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),  # Expiration
        }
        token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
        return token
    
    @staticmethod
    def validar_token(token: str) -> Optional[Usuario]:
        """
        Valida un token JWT y devuelve el usuario correspondiente.
        
        Args:
            token: Token JWT a validar
            
        Returns:
            Usuario si el token es válido, None si es inválido o expirado
            
        Raises:
            ValueError: Si el token es inválido con detalle del error
        """
        try:
            payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
            nombre_usuario: str = payload.get("sub")
            
            if nombre_usuario is None:
                raise ValueError("Token inválido: falta 'sub'")
            
            # Buscar el usuario en la BD
            usuario = UsuarioRepository.obtener_por_nombre_usuario(nombre_usuario)
            
            if usuario is None:
                raise ValueError("Usuario no encontrado")
            
            if not usuario.activo:
                raise ValueError("Usuario inactivo")
            
            return usuario
        
        except JWTError as e:
            raise ValueError(f"Token inválido o expirado: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error validando token: {str(e)}")
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashea una contraseña usando pbkdf2_sha256.
        
        Args:
            password: Contraseña en texto plano
            
        Returns:
            Hash de la contraseña
        """
        return pbkdf2_sha256.hash(password)
    
    @staticmethod
    def verificar_password(password: str, password_hash: str) -> bool:
        """
        Verifica que una contraseña coincida con su hash.
        
        Args:
            password: Contraseña en texto plano
            password_hash: Hash almacenado
            
        Returns:
            True si coinciden, False en caso contrario
        """
        try:
            return pbkdf2_sha256.verify(password, password_hash)
        except Exception:
            return False
    
    @staticmethod
    def preparar_usuario_respuesta(usuario: Usuario) -> Dict[str, Any]:
        """
        Prepara un diccionario del usuario para devolver en respuestas.
        Remueve campos sensibles.
        
        Args:
            usuario: Usuario a serializar
            
        Returns:
            Diccionario con datos seguros del usuario
        """
        user_dict = usuario.to_dict()
        # Remover campos sensibles
        user_dict.pop('password_hash', None)
        return user_dict
    
    @staticmethod
    def registrar_usuario(
        nombre_usuario: str,
        email: str,
        password: str,
        id_rol: int = 2  # Por defecto rol 2 (Cliente)
    ) -> Usuario:
        """
        Registra un nuevo usuario en el sistema.
        
        Args:
            nombre_usuario: Nombre de usuario único
            email: Email único
            password: Contraseña en texto plano (será hasheada)
            id_rol: ID del rol a asignar (default 2 = Cliente)
            
        Returns:
            Usuario recién creado
            
        Raises:
            ValueError: Si el email o nombre de usuario ya existen, o si hay errores de validación
        """
        # Validaciones
        if not nombre_usuario or len(nombre_usuario) < 3:
            raise ValueError("El nombre de usuario debe tener al menos 3 caracteres")
        
        if not email or '@' not in email:
            raise ValueError("Email inválido")
        
        if not password or len(password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        
        # Verificar si ya existe
        if UsuarioRepository.existe_nombre_usuario(nombre_usuario):
            raise ValueError(f"El nombre de usuario '{nombre_usuario}' ya está en uso")
        
        if UsuarioRepository.existe_email(email):
            raise ValueError(f"El email '{email}' ya está registrado")
        
        # Crear usuario
        password_hash = AuthService.hash_password(password)
        
        nuevo_usuario = Usuario(
            nombre_usuario=nombre_usuario,
            email=email,
            password_hash=password_hash,
            id_rol=id_rol,
            activo=1  # Por defecto activo al registrarse
        )
        
        # Guardar en BD
        usuario_id = UsuarioRepository.crear(nuevo_usuario)
        nuevo_usuario.id = usuario_id
        
        return nuevo_usuario
    
    @staticmethod
    def marcar_activo(usuario_id: int, activo: bool = True) -> bool:
        """
        Marca un usuario como activo o inactivo.
        
        Args:
            usuario_id: ID del usuario
            activo: True para activar, False para desactivar
            
        Returns:
            True si se actualizó correctamente
        """
        return UsuarioRepository.activar(usuario_id, activo)