"""Paquete de capas CRUD.

Expone funciones de acceso a datos por entidad.
"""

# Repository package: re-export repository classes to simplify imports.
# Import each repository from its module (avoid importing the wrong symbol).
from .cliente_repository import ClienteRepository
from .cancha_repository import CanchaRepository
from .servicio_adicional_repository import ServicioAdicionalRepository
from .usuario_repository import UsuarioRepository
from .torneo_repository import TorneoRepository
from .equipo_repository import EquipoRepository
from .tarifa_repository import TarifaRepository
from .partido_repository import PartidoRepository

__all__ = [
	'ClienteRepository',
	'CanchaRepository',
    'EquipoRepository',
    'ServicioAdicionalRepository',
    'UsuarioRepository',
    'TorneoRepository',
    'TarifaRepository',
    'PartidoRepository',
]
