"""
Servicio de lógica de negocio para Turnos/Reservas.
"""

from models.turno import Turno
from repository.turno_repository import TurnoRepository
from repository.cliente_repository import ClienteRepository
from datetime import datetime


class TurnoService:
    """Servicio para la lógica de negocio de turnos"""

    @staticmethod
    def registrar_reserva(
        turno_id: int, 
        id_cliente: int, 
        id_usuario_registro: int
    ) -> Turno:
        """
        Orquesta la lógica de negocio para registrar una RESERVA.
        Esto es un UPDATE, no un CREATE.
        
        Args:
            turno_id: ID del turno a reservar
            id_cliente: ID del cliente que hace la reserva
            id_usuario_registro: ID del usuario que registra la reserva
            
        Returns:
            Objeto Turno actualizado
            
        Raises:
            ValueError: Si hay error de validación de negocio
            LookupError: Si no se encuentra el turno
            Exception: Si hay error en la persistencia
        """
        
        # 1. Validar que el cliente existe
        if not ClienteRepository.obtener_por_id(id_cliente):
            raise ValueError(f"El cliente con ID {id_cliente} no existe.")

        # 2. Obtener el turno que se quiere reservar
        turno_a_reservar = TurnoRepository.obtener_por_id(turno_id)
        
        if not turno_a_reservar:
            raise LookupError(f"El turno con ID {turno_id} no existe.")

        # 3. Validar Lógica de Negocio (Disponibilidad)
        if turno_a_reservar.estado != 'disponible':
            raise ValueError(
                f"El turno {turno_id} no está disponible. Estado actual: {turno_a_reservar.estado}"
            )

        # 4. Modificar el objeto modelo 'Turno'
        turno_a_reservar.estado = 'reservado'
        turno_a_reservar.id_cliente = id_cliente
        turno_a_reservar.id_usuario_registro = id_usuario_registro
        turno_a_reservar.reserva_created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Limpiar campos de bloqueo
        turno_a_reservar.id_usuario_bloqueo = None
        turno_a_reservar.motivo_bloqueo = None

        # 5. Persistir el cambio en la base de datos
        try:
            actualizado_ok = TurnoRepository.actualizar(turno_a_reservar)
            if not actualizado_ok:
                raise Exception("No se pudo actualizar la base de datos (rowcount 0).")
                
            return turno_a_reservar
        except Exception as e:
            raise Exception(f"No se pudo registrar la reserva: {e}")