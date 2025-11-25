"""Dependencias reutilizables de FastAPI."""

from .auth import (
    get_current_user,
    get_current_active_user,
    require_admin,
    require_role,
    get_current_user_optional
)

__all__ = [
    "get_current_user",
    "get_current_active_user", 
    "require_admin",
    "require_role",
    "get_current_user_optional"
]
