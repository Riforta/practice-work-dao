"""Repository para la entidad TurnoXServicio.

Maneja la relación muchos-a-muchos entre Turnos y Servicios Adicionales.
"""

from typing import List, Optional

from models.turno_servicio import TurnoServicio
from database.connection import get_connection


class TurnoXServicioRepository:
    """Repositorio para gestionar servicios adicionales de turnos."""

    @staticmethod
    def agregar(turno_servicio: TurnoServicio) -> int:
        """Agrega un servicio adicional a un turno.
        
        Args:
            turno_servicio: Instancia de TurnoServicio a crear
            
        Returns:
            ID del registro creado
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO TurnoXServicio (
                    id_turno, id_servicio, cantidad, precio_unitario_congelado
                ) VALUES (?, ?, ?, ?)
                """,
                (
                    turno_servicio.id_turno,
                    turno_servicio.id_servicio,
                    turno_servicio.cantidad,
                    turno_servicio.precio_unitario_congelado,
                ),
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(registro_id: int) -> Optional[TurnoServicio]:
        """Obtiene un registro TurnoXServicio por su ID.
        
        Args:
            registro_id: ID del registro
            
        Returns:
            Instancia de TurnoServicio o None
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM TurnoXServicio WHERE id = ?", (registro_id,))
            row = cursor.fetchone()
            if row:
                return TurnoServicio(
                    id=row["id"],
                    id_turno=row["id_turno"],
                    id_servicio=row["id_servicio"],
                    cantidad=row["cantidad"],
                    precio_unitario_congelado=row["precio_unitario_congelado"],
                )
            return None
        finally:
            conn.close()

    @staticmethod
    def listar_por_turno(id_turno: int) -> List[TurnoServicio]:
        """Lista todos los servicios de un turno específico.
        
        Args:
            id_turno: ID del turno
            
        Returns:
            Lista de servicios del turno
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM TurnoXServicio WHERE id_turno = ?",
                (id_turno,)
            )
            rows = cursor.fetchall()
            return [
                TurnoServicio(
                    id_turno=row["id_turno"],
                    id_servicio=row["id_servicio"],
                    cantidad=row["cantidad"],
                    precio_unitario_congelado=row["precio_unitario_congelado"],
                )
                for row in rows
            ]
        finally:
            conn.close()

    @staticmethod
    def actualizar(turno_servicio: TurnoServicio) -> bool:
        """Actualiza un registro TurnoXServicio.
        
        Args:
            turno_servicio: Instancia con datos actualizados
            
        Returns:
            True si se actualizó correctamente
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE TurnoXServicio SET
                    id_turno = ?,
                    id_servicio = ?,
                    cantidad = ?,
                    precio_unitario_congelado = ?
                WHERE id = ?
                """,
                (
                    turno_servicio.id_turno,
                    turno_servicio.id_servicio,
                    turno_servicio.cantidad,
                    turno_servicio.precio_unitario_congelado,
                    turno_servicio.id,
                ),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def eliminar(registro_id: int) -> bool:
        """Elimina un registro TurnoXServicio.
        
        Args:
            registro_id: ID del registro a eliminar
            
        Returns:
            True si se eliminó correctamente
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM TurnoXServicio WHERE id = ?", (registro_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def eliminar_por_turno(id_turno: int) -> bool:
        """Elimina todos los servicios de un turno.
        
        Args:
            id_turno: ID del turno
            
        Returns:
            True si se eliminó al menos un registro
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM TurnoXServicio WHERE id_turno = ?", (id_turno,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def calcular_total_servicios(id_turno: int) -> float:
        """Calcula el total de servicios adicionales de un turno.
        
        Args:
            id_turno: ID del turno
            
        Returns:
            Total en pesos de los servicios
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT SUM(cantidad * precio_unitario_congelado) as total
                FROM TurnoXServicio
                WHERE id_turno = ?
                """,
                (id_turno,)
            )
            row = cursor.fetchone()
            return row["total"] if row["total"] else 0.0
        finally:
            conn.close()
