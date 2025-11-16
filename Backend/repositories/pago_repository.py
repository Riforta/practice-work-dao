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
                INSERT INTO Pago (id_pedido, monto, estado, metodo_pago, id_gateway_externo, fecha_pago, id_usuario_manual)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (pago.id_pedido, pago.monto, pago.estado, pago.metodo_pago, pago.id_gateway_externo, pago.fecha_pago, pago.id_usuario_manual)
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
    def listar_por_pedido(id_pedido: int) -> List[Pago]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Pago WHERE id_pedido = ? ORDER BY id DESC", (id_pedido,))
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
                SET id_pedido = ?, monto = ?, estado = ?, metodo_pago = ?, id_gateway_externo = ?, fecha_pago = ?, id_usuario_manual = ?
                WHERE id = ?
                """,
                (pago.id_pedido, pago.monto, pago.estado, pago.metodo_pago, pago.id_gateway_externo, pago.fecha_pago, pago.id_usuario_manual, pago.id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar pago: {e}")
        finally:
            conn.close()

    @staticmethod
    def cambiar_estado(pago_id: int, nuevo_estado: str) -> bool:
        conn = get_connection()
        try:
            cursor = conn.cursor()
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
