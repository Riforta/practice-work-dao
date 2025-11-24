"""Router de autenticación - Solo define endpoints HTTP."""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict, Any
from api.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    UsuarioResponse,
    LoginResponse,
    RegisterResponse
)
from services.auth_service import AuthService
from api.dependencies.auth import get_current_user
from models.usuario import Usuario

router = APIRouter()


# ===== Endpoints =====

@router.post("/login", response_model=LoginResponse, summary="Login de usuario")
def login(credentials: LoginRequest):
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
        usuario_field=credentials.usuario,
        password=credentials.password
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
    
    # Prepara la respuesta usando schema Pydantic
    return LoginResponse(
        token=token,
        user=UsuarioResponse.model_validate(user)
    )


@router.post("/register", response_model=RegisterResponse, summary="Registrar nuevo usuario")
def register(data: RegisterRequest):
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
            nombre_usuario=data.nombre_usuario,
            email=data.email,
            password=data.password,
            id_rol=data.id_rol
        )
        
        # Genera el token automáticamente
        token = AuthService.generar_token(nuevo_usuario)
        
        # Prepara la respuesta usando schema Pydantic
        return RegisterResponse(
            token=token,
            user=UsuarioResponse.model_validate(nuevo_usuario),
            message="Usuario registrado exitosamente"
        )
    
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
