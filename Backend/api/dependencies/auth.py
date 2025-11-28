"""Dependencias de FastAPI para autenticación."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from models.usuario import Usuario
from services.auth_service import AuthService
from repositories.rol_repository import RolRepository

# Define el esquema de seguridad Bearer
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Usuario:
    """
    Extrae y valida el token JWT del header Authorization.
    Devuelve el usuario autenticado o lanza HTTPException 401.
    
    Usage:
        @router.get("/protected")
        def endpoint(current_user: Usuario = Depends(get_current_user)):
            return {"user_id": current_user.id}
    """
    token = credentials.credentials
    
    try:
        # Delega la validación al servicio
        usuario = AuthService.validar_token(token)
        return usuario
    
    except ValueError as e:
        # El servicio ya maneja JWT errors y los convierte a ValueError
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error de autenticación: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_active_user(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """
    Compatibilidad: previamente verificaba un flag 'activo'.
    Ya no se usa; se mantiene para compatibilidad y retorna el usuario.
    """
    return current_user


def require_admin(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """
    Verifica que el usuario sea administrador.
    
    Usage:
        @router.delete("/turnos/{id}")
        def eliminar_turno(id: int, admin: Usuario = Depends(require_admin)):
            ...
    """
    # Busca el rol para verificar
    rol = RolRepository.obtener_por_id(current_user.id_rol)
    
    # Verifica si es admin
    if rol and rol.nombre_rol.lower() in ["admin", "administrador"]:
        return current_user
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Se requieren permisos de administrador"
    )


def require_role(rol_descripcion: str):
    """
    Factory de dependencias que verifica un rol específico.
    Los administradores siempre tienen acceso independientemente del rol requerido.
    
    Usage:
        @router.post("/torneos")
        def crear_torneo(user: Usuario = Depends(require_role("Organizador"))):
            ...
    """
    def role_checker(current_user: Usuario = Depends(get_current_user)) -> Usuario:
        rol = RolRepository.obtener_por_id(current_user.id_rol)
        
        if not rol:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere rol: {rol_descripcion}"
            )
        
        # Los administradores tienen acceso a todo
        if rol.nombre_rol.lower() in ["admin", "administrador"]:
            return current_user
        
        # Verificar si tiene el rol específico requerido
        if rol.nombre_rol.lower() != rol_descripcion.lower():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere rol: {rol_descripcion}"
            )
        
        return current_user
    
    return role_checker


def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    )
) -> Optional[Usuario]:
    """
    Intenta obtener el usuario del token, pero no falla si no hay token.
    Útil para endpoints que se comportan diferente con/sin auth.
    
    Returns:
        Usuario si hay token válido, None si no hay token
    """
    if credentials is None:
        return None
    
    try:
        return get_current_user(credentials)
    except HTTPException:
        return None
