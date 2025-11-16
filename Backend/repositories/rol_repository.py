from typing import List, Optional
from models.rol import Rol
from database.connection import get_connection


class RolRepository:
    """Repositorio para operaciones CRUD sobre la tabla Rol.

    Campos esperados en la tabla (según el DER): id, nombre, descripcion
    """

    @staticmethod
    def crear(rol: Rol) -> int:
        """Inserta un nuevo rol y devuelve su id."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO Rol (nombre_rol, descripcion)
                VALUES (?, ?)
                """,
                (rol.nombre_rol, rol.descripcion),
            )

            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear rol: {e}")
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(rol_id: int) -> Optional[Rol]:
        """Devuelve un objeto Rol o None si no existe."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, nombre_rol, descripcion FROM Rol WHERE id = ?",
                (rol_id,),
            )
            row = cursor.fetchone()

            if row:
                return Rol.from_db_row(row)
            return None
        finally:
            conn.close()

    @staticmethod
    def obtener_todos() -> List[Rol]:
        """Devuelve todos los roles ordenados por nombre."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, nombre_rol, descripcion FROM Rol ORDER BY nombre_rol"
            )
            rows = cursor.fetchall()

            return [Rol.from_db_row(row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def actualizar(rol: Rol) -> bool:
        """Actualiza un rol existente. Devuelve True si se actualizó."""
        if not getattr(rol, "id", None):
            raise ValueError("El rol debe tener un ID para actualizar")

        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE Rol
                SET nombre_rol = ?, descripcion = ?
                WHERE id = ?
                """,
                (rol.nombre_rol, rol.descripcion, rol.id),
            )

            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar rol: {e}")
        finally:
            conn.close()

    @staticmethod
    def eliminar(rol_id: int) -> bool:
        """Elimina un rol por id. Devuelve True si se eliminó."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Rol WHERE id = ?", (rol_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar rol: {e}")
        finally:
            conn.close()
    