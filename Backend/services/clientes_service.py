"""Servicios para la entidad Cliente.

Este módulo implementa la capa de servicios que orquesta validaciones y
llama al repositorio (`repository/cliente_repository.py`).

Funciones públicas (API):
 - crear_cliente(data: dict) -> Cliente
 - obtener_cliente_por_id(cliente_id: int) -> Cliente
 - listar_clientes() -> list[Cliente]
 - buscar_clientes_por_nombre(nombre: str) -> list[Cliente]
 - actualizar_cliente(cliente_id: int, data: dict) -> Cliente
 - eliminar_cliente(cliente_id: int) -> bool

Las funciones devuelven instancias de `models.cliente.Cliente` o lanzan
excepciones (`ValueError` para validaciones, `LookupError` para no encontrado,
`Exception` para errores de persistencia).
"""

from typing import List, Optional, Dict, Any

from services import roles_service
from services import usuarios_service
from models.cliente import Cliente
from repositories.cliente_repository import ClienteRepository


def _validar_datos_cliente(data: Dict[str, Any], para_actualizar: bool = False, skip_rol_validation: bool = False) -> None:
	"""Valida los campos mínimos para crear/actualizar un cliente.

	Lanza ValueError en caso de datos inválidos.
	
	Args:
		data: Datos del cliente a validar
		para_actualizar: Si es True, solo valida campos provistos
		skip_rol_validation: Si es True, omite validación de rol (usado en registro de usuario)
	"""
	nombre = data.get('nombre')
	apellido = data.get('apellido')
	telefono = data.get('telefono')
	dni = data.get('dni')
	id_usuario = data.get('id_usuario')

	if not para_actualizar:
		# En creación, nombre, apellido, teléfono y dni son obligatorios
		if not nombre or not str(nombre).strip():
			raise ValueError("El nombre es obligatorio")
		if not apellido or not str(apellido).strip():
			raise ValueError("El apellido es obligatorio")
		if not telefono or not str(telefono).strip():
			raise ValueError("El teléfono es obligatorio")
		if not dni or not str(dni).strip():
			raise ValueError("El DNI es obligatorio")

		# id_usuario es OPCIONAL. Si se provee, validar su existencia y rol
		if id_usuario is not None:
			try:
				usuario = usuarios_service.obtener_usuario_por_id(int(id_usuario))
			except Exception:
				raise ValueError("El usuario vinculado no existe")
			
			# Validar rol 'cliente' SOLO si NO estamos en registro de usuario
			# (skip_rol_validation se usa cuando usuario y cliente se crean juntos)
			if not skip_rol_validation and usuario is not None:
				rol = roles_service.obtener_rol_por_id(usuario.id_rol)
				if rol and getattr(rol, 'nombre', getattr(rol, 'nombre_rol', '')).lower() != 'cliente':
					raise ValueError("El usuario vinculado debe tener rol 'cliente'")
			
			# Evitar duplicar vínculo si ese usuario ya tiene cliente
			existente = ClienteRepository.obtener_por_id_usuario(int(id_usuario))
			if existente is not None:
				raise ValueError("El usuario ya está vinculado a un cliente")
	else:
		# En actualización, si se suministran campos requeridos, validar que no sean vacíos
		if 'nombre' in data and (not data.get('nombre') or not str(data.get('nombre')).strip()):
			raise ValueError("El nombre no puede estar vacío si se proporciona")
		if 'apellido' in data and (not data.get('apellido') or not str(data.get('apellido')).strip()):
			raise ValueError("El apellido no puede estar vacío si se proporciona")
		if 'telefono' in data and (not data.get('telefono') or not str(data.get('telefono')).strip()):
			raise ValueError("El teléfono no puede estar vacío si se proporciona")
		# Si se desea vincular o cambiar 'id_usuario' en actualización
		if 'id_usuario' in data and data.get('id_usuario') is not None:
			try:
				usuario = usuarios_service.obtener_usuario_por_id(int(data.get('id_usuario')))
			except Exception:
				raise ValueError("El usuario vinculado no existe")
			rol = roles_service.obtener_rol_por_id(usuario.id_rol)
			if rol and getattr(rol, 'nombre', getattr(rol, 'nombre_rol', '')).lower() != 'cliente':
				raise ValueError("El usuario vinculado debe tener rol 'cliente'")
			# Evitar duplicar vínculo (excepto si es el mismo cliente)
			existente = ClienteRepository.obtener_por_id_usuario(int(data.get('id_usuario')))
			if existente is not None and existente.id != data.get('cliente_id_actual'):
				raise ValueError("El usuario ya está vinculado a otro cliente")


