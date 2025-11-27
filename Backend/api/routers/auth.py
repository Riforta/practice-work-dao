"""Router de autenticación - Solo define endpoints HTTP."""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict, Any
from services.auth_service import AuthService
from repositories.cliente_repository import ClienteRepository
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
    
    # Genera el token
    token = AuthService.generar_token(user)

    cliente = ClienteRepository.obtener_por_id_usuario(user.id)
    
    # Prepara la respuesta como dict
    return {
        "token": token,
        "user": {
            "id": user.id,
            "nombre_usuario": user.nombre_usuario,
            "email": user.email,
            "id_rol": user.id_rol,
            "id_cliente": cliente.id if cliente else None
        }
    }


# ===== ENDPOINT DE REGISTRO MOVIDO A /api/usuarios/register =====
# El registro de usuarios ahora se maneja en el router de usuarios
# para registrar Usuario + Cliente en una sola operación.
# Ver: api/routers/usuarios.py -> POST /usuarios/register

# @router.post("/register", summary="Registrar nuevo usuario")
# def register(data: Dict[str, Any]):
#     """
#     DEPRECADO: Usar POST /api/usuarios/register en su lugar.
#     
#     Este endpoint registraba solo el Usuario sin crear el perfil de Cliente.
#     Ahora se requiere que todo cliente tenga un Usuario asociado (id_usuario NOT NULL).
#     
#     El nuevo endpoint registra Usuario + Cliente en una sola transacción.
#     """
#     raise HTTPException(
#         status_code=status.HTTP_410_GONE,
#         detail="Este endpoint ha sido movido a POST /api/usuarios/register"
#     )

'''
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
'''
