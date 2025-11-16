"""
Repository (DAO) para EquipoMiembro (tabla intermedia entre Equipo y Cliente).
"""
from typing import List
from models.equipo_miembro import EquipoMiembro
from database.connection import get_connection


class EquipoMiembroRepository:
    @staticmethod
    def agregar(miembro: EquipoMiembro) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO EquipoMiembro (id_equipo, id_cliente) VALUES (?, ?)",
                (miembro.id_equipo, miembro.id_cliente)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al agregar miembro a equipo: {e}")
        finally:
            conn.close()

    @staticmethod
    def listar_por_equipo(id_equipo: int) -> List[EquipoMiembro]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM EquipoMiembro WHERE id_equipo = ?",
                (id_equipo,)
            )
            return [EquipoMiembro.from_db_row(r) for r in cursor.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_equipo: int, id_cliente: int) -> bool:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM EquipoMiembro WHERE id_equipo = ? AND id_cliente = ?",
                (id_equipo, id_cliente)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar miembro del equipo: {e}")
        finally:
            conn.close()
