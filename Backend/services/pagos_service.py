from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from models.pago import Pago
from repositories.pago_repository import PagoRepository
from repositories.turno_repository import TurnoRepository
from repositories.inscripcion_repository import InscripcionRepository
from repositories.turno_servicio_repository import TurnoXServicioRepository


def crear_pago_turno(
    id_turno: int,
    id_cliente: int,
    monto_turno: float,
    monto_servicios: float,
    servicios: Optional[List[Dict[str, Any]]] = None,
    id_usuario_registro: Optional[int] = None,
    metodo_pago: Optional[str] = None
) -> Pago:
    """
    Crea un pago para un turno y cambia su estado a 'pendiente_pago'.
    
    Args:
        id_turno: ID del turno a reservar
        id_cliente: ID del cliente que reserva
        monto_turno: Precio del turno
        monto_servicios: Suma de servicios adicionales
        servicios: Lista de servicios con {id_servicio, cantidad, precio_unitario}
        id_usuario_registro: Usuario que registra (opcional, puede ser el mismo cliente)
        metodo_pago: Método de pago utilizado
    
    Returns:
        Pago creado con estado 'iniciado' y fecha_expiracion en 15 minutos
    """
    # Verificar que el turno exista y esté disponible
    turno = TurnoRepository.obtener_por_id(id_turno)
    if not turno:
        raise LookupError(f'Turno con ID {id_turno} no encontrado')
    
    if turno.estado != 'disponible':
        raise ValueError(f'El turno no está disponible (estado actual: {turno.estado})')
    
    # Crear el pago
    fecha_creacion = datetime.now().isoformat()
    fecha_expiracion = (datetime.now() + timedelta(minutes=15)).isoformat()
    
    pago_data = {
        'id_turno': id_turno,
        'id_inscripcion': None,
        'monto_turno': monto_turno,
        'monto_servicios': monto_servicios,
        'monto_total': monto_turno + monto_servicios,
        'id_cliente': id_cliente,
        'id_usuario_registro': id_usuario_registro,
        'estado': 'iniciado',
        'metodo_pago': metodo_pago,
        'fecha_creacion': fecha_creacion,
        'fecha_expiracion': fecha_expiracion,
        'fecha_completado': None
    }
    
    pago = Pago.from_dict(pago_data)
    
    try:
        # Crear el pago
        pago.id = PagoRepository.crear(pago)
        
        # Cambiar estado del turno a 'pendiente_pago'
        TurnoRepository.cambiar_estado(id_turno, 'pendiente_pago')
        
        # Si hay servicios, guardarlos (aunque el pago no esté completado aún)
        # Esto es para tener el registro de qué se pidió
        if servicios:
            for servicio in servicios:
                TurnoXServicioRepository.crear({
                    'id_turno': id_turno,
                    'id_servicio': servicio['id_servicio'],
                    'cantidad': servicio.get('cantidad', 1),
                    'precio_unitario_congelado': servicio['precio_unitario']
                })
        
        return pago
    except Exception as e:
        raise Exception(f'Error al crear pago de turno: {e}')


def crear_pago_inscripcion(
    id_inscripcion: int,
    id_cliente: int,
    monto_total: float,
    id_usuario_registro: Optional[int] = None,
    metodo_pago: Optional[str] = None
) -> Pago:
    """
    Crea un pago para una inscripción de torneo.
    
    Args:
        id_inscripcion: ID de la inscripción
        id_cliente: ID del cliente (capitán del equipo)
        monto_total: Costo de inscripción del torneo
        id_usuario_registro: Usuario que registra
        metodo_pago: Método de pago utilizado
    
    Returns:
        Pago creado con estado 'iniciado' y fecha_expiracion en 15 minutos
    """
    # Verificar que la inscripción exista
    inscripcion = InscripcionRepository.obtener_por_id(id_inscripcion)
    if not inscripcion:
        raise LookupError(f'Inscripción con ID {id_inscripcion} no encontrada')
    
    if inscripcion.estado != 'pendiente_pago':
        raise ValueError(f'La inscripción no está pendiente de pago (estado: {inscripcion.estado})')
    
    # Crear el pago
    fecha_creacion = datetime.now().isoformat()
    fecha_expiracion = (datetime.now() + timedelta(minutes=15)).isoformat()
    
    pago_data = {
        'id_turno': None,
        'id_inscripcion': id_inscripcion,
        'monto_turno': None,
        'monto_servicios': 0.0,
        'monto_total': monto_total,
        'id_cliente': id_cliente,
        'id_usuario_registro': id_usuario_registro,
        'estado': 'iniciado',
        'metodo_pago': metodo_pago,
        'fecha_creacion': fecha_creacion,
        'fecha_expiracion': fecha_expiracion,
        'fecha_completado': None
    }
    
    pago = Pago.from_dict(pago_data)
    
    try:
        pago.id = PagoRepository.crear(pago)
        return pago
    except Exception as e:
        raise Exception(f'Error al crear pago de inscripción: {e}')


