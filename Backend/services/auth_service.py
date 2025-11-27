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
ACCESS_TOKEN_EXPIRE_MINUTES = 5  # 5 minutos


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
    
    # ===== MÉTODO DE REGISTRO MOVIDO A usuarios_service.py =====
    # El registro de usuarios ahora se maneja en usuarios_service.registrar_usuario_cliente()
    # que registra Usuario + Cliente en una sola transacción.
    # Ver: services/usuarios_service.py -> registrar_usuario_cliente()
    
    # @staticmethod
    # def registrar_usuario(
    #     nombre_usuario: str,
    #     email: str,
    #     password: str,
    #     id_rol: int = 2
    # ) -> Usuario:
    #     """
    #     DEPRECADO: Usar usuarios_service.registrar_usuario_cliente() en su lugar.
    #     
    #     Este método solo registraba el Usuario sin crear el perfil de Cliente.
    #     Ahora se requiere que todo cliente tenga un Usuario asociado.
    #     """
    #     pass