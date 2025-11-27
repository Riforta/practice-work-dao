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
from .partido_repository import PartidoRepository
from .equipo_miembro_repository import EquipoMiembroRepository
from .inscripcion_repository import InscripcionRepository
from .pago_repository import PagoRepository
from .rol_repository import RolRepository
from .turno_repository import TurnoRepository
from .turno_servicio_repository import TurnoXServicioRepository
from .tarifa_repository import TarifaRepository

__all__ = [
	'ClienteRepository',
	'CanchaRepository',
    'EquipoRepository',
    'ServicioAdicionalRepository',
    'UsuarioRepository',
    'TorneoRepository',
    'PartidoRepository',
    'EquipoMiembroRepository',
    'InscripcionRepository',
    'PagoRepository',
    'RolRepository',
    'TurnoRepository',
    'TurnoXServicioRepository',
    'TarifaRepository',
]
