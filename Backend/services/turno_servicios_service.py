"""Servicios para TurnoXServicio (servicios adicionales de turnos)."""

from typing import List, Dict, Any

from models.turno_servicio import TurnoServicio
from repositories.turno_servicio_repository import TurnoXServicioRepository
from repositories.servicio_adicional_repository import ServicioAdicionalRepository


def agregar_servicio_a_turno(data: Dict[str, Any]) -> TurnoServicio:
    """Agrega un servicio adicional a un turno.
    
    Args:
        data: Diccionario con id_turno, id_servicio, cantidad
        
    Returns:
        Instancia de TurnoServicio creado
    """
    if not data.get('id_turno'):
        raise ValueError("El campo 'id_turno' es requerido")
    if not data.get('id_servicio'):
        raise ValueError("El campo 'id_servicio' es requerido")
    
    cantidad = data.get('cantidad', 1)
    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor a 0")
    
    # Obtener el precio actual del servicio
    servicio = ServicioAdicionalRepository.obtener_por_id(data['id_servicio'])
    if not servicio:
        raise LookupError(f"Servicio con ID {data['id_servicio']} no encontrado")
    
    if not servicio.activo:
        raise ValueError(f"El servicio '{servicio.nombre}' no está activo")
    
    turno_servicio = TurnoServicio(
        id_turno=data['id_turno'],
        id_servicio=data['id_servicio'],
        cantidad=cantidad,
        precio_unitario_congelado=servicio.precio_actual,
    )
    
    registro_id = TurnoXServicioRepository.agregar(turno_servicio)
    turno_servicio.id = registro_id
    return turno_servicio


def listar_servicios_por_turno(id_turno: int) -> List[TurnoServicio]:
    """Lista todos los servicios de un turno."""
    return TurnoXServicioRepository.listar_por_turno(id_turno)


def actualizar_servicio_turno(registro_id: int, data: Dict[str, Any]) -> TurnoServicio:
    """Actualiza la cantidad de un servicio en un turno.
    
    Args:
        registro_id: ID del registro TurnoXServicio
        data: Datos a actualizar (cantidad)
        
    Returns:
        Instancia actualizada
    """
    turno_servicio = TurnoXServicioRepository.obtener_por_id(registro_id)
    if not turno_servicio:
        raise LookupError(f"Registro con ID {registro_id} no encontrado")
    
    if 'cantidad' in data:
        cantidad = data['cantidad']
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        turno_servicio.cantidad = cantidad
    
    success = TurnoXServicioRepository.actualizar(turno_servicio)
    if not success:
        raise Exception("No se pudo actualizar el servicio")
    
    return turno_servicio


def eliminar_servicio_turno(registro_id: int) -> bool:
    """Elimina un servicio de un turno.
    
    Args:
        registro_id: ID del registro
        
    Returns:
        True si se eliminó correctamente
    """
    # Validar que exista
    turno_servicio = TurnoXServicioRepository.obtener_por_id(registro_id)
    if not turno_servicio:
        raise LookupError(f"Registro con ID {registro_id} no encontrado")
    
    return TurnoXServicioRepository.eliminar(registro_id)


def calcular_total_servicios_turno(id_turno: int) -> float:
    """Calcula el total de servicios de un turno."""
    return TurnoXServicioRepository.calcular_total_servicios(id_turno)
