"""Servicios para la entidad Turno (Reservas/Turnos de canchas).

Este módulo implementa la lógica de negocio para gestionar turnos/reservas.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from models.turno import Turno
from repositories.turno_repository import TurnoRepository
from repositories.turno_servicio_repository import TurnoXServicioRepository


def _validar_datos_turno(data: Dict[str, Any], para_actualizar: bool = False) -> None:
    """Valida los campos para crear/actualizar un turno."""
    if not para_actualizar:
        if not data.get('id_cancha'):
            raise ValueError("El campo 'id_cancha' es requerido")
        if not data.get('fecha_hora_inicio'):
            raise ValueError("El campo 'fecha_hora_inicio' es requerido")
        if not data.get('fecha_hora_fin'):
            raise ValueError("El campo 'fecha_hora_fin' es requerido")
    
    # Validar que fecha_fin sea posterior a fecha_inicio
    if data.get('fecha_hora_inicio') and data.get('fecha_hora_fin'):
        if data['fecha_hora_inicio'] >= data['fecha_hora_fin']:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio")


def crear_turno(data: Dict[str, Any]) -> Turno:
    """Crea un nuevo turno/reserva.
    
    Args:
        data: Diccionario con datos del turno
        
    Returns:
        Instancia de Turno creado
    """
    _validar_datos_turno(data)
    
    turno = Turno(
        id_cancha=data['id_cancha'],
        fecha_hora_inicio=data['fecha_hora_inicio'],
        fecha_hora_fin=data['fecha_hora_fin'],
        estado=data.get('estado', 'disponible'),
        precio_final=data.get('precio_final', 0.0),
        id_cliente=data.get('id_cliente'),
        id_usuario_registro=data.get('id_usuario_registro'),
        reserva_created_at=data.get('reserva_created_at'),
        id_usuario_bloqueo=data.get('id_usuario_bloqueo'),
        motivo_bloqueo=data.get('motivo_bloqueo'),
    )
    
    turno_id = TurnoRepository.crear(turno)
    turno.id = turno_id
    return turno


def obtener_turno_por_id(turno_id: int) -> Turno:
    """Obtiene un turno por su ID.
    
    Args:
        turno_id: ID del turno
        
    Returns:
        Instancia de Turno
        
    Raises:
        LookupError: Si el turno no existe
    """
    turno = TurnoRepository.obtener_por_id(turno_id)
    if not turno:
        raise LookupError(f"Turno con ID {turno_id} no encontrado")
    return turno


def listar_turnos() -> List[Turno]:
    """Lista todos los turnos."""
    return TurnoRepository.obtener_todos_filtrados()


def listar_turnos_por_cancha(id_cancha: int) -> List[Turno]:
    """Lista turnos de una cancha específica."""
    return TurnoRepository.obtener_por_cancha(id_cancha)


def listar_turnos_por_cliente(id_cliente: int) -> List[Turno]:
    """Lista turnos de un cliente específico."""
    return TurnoRepository.obtener_por_cliente(id_cliente)


def listar_turnos_por_estado(estado: str) -> List[Turno]:
    """Lista turnos por estado."""
    return TurnoRepository.obtener_todos_filtrados(estado=estado)


def buscar_disponibles(id_cancha: int, fecha_inicio: str, fecha_fin: str) -> List[Turno]:
    """Busca turnos disponibles en un rango de fechas."""
    # Filtrar por cancha y estado disponible, luego filtrar por fechas
    turnos = TurnoRepository.obtener_por_cancha(id_cancha, estado='disponible')
    # Filtrar por rango de fechas (simplificado)
    return [t for t in turnos if fecha_inicio <= t.fecha_hora_inicio <= fecha_fin]


def actualizar_turno(turno_id: int, data: Dict[str, Any]) -> Turno:
    """Actualiza un turno existente.
    
    Args:
        turno_id: ID del turno a actualizar
        data: Datos a actualizar
        
    Returns:
        Instancia de Turno actualizado
    """
    _validar_datos_turno(data, para_actualizar=True)
    
    turno = obtener_turno_por_id(turno_id)
    
    # Actualizar campos
    if 'id_cancha' in data:
        turno.id_cancha = data['id_cancha']
    if 'fecha_hora_inicio' in data:
        turno.fecha_hora_inicio = data['fecha_hora_inicio']
    if 'fecha_hora_fin' in data:
        turno.fecha_hora_fin = data['fecha_hora_fin']
    if 'estado' in data:
        turno.estado = data['estado']
    if 'precio_final' in data:
        turno.precio_final = data['precio_final']
    if 'id_cliente' in data:
        turno.id_cliente = data['id_cliente']
    if 'id_usuario_registro' in data:
        turno.id_usuario_registro = data['id_usuario_registro']
    if 'reserva_created_at' in data:
        turno.reserva_created_at = data['reserva_created_at']
    if 'id_usuario_bloqueo' in data:
        turno.id_usuario_bloqueo = data['id_usuario_bloqueo']
    if 'motivo_bloqueo' in data:
        turno.motivo_bloqueo = data['motivo_bloqueo']
    
    success = TurnoRepository.actualizar(turno)
    if not success:
        raise Exception("No se pudo actualizar el turno")
    
    return turno


def cambiar_estado_turno(turno_id: int, nuevo_estado: str) -> bool:
    """Cambia el estado de un turno.
    
    Args:
        turno_id: ID del turno
        nuevo_estado: Nuevo estado
        
    Returns:
        True si se actualizó correctamente
    """
    # Validar que el turno exista
    obtener_turno_por_id(turno_id)
    
    # Validar estados permitidos
    estados_validos = ['disponible', 'reservado', 'bloqueado', 'cancelado', 'finalizado']
    if nuevo_estado not in estados_validos:
        raise ValueError(f"Estado inválido. Debe ser uno de: {', '.join(estados_validos)}")
    
    return TurnoRepository.cambiar_estado(turno_id, nuevo_estado)


def eliminar_turno(turno_id: int) -> bool:
    """Elimina un turno.
    
    Args:
        turno_id: ID del turno
        
    Returns:
        True si se eliminó correctamente
    """
    # Validar que exista
    obtener_turno_por_id(turno_id)
    
    # Eliminar servicios asociados primero
    TurnoXServicioRepository.eliminar_por_turno(turno_id)
    
    return TurnoRepository.eliminar(turno_id)


def reservar_turno(turno_id: int, id_cliente: int, id_usuario_registro: Optional[int] = None) -> Turno:
    """Reserva un turno para un cliente.
    
    Args:
        turno_id: ID del turno
        id_cliente: ID del cliente
        id_usuario_registro: ID del usuario que registra (opcional)
        
    Returns:
        Turno reservado
        
    Raises:
        ValueError: Si el turno no está disponible
    """
    turno = obtener_turno_por_id(turno_id)
    
    if turno.estado != 'disponible':
        raise ValueError(f"El turno no está disponible (estado actual: {turno.estado})")
    
    turno.estado = 'reservado'
    turno.id_cliente = id_cliente
    turno.id_usuario_registro = id_usuario_registro
    turno.reserva_created_at = datetime.now().isoformat()
    
    TurnoRepository.actualizar(turno)
    return turno


def cancelar_reserva(turno_id: int) -> Turno:
    """Cancela una reserva, devolviendo el turno a disponible.
    
    Args:
        turno_id: ID del turno
        
    Returns:
        Turno actualizado
    """
    turno = obtener_turno_por_id(turno_id)
    
    if turno.estado not in ['reservado', 'bloqueado']:
        raise ValueError(f"Solo se pueden cancelar turnos reservados o bloqueados (estado actual: {turno.estado})")
    
    turno.estado = 'cancelado'
    TurnoRepository.actualizar(turno)
    return turno


def bloquear_turno(turno_id: int, id_usuario: int, motivo: str) -> Turno:
    """Bloquea un turno (admin/operador).
    
    Args:
        turno_id: ID del turno
        id_usuario: ID del usuario que bloquea
        motivo: Motivo del bloqueo
        
    Returns:
        Turno bloqueado
    """
    turno = obtener_turno_por_id(turno_id)
    
    turno.estado = 'bloqueado'
    turno.id_usuario_bloqueo = id_usuario
    turno.motivo_bloqueo = motivo
    
    TurnoRepository.actualizar(turno)
    return turno


def calcular_precio_total_turno(turno_id: int) -> float:
    """Calcula el precio total de un turno (precio base + servicios).
    
    Args:
        turno_id: ID del turno
        
    Returns:
        Precio total
    """
    turno = obtener_turno_por_id(turno_id)
    total_servicios = TurnoXServicioRepository.calcular_total_servicios(turno_id)
    return turno.precio_final + total_servicios
