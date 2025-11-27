"""Servicios para la entidad Turno (Reservas/Turnos de canchas).

Este módulo implementa la lógica de negocio para gestionar turnos/reservas.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from models.turno import Turno
from repositories.turno_repository import TurnoRepository
from repositories.turno_servicio_repository import TurnoXServicioRepository
from repositories.cliente_repository import ClienteRepository


def validar_turno_disponible(turno_id: int) -> Turno:
    """Valida que un turno exista y esté disponible para reservar.
    
    Args:
        turno_id: ID del turno a validar
        
    Returns:
        El turno si está disponible
        
    Raises:
        LookupError: Si el turno no existe
        ValueError: Si el turno no está disponible
    """
    turno = TurnoRepository.obtener_por_id(turno_id)
    if not turno:
        raise LookupError(f"Turno con ID {turno_id} no encontrado")
    
    if turno.estado != 'disponible':
        raise ValueError(f"El turno no está disponible (estado actual: {turno.estado})")
    
    return turno


def cambiar_estado_turno(turno_id: int, nuevo_estado: str) -> bool:
    """Cambia el estado de un turno.
    
    Args:
        turno_id: ID del turno
        nuevo_estado: Nuevo estado ('disponible', 'pendiente_pago', 'reservado', 'bloqueado', 'cancelado', 'finalizado', 'no_disponible')
        
    Returns:
        True si se actualizó correctamente
    """
    estados_validos = ['disponible', 'pendiente_pago', 'reservado', 'bloqueado', 'cancelado', 'finalizado', 'no_disponible']
    if nuevo_estado not in estados_validos:
        raise ValueError(f"Estado '{nuevo_estado}' no válido. Usar: {', '.join(estados_validos)}")
    
    return TurnoRepository.cambiar_estado(turno_id, nuevo_estado)


def _expirar_turnos_pasados() -> None:
    """Marca como no disponibles los turnos vencidos que sigan en estado disponible."""
    TurnoRepository.marcar_pasados_no_disponible()


def _validar_datos_turno(data: Dict[str, Any], para_actualizar: bool = False, turno_id: Optional[int] = None) -> None:
    """Valida los campos para crear/actualizar un turno."""
    if not data.get('id_cancha'):
        raise ValueError("El campo 'id_cancha' es requerido")
    if not data.get('fecha_hora_inicio'):
        raise ValueError("El campo 'fecha_hora_inicio' es requerido")
    if not data.get('fecha_hora_fin'):
        raise ValueError("El campo 'fecha_hora_fin' es requerido")

    # Validar formato y que fecha_fin sea posterior a fecha_inicio
    try:
        inicio_dt = datetime.fromisoformat(str(data['fecha_hora_inicio']))
        fin_dt = datetime.fromisoformat(str(data['fecha_hora_fin']))
    except Exception:
        raise ValueError("Formato de fecha/hora inválido. Usa ISO (YYYY-MM-DDTHH:MM).")

    if fin_dt <= inicio_dt:
        raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio")

    if inicio_dt < datetime.now():
        raise ValueError("No se puede crear/actualizar un turno en una fecha/hora pasada")

    estado = data.get('estado', 'disponible')
    if estado == 'reservado' and not data.get('id_cliente'):
        raise ValueError("Debe indicar un cliente para un turno en estado 'reservado'")

    # Validar solapamiento de turnos en la misma cancha
    if data.get('id_cancha') and data.get('fecha_hora_inicio') and data.get('fecha_hora_fin'):
        if TurnoRepository.existe_solapado(
            id_cancha=data['id_cancha'],
            fecha_hora_inicio=data['fecha_hora_inicio'],
            fecha_hora_fin=data['fecha_hora_fin'],
            excluir_id=turno_id
        ):
            raise ValueError("Ya existe un turno en esa cancha que se solapa con el horario indicado")


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
    _expirar_turnos_pasados()
    turno = TurnoRepository.obtener_por_id(turno_id)
    if not turno:
        raise LookupError(f"Turno con ID {turno_id} no encontrado")
    return turno


def listar_turnos() -> List[Turno]:
    """Lista todos los turnos."""
    _expirar_turnos_pasados()
    return TurnoRepository.obtener_todos_filtrados()


def listar_turnos_por_cancha(id_cancha: int) -> List[Turno]:
    """Lista turnos de una cancha específica."""
    _expirar_turnos_pasados()
    return TurnoRepository.obtener_por_cancha(id_cancha)


def listar_turnos_por_cliente(id_cliente: int) -> List[Turno]:
    """Lista turnos de un cliente específico."""
    _expirar_turnos_pasados()
    return TurnoRepository.obtener_por_cliente(id_cliente)


def listar_turnos_por_cliente_con_detalle(id_cliente: int) -> List[Dict[str, Any]]:
    """Lista turnos de un cliente con información completa de pago y servicios.
    
    Args:
        id_cliente: ID del cliente
        
    Returns:
        Lista de diccionarios con turno + pago + servicios
    """
    from repositories.pago_repository import PagoRepository
    
    _expirar_turnos_pasados()
    turnos = TurnoRepository.obtener_por_cliente(id_cliente)
    
    resultado = []
    for turno in turnos:
        turno_dict = turno.to_dict()
        
        # Obtener pago asociado
        if turno.id:
            try:
                pago = PagoRepository.obtener_por_turno(turno.id)
                if pago:
                    turno_dict['pago'] = {
                        'id': pago.id,
                        'monto_turno': pago.monto_turno,
                        'monto_servicios': pago.monto_servicios,
                        'monto_total': pago.monto_total,
                        'estado': pago.estado,
                        'metodo_pago': pago.metodo_pago,
                        'fecha_creacion': pago.fecha_creacion,
                        'fecha_completado': pago.fecha_completado
                    }
                else:
                    print(f"DEBUG: No hay pago para turno {turno.id}")
            except Exception as e:
                print(f"DEBUG: Error obteniendo pago para turno {turno.id}: {e}")
            
            # Obtener servicios adicionales
            try:
                servicios = TurnoXServicioRepository.listar_por_turno(turno.id)
                if servicios:
                    turno_dict['servicios'] = [
                        {
                            'id_servicio': s.id_servicio,
                            'cantidad': s.cantidad,
                            'precio_unitario': s.precio_unitario_congelado
                        }
                        for s in servicios
                    ]
            except Exception as e:
                print(f"DEBUG: Error obteniendo servicios para turno {turno.id}: {e}")
        
        resultado.append(turno_dict)
    
    return resultado


def listar_turnos_por_estado(estado: str) -> List[Turno]:
    """Lista turnos por estado."""
    _expirar_turnos_pasados()
    return TurnoRepository.obtener_todos_filtrados(estado=estado)


def buscar_disponibles(id_cancha: int, fecha_inicio: str, fecha_fin: str) -> List[Turno]:
    """Busca turnos disponibles en un rango de fechas."""
    _expirar_turnos_pasados()
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
    turno_existente = obtener_turno_por_id(turno_id)

    merged = turno_existente.to_dict()
    merged.update(data)

    _validar_datos_turno(merged, para_actualizar=True, turno_id=turno_id)

    turno_actualizado = Turno.from_dict(merged)
    turno_actualizado.id = turno_id

    success = TurnoRepository.actualizar(turno_actualizado)
    if not success:
        raise Exception("No se pudo actualizar el turno")
    
    return turno_actualizado


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
    estados_validos = ['disponible', 'pendiente_pago', 'reservado', 'bloqueado', 'cancelado', 'finalizado', 'no_disponible']
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

    cliente = ClienteRepository.obtener_por_id(id_cliente)
    if not cliente:
        raise ValueError(f"El cliente con ID {id_cliente} no existe.")
    
    if turno.estado != 'disponible':
        raise ValueError(f"El turno no está disponible (estado actual: {turno.estado})")
    
    turno.estado = 'reservado'
    turno.id_cliente = id_cliente
    turno.id_usuario_registro = id_usuario_registro
    turno.reserva_created_at = datetime.now().isoformat()
    
    TurnoRepository.actualizar(turno)
    return turno


def cancelar_reserva(turno_id: int) -> Turno:
    """Cancela una reserva, devolviendo el turno a disponible y liberando el cliente.
    
    Args:
        turno_id: ID del turno
        
    Returns:
        Turno actualizado
    """
    turno = obtener_turno_por_id(turno_id)
    
    # Si ya está disponible o cancelado, devolverlo idempotente
    if turno.estado in ['disponible', 'cancelado']:
        return turno

    if turno.estado not in ['reservado', 'bloqueado']:
        raise ValueError(f"Solo se pueden cancelar turnos reservados o bloqueados (estado actual: {turno.estado})")
    
    turno.estado = 'disponible'
    turno.id_cliente = None
    turno.id_usuario_registro = None
    turno.reserva_created_at = None
    turno.id_usuario_bloqueo = None
    turno.motivo_bloqueo = None
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
