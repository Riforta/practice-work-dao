"""
Repository (DAO) para la entidad Equipo.
Maneja todas las operaciones de base de datos relacionadas con equipos.
"""

from typing import List, Optional
from models.equipo import Equipo
from database.connection import get_connection


class EquipoRepository:
    """Repositorio para operaciones CRUD de Equipo"""

    # CREATE
    @staticmethod
    def crear(equipo: Equipo) -> int:
        """
        Crea un nuevo equipo en la base de datos.

        Returns: ID del equipo creado
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO Equipo (nombre_equipo, id_capitan)
                VALUES (?, ?)
                """,
                (
                    equipo.nombre_equipo,
                    equipo.id_capitan,
                ),
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear equipo: {e}")
        finally:
            conn.close()

    # READ
    @staticmethod
    def obtener_por_id(equipo_id: int) -> Optional[Equipo]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Equipo WHERE id = ?", (equipo_id,))
            row = cursor.fetchone()
            return Equipo.from_db_row(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def obtener_por_nombre(nombre_equipo: str) -> Optional[Equipo]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM Equipo WHERE nombre_equipo = ?",
                (nombre_equipo,),
            )
            row = cursor.fetchone()
            return Equipo.from_db_row(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def obtener_todos() -> List[Equipo]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Equipo ORDER BY nombre_equipo")
            rows = cursor.fetchall()
            return [Equipo.from_db_row(r) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def buscar_por_nombre(nombre_parcial: str) -> List[Equipo]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            like = f"%{nombre_parcial}%"
            cursor.execute(
                "SELECT * FROM Equipo WHERE nombre_equipo LIKE ? ORDER BY nombre_equipo",
                (like,),
            )
            rows = cursor.fetchall()
            return [Equipo.from_db_row(r) for r in rows]
        finally:
            conn.close()

    # UPDATE
    @staticmethod
    def actualizar(equipo: Equipo) -> bool:
        if not equipo.id:
            raise ValueError("El equipo debe tener un ID para actualizar")
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE Equipo
                SET nombre_equipo = ?, id_capitan = ?
                WHERE id = ?
                """,
                (
                    equipo.nombre_equipo,
                    equipo.id_capitan,
                    equipo.id,
                ),
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar equipo: {e}")
        finally:
            conn.close()

    # DELETE
    @staticmethod
    def eliminar(equipo_id: int) -> bool:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Equipo WHERE id = ?", (equipo_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar equipo: {e}")
        finally:
            conn.close()

    # HELPERS
    @staticmethod
    def existe_nombre(nombre_equipo: str, excluir_id: Optional[int] = None) -> bool:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            if excluir_id is not None:
                cursor.execute(
                    "SELECT COUNT(*) FROM Equipo WHERE nombre_equipo = ? AND id != ?",
                    (nombre_equipo, excluir_id),
                )
            else:
                cursor.execute(
                    "SELECT COUNT(*) FROM Equipo WHERE nombre_equipo = ?",
                    (nombre_equipo,),
                )
            count = cursor.fetchone()[0]
            return count > 0
        finally:
            conn.close()

    @staticmethod
    def contar() -> int:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Equipo")
            return cursor.fetchone()[0]
        finally:
            conn.close()
