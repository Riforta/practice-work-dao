"""Paquete de capas CRUD.

Expone funciones de acceso a datos por entidad.
"""

# Repository package
from .cliente_repository import ClienteRepository

__all__ = ['ClienteRepository']
