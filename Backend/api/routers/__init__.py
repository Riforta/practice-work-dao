"""Routers package for API.

Este paquete agrupa todos los routers de FastAPI y ofrece un
helper `register_routers(app)` para incluirlos de forma centralizada.
"""

from fastapi import FastAPI

# Importamos cada router del paquete
from .auth import router as auth_router
from .canchas import router as canchas_router
from .clientes import router as clientes_router
from .equipos import router as equipos_router
from .equipo_miembros import router as equipo_miembros_router
from .inscripciones import router as inscripciones_router
from .pagos import router as pagos_router
from .partidos import router as partidos_router
from .pedidos import router as pedidos_router
from .roles import router as roles_router
from .servicios_adicionales import router as servicios_adicionales_router
from .torneos import router as torneos_router
from .turnos import router as turnos_router
from .usuarios import router as usuarios_router

__all__ = [
	"auth_router",
	"canchas_router",
	"clientes_router",
	"equipos_router",
	"equipo_miembros_router",
	"inscripciones_router",
	"pagos_router",
	"partidos_router",
	"pedidos_router",
	"roles_router",
	"servicios_adicionales_router",
	"torneos_router",
	"turnos_router",
	"usuarios_router",
	"register_routers",
]


def register_routers(app: FastAPI, prefix: str = "/api") -> None:
	"""Incluye todos los routers en la app.

	Args:
		app: Instancia de FastAPI donde incluir los routers
		prefix: Prefijo opcional para todos los routers (ej: "/api")
	"""
	app.include_router(auth_router, prefix=prefix)
	app.include_router(canchas_router, prefix=prefix)
	app.include_router(clientes_router, prefix=prefix)
	app.include_router(equipos_router, prefix=prefix)
	app.include_router(equipo_miembros_router, prefix=prefix)
	app.include_router(partidos_router, prefix=prefix)
	app.include_router(pedidos_router, prefix=prefix)
	app.include_router(pagos_router, prefix=prefix)
	app.include_router(inscripciones_router, prefix=prefix)
	app.include_router(servicios_adicionales_router, prefix=prefix)
	app.include_router(torneos_router, prefix=prefix)
	app.include_router(roles_router, prefix=prefix)
	app.include_router(usuarios_router, prefix=prefix)
	app.include_router(turnos_router, prefix=prefix)
