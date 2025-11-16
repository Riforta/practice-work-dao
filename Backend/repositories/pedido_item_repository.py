"""
Repository (DAO) para la entidad PedidoItem.
"""
from typing import List, Optional
from models.pedido_item import PedidoItem
from database.connection import get_connection


class PedidoItemRepository:
    @staticmethod
    def crear(item: PedidoItem) -> int:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO PedidoItem (id_pedido, id_turno, id_inscripcion, descripcion, monto)
                VALUES (?, ?, ?, ?, ?)
                """,
                (item.id_pedido, item.id_turno, item.id_inscripcion, item.descripcion, item.monto)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear item de pedido: {e}")
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(item_id: int) -> Optional[PedidoItem]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PedidoItem WHERE id = ?", (item_id,))
            row = cursor.fetchone()
            return PedidoItem.from_db_row(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def listar_por_pedido(id_pedido: int) -> List[PedidoItem]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PedidoItem WHERE id_pedido = ?", (id_pedido,))
            return [PedidoItem.from_db_row(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def actualizar(item: PedidoItem) -> bool:
        if not item.id:
            raise ValueError("El item debe tener ID para actualizar")
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE PedidoItem
                SET id_pedido = ?, id_turno = ?, id_inscripcion = ?, descripcion = ?, monto = ?
                WHERE id = ?
                """,
                (item.id_pedido, item.id_turno, item.id_inscripcion, item.descripcion, item.monto, item.id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar item de pedido: {e}")
        finally:
            conn.close()

    @staticmethod
    def eliminar(item_id: int) -> bool:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM PedidoItem WHERE id = ?", (item_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar item de pedido: {e}")
        finally:
            conn.close()