def crear_cliente(data: Dict[str, Any], skip_rol_validation: bool = False) -> Cliente:
	"""Crea un cliente luego de validar y verificar unicidad de DNI.

	Devuelve la instancia creada con su `id`.
	
	Args:
		data: Datos del cliente
		skip_rol_validation: Si es True, omite validación de rol (usado en registro usuario+cliente)
	"""
	_validar_datos_cliente(data, para_actualizar=False, skip_rol_validation=skip_rol_validation)

	dni = data.get('dni')
	if dni and ClienteRepository.existe_dni(dni):
		raise ValueError(f"Ya existe un cliente con DNI {dni}")

	cliente = Cliente.from_dict(data)
	try:
		nuevo_id = ClienteRepository.crear(cliente)
		cliente.id = nuevo_id
		return cliente
	except Exception as e:
		raise Exception(f"Error al crear cliente: {e}")


def obtener_cliente_por_id(cliente_id: int) -> Cliente:
	"""Devuelve un cliente por ID o lanza LookupError si no existe."""
	cliente = ClienteRepository.obtener_por_id(cliente_id)
	if cliente is None:
		raise LookupError(f"Cliente con ID {cliente_id} no encontrado")
	return cliente


def listar_clientes() -> List[Cliente]:
	"""Obtiene todos los clientes ordenados por nombre/apellido."""
	return ClienteRepository.obtener_todos()


def buscar_clientes_por_nombre(nombre: str) -> List[Cliente]:
	"""Busca clientes por nombre o apellido (coincidencia parcial)."""
	if not nombre:
		return []
	return ClienteRepository.buscar_por_nombre(nombre)


def actualizar_cliente(cliente_id: int, data: Dict[str, Any]) -> Cliente:
	"""Actualiza un cliente existente.

	- Valida campos si fueron provistos
	- Verifica unicidad de dni si se actualiza
	- Lanza LookupError si el cliente no existe
	- Devuelve la instancia actualizada
	"""
	if not data:
		raise ValueError("No hay datos para actualizar")

	# Asegurar que el cliente exista
	existente = ClienteRepository.obtener_por_id(cliente_id)
	if existente is None:
		raise LookupError(f"Cliente con ID {cliente_id} no encontrado")

	# Agregar cliente_id_actual para validar duplicado de id_usuario
	data['cliente_id_actual'] = cliente_id
	_validar_datos_cliente(data, para_actualizar=True)

	# Si se provee dni, verificar que no exista en otro cliente
	if 'dni' in data and data.get('dni'):
		if ClienteRepository.existe_dni(data.get('dni'), excluir_id=cliente_id):
			raise ValueError(f"Otro cliente ya tiene el DNI {data.get('dni')}")

	# Mezclar datos y persistir
	updated = existente.to_dict()
	updated.update(data)
	cliente_actualizado = Cliente.from_dict(updated)
	cliente_actualizado.id = cliente_id

	try:
		ok = ClienteRepository.actualizar(cliente_actualizado)
		if not ok:
			raise Exception("La actualización no modificó filas (cliente no encontrado al actualizar)")
		return cliente_actualizado
	except Exception as e:
		raise Exception(f"Error al actualizar cliente: {e}")


def eliminar_cliente(cliente_id: int) -> bool:
	"""Elimina un cliente por su ID. Devuelve True si se eliminó."""
	try:
		eliminado = ClienteRepository.eliminar(cliente_id)
		if not eliminado:
			raise LookupError(f"Cliente con ID {cliente_id} no encontrado para eliminar")
		return True
	except LookupError:
		raise
	except Exception as e:
		raise Exception(f"Error al eliminar cliente: {e}")
