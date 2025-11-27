from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from models.pago import Pago
from repositories.pago_repository import PagoRepository


def crear_pago_turno(
    id_turno: int,
    id_cliente: int,
    monto_turno: float,
    monto_servicios: float,
    id_usuario_registro: Optional[int] = None,
    metodo_pago: Optional[str] = None
) -> Pago:
    """
    Crea un registro de pago para un turno.
    SOLO gestiona el pago, NO modifica el turno ni agrega servicios.
    
    Args:
        id_turno: ID del turno a pagar
        id_cliente: ID del cliente que paga
        monto_turno: Precio del turno
        monto_servicios: Suma de servicios adicionales
        id_usuario_registro: Usuario que registra (opcional)
        metodo_pago: Método de pago utilizado
    
    Returns:
        Pago creado con estado 'iniciado' y fecha_expiracion en 15 minutos
    """
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
        # Crear el pago en la BD
        pago.id = PagoRepository.crear(pago)
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
    Crea un registro de pago para una inscripción de torneo.
    SOLO gestiona el pago, NO modifica la inscripción.
    
    Args:
        id_inscripcion: ID de la inscripción
        id_cliente: ID del cliente (capitán del equipo)
        monto_total: Costo de inscripción del torneo
        id_usuario_registro: Usuario que registra
        metodo_pago: Método de pago utilizado
    
    Returns:
        Pago creado con estado 'iniciado' y fecha_expiracion en 15 minutos
    """
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
    Confirma un pago exitoso marcándolo como 'completado'.
    NO modifica el estado del turno/inscripción - eso lo hace la reserva/inscripción.
    
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
        
        # NO modificamos el turno/inscripción aquí
        # Eso lo hace registrar_reserva() o crear_inscripcion()
        
        return pago
    except Exception as e:
        raise Exception(f'Error al confirmar pago: {e}')


def marcar_pago_fallido(pago_id: int) -> Pago:
    """
    Marca un pago como fallido.
    SOLO gestiona el pago, NO modifica turno/inscripción.
    El llamador debe liberar el turno/inscripción según corresponda.
    
    Returns:
        Pago actualizado con estado 'fallido'
    """
    pago = PagoRepository.obtener_por_id(pago_id)
    if not pago:
        raise LookupError(f'Pago con ID {pago_id} no encontrado')
    
    try:
        # Marcar pago como fallido
        PagoRepository.cambiar_estado(pago_id, 'fallido')
        pago.estado = 'fallido'
        return pago
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
