"""
Repository (DAO) para la entidad Pago.
"""
from typing import List, Optional
from models.pago import Pago
from database.connection import get_connection


class PagoRepository:
    @staticmethod
    def crear(pago: Pago) -> int:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO Pago (
                    id_turno, monto_turno, monto_servicios, monto_total,
                    id_cliente, id_usuario_registro, estado, metodo_pago, id_gateway_externo,
                    fecha_creacion, fecha_expiracion, fecha_completado
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    pago.id_turno, pago.monto_turno, pago.monto_servicios,
                    pago.monto_total, pago.id_cliente, pago.id_usuario_registro, pago.estado,
                    pago.metodo_pago, pago.id_gateway_externo, pago.fecha_creacion,
                    pago.fecha_expiracion, pago.fecha_completado
                )
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear pago: {e}")
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(pago_id: int) -> Optional[Pago]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Pago WHERE id = ?", (pago_id,))
            row = cursor.fetchone()
            return Pago.from_db_row(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def obtener_por_turno(id_turno: int) -> Optional[Pago]:
        """Obtiene el pago asociado a un turno específico"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Pago WHERE id_turno = ? ORDER BY id DESC LIMIT 1", (id_turno,))
            row = cursor.fetchone()
            return Pago.from_db_row(row) if row else None
        finally:
            conn.close()

    # MÉTODO DESHABILITADO: La tabla Inscripcion ya no existe
    # @staticmethod
    # def obtener_por_inscripcion(id_inscripcion: int) -> Optional[Pago]:
    #     """Obtiene el pago asociado a una inscripción específica"""
    #     conn = get_connection()
    #     try:
    #         cursor = conn.cursor()
    #         cursor.execute("SELECT * FROM Pago WHERE id_inscripcion = ? ORDER BY id DESC LIMIT 1", (id_inscripcion,))
    #         row = cursor.fetchone()
    #         return Pago.from_db_row(row) if row else None
    #     finally:
    #         conn.close()

    @staticmethod
    def listar_por_cliente(id_cliente: int) -> List[Pago]:
        """Lista todos los pagos de un cliente"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Pago WHERE id_cliente = ? ORDER BY fecha_creacion DESC", (id_cliente,))
            return [Pago.from_db_row(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def listar_todos() -> List[Pago]:
        """Lista todos los pagos del sistema (para administradores)"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Pago ORDER BY fecha_creacion DESC")
            return [Pago.from_db_row(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def listar_expirados() -> List[Pago]:
        """Lista pagos que expiraron y siguen en estado 'iniciado'"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM Pago 
                WHERE estado = 'iniciado' 
                AND fecha_expiracion IS NOT NULL 
                AND datetime(fecha_expiracion) < datetime('now')
                ORDER BY fecha_expiracion
                """
            )
            return [Pago.from_db_row(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def actualizar(pago: Pago) -> bool:
        if not pago.id:
            raise ValueError("El pago debe tener ID para actualizar")
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE Pago
                SET id_turno = ?, monto_turno = ?, monto_servicios = ?,
                    monto_total = ?, id_cliente = ?, id_usuario_registro = ?, estado = ?,
                    metodo_pago = ?, id_gateway_externo = ?, fecha_creacion = ?,
                    fecha_expiracion = ?, fecha_completado = ?
                WHERE id = ?
                """,
                (
                    pago.id_turno, pago.monto_turno, pago.monto_servicios,
                    pago.monto_total, pago.id_cliente, pago.id_usuario_registro, pago.estado,
                    pago.metodo_pago, pago.id_gateway_externo, pago.fecha_creacion,
                    pago.fecha_expiracion, pago.fecha_completado, pago.id
                )
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar pago: {e}")
        finally:
            conn.close()

    @staticmethod
    def cambiar_estado(pago_id: int, nuevo_estado: str, fecha_completado: Optional[str] = None) -> bool:
        """Cambia el estado de un pago, opcionalmente actualizando fecha_completado"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            if fecha_completado:
                cursor.execute(
                    "UPDATE Pago SET estado = ?, fecha_completado = ? WHERE id = ?",
                    (nuevo_estado, fecha_completado, pago_id)
                )
            else:
                cursor.execute("UPDATE Pago SET estado = ? WHERE id = ?", (nuevo_estado, pago_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def eliminar(pago_id: int) -> bool:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Pago WHERE id = ?", (pago_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar pago: {e}")
        finally:
            conn.close()
