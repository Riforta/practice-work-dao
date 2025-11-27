"""
Repository (DAO) para la entidad Inscripcion.
"""
from typing import List, Optional
from models.inscripcion import Inscripcion
from database.connection import get_connection


class InscripcionRepository:
    @staticmethod
    def crear(ins: Inscripcion) -> int:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO Inscripcion (id_equipo, id_torneo, fecha_inscripcion, estado)
                VALUES (?, ?, ?, ?)
                """,
                (ins.id_equipo, ins.id_torneo, ins.fecha_inscripcion, ins.estado)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear inscripción: {e}")
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(inscripcion_id: int) -> Optional[Inscripcion]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Inscripcion WHERE id = ?", (inscripcion_id,))
            row = cursor.fetchone()
            return Inscripcion.from_db_row(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def listar_por_torneo(id_torneo: int) -> List[Inscripcion]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM Inscripcion WHERE id_torneo = ? ORDER BY fecha_inscripcion",
                (id_torneo,)
            )
            return [Inscripcion.from_db_row(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def listar_todas() -> List[Inscripcion]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Inscripcion ORDER BY fecha_inscripcion")
            return [Inscripcion.from_db_row(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def actualizar(ins: Inscripcion) -> bool:
        if not ins.id:
            raise ValueError("La inscripción debe tener ID para actualizar")
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE Inscripcion
                SET id_equipo = ?, id_torneo = ?, fecha_inscripcion = ?, estado = ?
                WHERE id = ?
                """,
                (ins.id_equipo, ins.id_torneo, ins.fecha_inscripcion, ins.estado, ins.id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar inscripción: {e}")
        finally:
            conn.close()

    @staticmethod
    def cambiar_estado(inscripcion_id: int, nuevo_estado: str) -> bool:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Inscripcion SET estado = ? WHERE id = ?",
                (nuevo_estado, inscripcion_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def eliminar(inscripcion_id: int) -> bool:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Inscripcion WHERE id = ?", (inscripcion_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar inscripción: {e}")
        finally:
            conn.close()
