"""Services package.

Provee importación perezosa (lazy) de submódulos para evitar dependencias
innecesarias en tiempo de importación. Permite expresiones como:
`from services import turnos_services`.
"""

from importlib import import_module
from typing import Any

__all__ = [
    "auth_service",
    "canchas_service",
    "clientes_service",
    "equipo_miembros_service",
    "equipos_service",
    "inscripciones_service",
    "pagos_service",
    "partidos_service",
    "pedidos_service",
    "reservas_service",
    "roles_service",
    "servicios_adicionales_service",
    "tarifas_service",
    "torneos_service",
    "turno_servicios_service",
    "turnos_service",
    "usuarios_service",
]


def __getattr__(name: str) -> Any:
    """Carga perezosa de submódulos bajo `services`.

    Evita importar todos los módulos y sus dependencias al cargar el paquete.
    """
    if name in __all__:
        return import_module(f"{__name__}.{name}")
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