def confirmar_pago(
    pago_id: int,
    metodo_pago: Optional[str] = None,
    id_gateway_externo: Optional[str] = None
) -> Pago:
    """
    Confirma un pago exitoso y actualiza el estado del turno/inscripción asociado.
    
    Args:
        pago_id: ID del pago a confirmar
        metodo_pago: Método de pago final usado
        id_gateway_externo: ID de transacción del gateway de pago
    
    Returns:
        Pago actualizado con estado 'completado'
    """
    pago = PagoRepository.obtener_por_id(pago_id)
    if not pago:
        raise LookupError(f'Pago con ID {pago_id} no encontrado')
    
    if pago.estado != 'iniciado':
        raise ValueError(f'El pago no está en estado iniciado (estado actual: {pago.estado})')
    
    # Verificar si el pago no expiró
    if pago.fecha_expiracion:
        fecha_exp = datetime.fromisoformat(pago.fecha_expiracion)
        if datetime.now() > fecha_exp:
            raise ValueError('El pago ha expirado')
    
    fecha_completado = datetime.now().isoformat()
    
    try:
        # Actualizar el pago
        pago.estado = 'completado'
        pago.fecha_completado = fecha_completado
        if metodo_pago:
            pago.metodo_pago = metodo_pago
        if id_gateway_externo:
            pago.id_gateway_externo = id_gateway_externo
        
        PagoRepository.actualizar(pago)
        
        # Actualizar el estado del turno o inscripción
        if pago.id_turno:
            TurnoRepository.cambiar_estado(pago.id_turno, 'reservado')
        elif pago.id_inscripcion:
            InscripcionRepository.cambiar_estado(pago.id_inscripcion, 'confirmada')
        
        return pago
    except Exception as e:
        raise Exception(f'Error al confirmar pago: {e}')


def marcar_pago_fallido(pago_id: int) -> bool:
    """
    Marca un pago como fallido y libera el turno/inscripción asociado.
    
    Returns:
        True si se actualizó correctamente
    """
    pago = PagoRepository.obtener_por_id(pago_id)
    if not pago:
        raise LookupError(f'Pago con ID {pago_id} no encontrado')
    
    try:
        # Marcar pago como fallido
        PagoRepository.cambiar_estado(pago_id, 'fallido')
        
        # Liberar turno o inscripción
        if pago.id_turno:
            TurnoRepository.cambiar_estado(pago.id_turno, 'disponible')
            # Opcional: eliminar servicios asociados
            # TurnoServicioRepository.eliminar_por_turno(pago.id_turno)
        elif pago.id_inscripcion:
            InscripcionRepository.cambiar_estado(pago.id_inscripcion, 'cancelada')
        
        return True
    except Exception as e:
        raise Exception(f'Error al marcar pago como fallido: {e}')


def procesar_pagos_expirados() -> int:
    """
    Procesa todos los pagos que expiraron y los marca como fallidos.
    Debe ejecutarse periódicamente (ej: cada minuto con un cron job).
    
    Returns:
        Cantidad de pagos marcados como fallidos
    """
    try:
        pagos_expirados = PagoRepository.listar_expirados()
        contador = 0
        
        for pago in pagos_expirados:
            try:
                marcar_pago_fallido(pago.id)
                contador += 1
            except Exception as e:
                # Log error pero continuar con los demás
                print(f'Error al procesar pago expirado {pago.id}: {e}')
        
        return contador
    except Exception as e:
        raise Exception(f'Error al procesar pagos expirados: {e}')


def obtener_pago_por_id(pago_id: int) -> Pago:
    """Obtiene un pago por su ID"""
    pago = PagoRepository.obtener_por_id(pago_id)
    if pago is None:
        raise LookupError(f'Pago con ID {pago_id} no encontrado')
    return pago


def obtener_pago_por_turno(id_turno: int) -> Optional[Pago]:
    """Obtiene el pago asociado a un turno"""
    return PagoRepository.obtener_por_turno(id_turno)


def obtener_pago_por_inscripcion(id_inscripcion: int) -> Optional[Pago]:
    """Obtiene el pago asociado a una inscripción"""
    return PagoRepository.obtener_por_inscripcion(id_inscripcion)


def listar_pagos_por_cliente(id_cliente: int) -> List[Pago]:
    """Lista todos los pagos de un cliente"""
    return PagoRepository.listar_por_cliente(id_cliente)


def eliminar_pago(pago_id: int) -> bool:
    """Elimina un pago (usar con precaución)"""
    try:
        return PagoRepository.eliminar(pago_id)
    except Exception as e:
        raise Exception(f'Error al eliminar pago: {e}')
