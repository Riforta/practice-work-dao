"""Repository para la entidad Turno.

Maneja operaciones CRUD sobre la tabla Turno (reservas/turnos de canchas).
"""

from typing import List, Optional
from datetime import datetime

from models.turno import Turno
from database.connection import get_connection


class TurnoRepository:
    """Repositorio para gestionar turnos/reservas de canchas."""

    @staticmethod
    def crear(turno: Turno) -> int:
        """Crea un nuevo turno en la base de datos.
        
        Args:
            turno: Instancia de Turno a crear
            
        Returns:
            ID del turno creado
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO Turno (
                    id_cancha, fecha_hora_inicio, fecha_hora_fin, estado,
                    precio_final, id_cliente, id_usuario_registro,
                    reserva_created_at, id_usuario_bloqueo, motivo_bloqueo
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    turno.id_cancha,
                    turno.fecha_hora_inicio,
                    turno.fecha_hora_fin,
                    turno.estado,
                    turno.precio_final,
                    turno.id_cliente,
                    turno.id_usuario_registro,
                    turno.reserva_created_at,
                    turno.id_usuario_bloqueo,
                    turno.motivo_bloqueo,
                ),
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(turno_id: int) -> Optional[Turno]:
        """Obtiene un turno por su ID.
        
        Args:
            turno_id: ID del turno a buscar
            
        Returns:
            Instancia de Turno o None si no existe
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Turno WHERE id = ?", (turno_id,))
            row = cursor.fetchone()
            if row:
                return Turno(
                    id=row["id"],
                    id_cancha=row["id_cancha"],
                    fecha_hora_inicio=row["fecha_hora_inicio"],
                    fecha_hora_fin=row["fecha_hora_fin"],
                    estado=row["estado"],
                    precio_final=row["precio_final"],
                    id_cliente=row["id_cliente"],
                    id_usuario_registro=row["id_usuario_registro"],
                    reserva_created_at=row["reserva_created_at"],
                    id_usuario_bloqueo=row["id_usuario_bloqueo"],
                    motivo_bloqueo=row["motivo_bloqueo"],
                )
            return None
        finally:
            conn.close()

    @staticmethod
    def listar_todos() -> List[Turno]:
        """Lista todos los turnos.
        
        Returns:
            Lista de instancias de Turno
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Turno ORDER BY fecha_hora_inicio DESC")
            rows = cursor.fetchall()
            return [
                Turno(
                    id=row["id"],
                    id_cancha=row["id_cancha"],
                    fecha_hora_inicio=row["fecha_hora_inicio"],
                    fecha_hora_fin=row["fecha_hora_fin"],
                    estado=row["estado"],
                    precio_final=row["precio_final"],
                    id_cliente=row["id_cliente"],
                    id_usuario_registro=row["id_usuario_registro"],
                    reserva_created_at=row["reserva_created_at"],
                    id_usuario_bloqueo=row["id_usuario_bloqueo"],
                    motivo_bloqueo=row["motivo_bloqueo"],
                )
                for row in rows
            ]
        finally:
            conn.close()

    @staticmethod
    def listar_por_cancha(id_cancha: int) -> List[Turno]:
        """Lista turnos de una cancha específica.
        
        Args:
            id_cancha: ID de la cancha
            
        Returns:
            Lista de turnos de la cancha
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Turno WHERE id_cancha = ? ORDER BY fecha_hora_inicio DESC",
                (id_cancha,)
            )
            rows = cursor.fetchall()
            return [
                Turno(
                    id=row["id"],
                    id_cancha=row["id_cancha"],
                    fecha_hora_inicio=row["fecha_hora_inicio"],
                    fecha_hora_fin=row["fecha_hora_fin"],
                    estado=row["estado"],
                    precio_final=row["precio_final"],
                    id_cliente=row["id_cliente"],
                    id_usuario_registro=row["id_usuario_registro"],
                    reserva_created_at=row["reserva_created_at"],
                    id_usuario_bloqueo=row["id_usuario_bloqueo"],
                    motivo_bloqueo=row["motivo_bloqueo"],
                )
                for row in rows
            ]
        finally:
            conn.close()

    @staticmethod
    def listar_por_cliente(id_cliente: int) -> List[Turno]:
        """Lista turnos de un cliente específico.
        
        Args:
            id_cliente: ID del cliente
            
        Returns:
            Lista de turnos del cliente
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Turno WHERE id_cliente = ? ORDER BY fecha_hora_inicio DESC",
                (id_cliente,)
            )
            rows = cursor.fetchall()
            return [
                Turno(
                    id=row["id"],
                    id_cancha=row["id_cancha"],
                    fecha_hora_inicio=row["fecha_hora_inicio"],
                    fecha_hora_fin=row["fecha_hora_fin"],
                    estado=row["estado"],
                    precio_final=row["precio_final"],
                    id_cliente=row["id_cliente"],
                    id_usuario_registro=row["id_usuario_registro"],
                    reserva_created_at=row["reserva_created_at"],
                    id_usuario_bloqueo=row["id_usuario_bloqueo"],
                    motivo_bloqueo=row["motivo_bloqueo"],
                )
                for row in rows
            ]
        finally:
            conn.close()

    @staticmethod
    def listar_por_estado(estado: str) -> List[Turno]:
        """Lista turnos por estado.
        
        Args:
            estado: Estado a filtrar (disponible, reservado, bloqueado, cancelado, finalizado)
            
        Returns:
            Lista de turnos con el estado especificado
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Turno WHERE estado = ? ORDER BY fecha_hora_inicio",
                (estado,)
            )
            rows = cursor.fetchall()
            return [
                Turno(
                    id=row["id"],
                    id_cancha=row["id_cancha"],
                    fecha_hora_inicio=row["fecha_hora_inicio"],
                    fecha_hora_fin=row["fecha_hora_fin"],
                    estado=row["estado"],
                    precio_final=row["precio_final"],
                    id_cliente=row["id_cliente"],
                    id_usuario_registro=row["id_usuario_registro"],
                    reserva_created_at=row["reserva_created_at"],
                    id_usuario_bloqueo=row["id_usuario_bloqueo"],
                    motivo_bloqueo=row["motivo_bloqueo"],
                )
                for row in rows
            ]
        finally:
            conn.close()

    @staticmethod
    def actualizar(turno: Turno) -> bool:
        """Actualiza un turno existente.
        
        Args:
            turno: Instancia de Turno con datos actualizados
            
        Returns:
            True si se actualizó correctamente
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE Turno SET
                    id_cancha = ?,
                    fecha_hora_inicio = ?,
                    fecha_hora_fin = ?,
                    estado = ?,
                    precio_final = ?,
                    id_cliente = ?,
                    id_usuario_registro = ?,
                    reserva_created_at = ?,
                    id_usuario_bloqueo = ?,
                    motivo_bloqueo = ?
                WHERE id = ?
                """,
                (
                    turno.id_cancha,
                    turno.fecha_hora_inicio,
                    turno.fecha_hora_fin,
                    turno.estado,
                    turno.precio_final,
                    turno.id_cliente,
                    turno.id_usuario_registro,
                    turno.reserva_created_at,
                    turno.id_usuario_bloqueo,
                    turno.motivo_bloqueo,
                    turno.id,
                ),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def cambiar_estado(turno_id: int, nuevo_estado: str) -> bool:
        """Cambia el estado de un turno.
        
        Args:
            turno_id: ID del turno
            nuevo_estado: Nuevo estado del turno
            
        Returns:
            True si se actualizó correctamente
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE Turno SET estado = ? WHERE id = ?",
                (nuevo_estado, turno_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def eliminar(turno_id: int) -> bool:
        """Elimina un turno.
        
        Args:
            turno_id: ID del turno a eliminar
            
        Returns:
            True si se eliminó correctamente
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Turno WHERE id = ?", (turno_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def buscar_disponibles(id_cancha: int, fecha_inicio: str, fecha_fin: str) -> List[Turno]:
        """Busca turnos disponibles en un rango de fechas para una cancha.
        
        Args:
            id_cancha: ID de la cancha
            fecha_inicio: Fecha/hora de inicio del rango
            fecha_fin: Fecha/hora de fin del rango
            
        Returns:
            Lista de turnos disponibles
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT * FROM Turno 
                WHERE id_cancha = ? 
                  AND estado = 'disponible'
                  AND fecha_hora_inicio >= ?
                  AND fecha_hora_inicio <= ?
                ORDER BY fecha_hora_inicio
                """,
                (id_cancha, fecha_inicio, fecha_fin)
            )
            rows = cursor.fetchall()
            return [
                Turno(
                    id=row["id"],
                    id_cancha=row["id_cancha"],
                    fecha_hora_inicio=row["fecha_hora_inicio"],
                    fecha_hora_fin=row["fecha_hora_fin"],
                    estado=row["estado"],
                    precio_final=row["precio_final"],
                    id_cliente=row["id_cliente"],
                    id_usuario_registro=row["id_usuario_registro"],
                    reserva_created_at=row["reserva_created_at"],
                    id_usuario_bloqueo=row["id_usuario_bloqueo"],
                    motivo_bloqueo=row["motivo_bloqueo"],
                )
                for row in rows
            ]
        finally:
            conn.close()
