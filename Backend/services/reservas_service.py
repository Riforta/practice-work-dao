"""
Servicio de lógica de negocio para Reservas de Turnos.

Este servicio maneja específicamente las operaciones de reservas (CU-1 a CU-4):
registrar, consultar, modificar y cancelar reservas con validaciones de negocio.
"""

from typing import Optional, List
from models.turno import Turno
from repositories.turno_repository import TurnoRepository
from repositories.cliente_repository import ClienteRepository
from repositories.usuario_repository import UsuarioRepository
from datetime import datetime


class ReservasService:
    """Servicio para la lógica de negocio de reservas de turnos (CU-1 a CU-4)"""

    @staticmethod
    def _expirar_turnos_pasados() -> None:
        """Marca como no disponibles los turnos disponibles vencidos."""
        TurnoRepository.marcar_pasados_no_disponible()

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
    
    @staticmethod
    def consultar_turno_por_id(turno_id: int, id_cliente: Optional[int] = None) -> Turno:
        """
        Busca un turno por su ID.
        Lanza LookupError si no lo encuentra.
        Regla de pertenencia (si se informa id_cliente):
        - Si el turno está reservado debe pertenecer a ese cliente.
        - Si no pertenece o no está reservado para él -> PermissionError.
        """
        ReservasService._expirar_turnos_pasados()
        turno = TurnoRepository.obtener_por_id(turno_id)
        if not turno:
            raise LookupError(f"El turno con ID {turno_id} no existe.")

        if id_cliente is not None:
            # Si el turno no está reservado por ese cliente, negamos acceso
            if turno.id_cliente is None or turno.id_cliente != id_cliente:
                raise PermissionError("La reserva no pertenece al cliente indicado.")
        return turno

    @staticmethod
    def listar_reservas_cliente(
        id_cliente: int,
        id_cancha: Optional[int] = None,
        estado: Optional[str] = None
    ) -> List[Turno]:
        """
        Lista reservas (turnos con asociación a un cliente) para un cliente dado.
        Opcionalmente filtra por cancha y estado.
        Reglas:
        - El cliente debe existir.
        - Estado (si se proporciona) debe ser válido.
        - Solo devuelve turnos cuyo id_cliente coincide.
        """
        if not ClienteRepository.obtener_por_id(id_cliente):
            raise ValueError(f"El cliente con ID {id_cliente} no existe.")

        ESTADOS_VALIDOS = ['disponible', 'reservado', 'bloqueado', 'mantenimiento', 'no_disponible']
        if estado and estado not in ESTADOS_VALIDOS:
            raise ValueError(f"El estado '{estado}' no es válido. Valores permitidos: {ESTADOS_VALIDOS}")

        ReservasService._expirar_turnos_pasados()
        turnos = TurnoRepository.obtener_todos_filtrados(
            id_cancha=id_cancha,
            estado=estado,
            id_cliente=id_cliente
        )
        return turnos

    @staticmethod
    def listar_turnos(
        id_cancha: Optional[int] = None,
        estado: Optional[str] = None,
        id_cliente: Optional[int] = None
    ) -> List[Turno]:
        """
        Wrapper de compatibilidad usado por las rutas actuales.
        - Si se informa id_cliente: delega en listar_reservas_cliente (valida cliente y estado).
        - Si no se informa id_cliente: valida estado y devuelve según filtros (uso administrativo potencial).
        """
        ESTADOS_VALIDOS = ['disponible', 'reservado', 'bloqueado', 'mantenimiento', 'no_disponible']
        if estado and estado not in ESTADOS_VALIDOS:
            raise ValueError(f"El estado '{estado}' no es válido. Valores permitidos: {ESTADOS_VALIDOS}")

        ReservasService._expirar_turnos_pasados()
        if id_cliente is not None:
            return ReservasService.listar_reservas_cliente(
                id_cliente=id_cliente,
                id_cancha=id_cancha,
                estado=estado
            )

        # Listado general (no usado por cliente final), sin validar cliente
        return TurnoRepository.obtener_todos_filtrados(
            id_cancha=id_cancha,
            estado=estado,
            id_cliente=id_cliente
        )
    
    @staticmethod
    def modificar_reserva(
        turno_id: int, 
        nuevos_datos: dict,
        id_usuario_mod: int # Opcional: para auditar quién hizo el cambio
    ) -> Turno:
        """
        Modifica los datos de una reserva existente (un turno 'reservado').
        'nuevos_datos' es un diccionario con los campos a cambiar.
        Campos permitidos para modificar: 'id_cliente', 'precio_final'.
        """

        # 1. Validar el usuario (quién modifica)
        if not UsuarioRepository.obtener_por_id(id_usuario_mod):
            raise ValueError(f"El usuario (admin) con ID {id_usuario_mod} no existe.")

        # 2. Obtener el turno que se quiere modificar
        turno_a_modificar = TurnoRepository.obtener_por_id(turno_id)
        
        if not turno_a_modificar:
            raise LookupError(f"El turno con ID {turno_id} no existe.")

        # 3. Validar Lógica de Negocio (Estado)
        if turno_a_modificar.estado != 'reservado':
            raise ValueError(f"Solo se pueden modificar turnos que estén 'reservados' (Estado actual: {turno_a_modificar.estado}).")

        # 4. Aplicar los cambios (lógica de 'PATCH')
        cambios_realizados = False
        
        # 4a. ¿Se quiere cambiar el cliente?
        if 'id_cliente' in nuevos_datos:
            nuevo_id_cliente = nuevos_datos['id_cliente']
            # Validamos que el nuevo cliente exista
            if not ClienteRepository.obtener_por_id(nuevo_id_cliente):
                raise ValueError(f"El nuevo cliente con ID {nuevo_id_cliente} no existe.")
            
            turno_a_modificar.id_cliente = nuevo_id_cliente
            cambios_realizados = True
            
        # 4b. ¿Se quiere cambiar el precio final?
        if 'precio_final' in nuevos_datos:
            nuevo_precio = nuevos_datos['precio_final']
            if not isinstance(nuevo_precio, (int, float)) or nuevo_precio < 0:
                raise ValueError("El precio final debe ser un número positivo.")
                
            turno_a_modificar.precio_final = nuevo_precio
            cambios_realizados = True
        
        # 4c. ¿Se quiere cambiar el usuario que lo registró?
        # (Esto actualiza quién fue el *último* en modificar la reserva)
        if cambios_realizados:
            turno_a_modificar.id_usuario_registro = id_usuario_mod
            # Opcional: actualizar la fecha de modificación
            # turno_a_modificar.reserva_created_at = datetime.now().isoformat()
        else:
            # Si no se envió ningún dato válido para cambiar, lo informamos.
            raise ValueError("No se proporcionaron datos válidos para modificar ('id_cliente', 'precio_final').")

        # 5. Persistir el cambio en la base de datos
        try:
            TurnoRepository.actualizar(turno_a_modificar)
            return turno_a_modificar
        except Exception as e:
            raise Exception(f"No se pudo modificar la reserva: {e}")
        
    @staticmethod
    def cancelar_reserva(turno_id: int, id_usuario_cancelacion: int) -> Turno:
        """
        Cancela una reserva existente.
        Esto cambia el estado de 'reservado' de nuevo a 'disponible'
        y limpia los campos del cliente.
        """
        
        # 1. Validar el usuario (quién cancela)
        # (Asumimos que solo un admin puede cancelar)
        if not UsuarioRepository.obtener_por_id(id_usuario_cancelacion):
            raise ValueError(f"El usuario (admin) con ID {id_usuario_cancelacion} no existe.")

        # 2. Obtener el turno que se quiere cancelar
        turno_a_cancelar = TurnoRepository.obtener_por_id(turno_id)
        
        if not turno_a_cancelar:
            raise LookupError(f"El turno con ID {turno_id} no existe.")

        # 3. Validar Lógica de Negocio (Estado)
        if turno_a_cancelar.estado != 'reservado':
            raise ValueError(f"Solo se pueden cancelar turnos que estén 'reservados' (Estado actual: {turno_a_cancelar.estado}).")

        # 4. Aplicar la "cancelación" (Resetear el turno)
        # Volvemos el estado a 'disponible'
        turno_a_cancelar.estado = 'disponible'
        
        # MUY IMPORTANTE: Limpiamos los campos de la reserva
        turno_a_cancelar.id_cliente = None
        turno_a_cancelar.id_usuario_registro = None
        turno_a_cancelar.reserva_created_at = None

        # 5. Persistir el cambio en la base de datos
        try:
            TurnoRepository.actualizar(turno_a_cancelar)
            return turno_a_cancelar
        except Exception as e:
            raise Exception(f"No se pudo cancelar la reserva: {e}")
