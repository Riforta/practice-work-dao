"""Schemas Pydantic para validación y serialización de datos."""

# Schemas de autenticación
from .auth import (
    LoginRequest,
    RegisterRequest,
    UsuarioResponse,
    LoginResponse,
    RegisterResponse
)

# Schemas de turnos y reservas
from .turnos import (
    TurnoResponse,
    TurnoCreateRequest,
    TurnoUpdateRequest,
    ReservaRequest,
    ReservaModificarRequest,
    ReservaCancelarRequest
)

# Schemas de clientes
from .clientes import (
    ClienteResponse,
    ClienteCreateRequest,
    ClienteUpdateRequest
)

# Schemas de canchas
from .canchas import (
    CanchaResponse,
    CanchaCreateRequest,
    CanchaUpdateRequest
)

__all__ = [
    # Auth
    "LoginRequest",
    "RegisterRequest",
    "UsuarioResponse",
    "LoginResponse",
    "RegisterResponse",
    # Turnos
    "TurnoResponse",
    "TurnoCreateRequest",
    "TurnoUpdateRequest",
    "ReservaRequest",
    "ReservaModificarRequest",
    "ReservaCancelarRequest",
    # Clientes
    "ClienteResponse",
    "ClienteCreateRequest",
    "ClienteUpdateRequest",
    # Canchas
    "CanchaResponse",
    "CanchaCreateRequest",
    "CanchaUpdateRequest",
]
