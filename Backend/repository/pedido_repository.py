"""
Repository (DAO) para la entidad Pedido.
"""
from typing import List, Optional
from models.pedido import Pedido
from database.connection import get_connection


class PedidoRepository:
    @staticmethod
    def crear(pedido: Pedido) -> int:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO Pedido (id_cliente, monto_total, estado, fecha_creacion, fecha_expiracion)
                VALUES (?, ?, ?, ?, ?)
                """,
                (pedido.id_cliente, pedido.monto_total, pedido.estado, pedido.fecha_creacion, pedido.fecha_expiracion)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear pedido: {e}")
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(pedido_id: int) -> Optional[Pedido]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Pedido WHERE id = ?", (pedido_id,))
            row = cursor.fetchone()
            return Pedido.from_db_row(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def listar_por_cliente(id_cliente: int) -> List[Pedido]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Pedido WHERE id_cliente = ? ORDER BY fecha_creacion DESC", (id_cliente,))
            return [Pedido.from_db_row(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def actualizar(pedido: Pedido) -> bool:
        if not pedido.id:
            raise ValueError("El pedido debe tener ID para actualizar")
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE Pedido
                SET id_cliente = ?, monto_total = ?, estado = ?, fecha_creacion = ?, fecha_expiracion = ?
                WHERE id = ?
                """,
                (pedido.id_cliente, pedido.monto_total, pedido.estado, pedido.fecha_creacion, pedido.fecha_expiracion, pedido.id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar pedido: {e}")
        finally:
            conn.close()

    @staticmethod
    def cambiar_estado(pedido_id: int, nuevo_estado: str) -> bool:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE Pedido SET estado = ? WHERE id = ?", (nuevo_estado, pedido_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def eliminar(pedido_id: int) -> bool:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Pedido WHERE id = ?", (pedido_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar pedido: {e}")
        finally:
            conn.close()
