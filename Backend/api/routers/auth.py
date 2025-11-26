"""Router de autenticación - Solo define endpoints HTTP."""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict, Any
from services.auth_service import AuthService
from api.dependencies.auth import get_current_user
from models.usuario import Usuario

router = APIRouter()


# ===== Endpoints =====

@router.post("/login", summary="Login de usuario")
def login(credentials: Dict[str, Any]):
    """
    Autentica un usuario y devuelve un token JWT.
    Al hacer login, el usuario se marca como activo.
    
    - **usuario**: Nombre de usuario o email
    - **password**: Contraseña del usuario
    
    Returns:
        - **token**: Token JWT para usar en endpoints protegidos
        - **user**: Datos básicos del usuario (sin password)
    """
    # Delega la lógica al servicio
    user = AuthService.autenticar_usuario(
        usuario_field=credentials.get("usuario"),
        password=credentials.get("password")
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    # Marcar usuario como activo al hacer login
    AuthService.marcar_activo(user.id, activo=True)
    user.activo = 1  # Actualizar objeto en memoria
    
    # Genera el token
    token = AuthService.generar_token(user)
    
    # Prepara la respuesta como dict
    return {
        "token": token,
        "user": {
            "id": user.id,
            "nombre_usuario": user.nombre_usuario,
            "email": user.email,
            "id_rol": user.id_rol,
            "activo": user.activo,
            "fecha_creacion": user.fecha_creacion
        }
    }


@router.post("/register", summary="Registrar nuevo usuario")
def register(data: Dict[str, Any]):
    """
    Registra un nuevo usuario en el sistema y devuelve un token JWT.
    
    - **nombre_usuario**: Nombre de usuario único (mínimo 3 caracteres)
    - **email**: Email válido y único
    - **password**: Contraseña (mínimo 6 caracteres)
    - **id_rol**: ID del rol a asignar (default: 2 = Cliente)
    
    Returns:
        - **token**: Token JWT para usar inmediatamente
        - **user**: Datos básicos del usuario creado
        - **message**: Mensaje de confirmación
    """
    try:
        # Delega la lógica al servicio
        nuevo_usuario = AuthService.registrar_usuario(
            nombre_usuario=data.get("nombre_usuario"),
            email=data.get("email"),
            password=data.get("password"),
            id_rol=data.get("id_rol", 2)
        )
        
        # Genera el token automáticamente
        token = AuthService.generar_token(nuevo_usuario)
        
        # Prepara la respuesta como dict
        return {
            "token": token,
            "user": {
                "id": nuevo_usuario.id,
                "nombre_usuario": nuevo_usuario.nombre_usuario,
                "email": nuevo_usuario.email,
                "id_rol": nuevo_usuario.id_rol,
                "activo": nuevo_usuario.activo,
                "fecha_creacion": nuevo_usuario.fecha_creacion
            },
            "message": "Usuario registrado exitosamente"
        }
    
    except ValueError as e:
        # Errores de validación o duplicados
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Otros errores
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar usuario: {str(e)}"
        )


@router.post("/logout", summary="Cerrar sesión")
def logout(current_user: Usuario = Depends(get_current_user)):
    """
    Cierra la sesión del usuario marcándolo como inactivo.
    Requiere autenticación (token JWT en header Authorization).
    
    Returns:
        Mensaje de confirmación
    """
    try:
        # Marcar usuario como inactivo
        AuthService.marcar_activo(current_user.id, activo=False)
        
        return {
            "message": "Sesión cerrada exitosamente",
            "usuario": current_user.nombre_usuario
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cerrar sesión: {str(e)}"
        )


@router.post("/refresh", summary="Refrescar token")
def refresh_token(payload: Dict[str, Any]):
    """
    Refresca un token JWT expirado usando un refresh token.
    
    TODO: Implementar lógica de refresh tokens
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Endpoint de refresh aún no implementado"
    )
