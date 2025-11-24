"""Schemas Pydantic para autenticación."""

from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional


# ===== Request Schemas =====

class LoginRequest(BaseModel):
    """Schema para login de usuario."""
    usuario: str = Field(..., min_length=3, description="Nombre de usuario o email")
    password: str = Field(..., min_length=6, description="Contraseña")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "usuario": "admin",
                "password": "admin123"
            }
        }
    )


class RegisterRequest(BaseModel):
    """Schema para registro de usuario."""
    nombre_usuario: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario único")
    email: EmailStr = Field(..., description="Email válido")
    password: str = Field(..., min_length=6, description="Contraseña (mínimo 6 caracteres)")
    id_rol: Optional[int] = Field(default=2, description="ID del rol (default: 2 = Cliente)")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre_usuario": "juanperez",
                "email": "juan@example.com",
                "password": "password123",
                "id_rol": 2
            }
        }
    )


# ===== Response Schemas =====

class UsuarioResponse(BaseModel):
    """Schema para datos de usuario en respuestas (sin password_hash)."""
    id: int
    nombre_usuario: str
    email: str
    id_rol: int
    activo: int
    
    model_config = ConfigDict(from_attributes=True)


class LoginResponse(BaseModel):
    """Schema para respuesta de login."""
    token: str
    user: UsuarioResponse


class RegisterResponse(BaseModel):
    """Schema para respuesta de registro."""
    token: str
    user: UsuarioResponse
    message: str
