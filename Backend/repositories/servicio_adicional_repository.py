"""
Repository (DAO) para la entidad ServicioAdicional.
Maneja todas las operaciones de base de datos relacionadas con servicios adicionales.
"""

from typing import List, Optional
from models.servicio_adicional import ServicioAdicional
from database.connection import get_connection


class ServicioAdicionalRepository:
    """Repositorio para operaciones CRUD de ServicioAdicional"""

    # CREATE
    @staticmethod
    def crear(servicio: ServicioAdicional) -> int:
        """
        Crea un nuevo servicio adicional en la base de datos.

        Args:
            servicio: Objeto ServicioAdicional a crear

        Returns:
            ID del servicio creado
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO ServicioAdicional (nombre, precio_actual, activo)
                VALUES (?, ?, ?)
                """,
                (servicio.nombre, servicio.precio_actual, servicio.activo),
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear servicio adicional: {e}")
        finally:
            conn.close()

    # READ
    @staticmethod
    def obtener_por_id(servicio_id: int) -> Optional[ServicioAdicional]:
        """
        Obtiene un servicio adicional por su ID.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM ServicioAdicional WHERE id = ?", (servicio_id,)
            )
            row = cursor.fetchone()
            return ServicioAdicional.from_db_row(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def obtener_todos(activos: Optional[bool] = None) -> List[ServicioAdicional]:
        """
        Obtiene todos los servicios adicionales.

        Args:
            activos: Si es True, solo activos; si es False, solo inactivos; si es None, todos
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            if activos is True:
                cursor.execute(
                    "SELECT * FROM ServicioAdicional WHERE activo = 1 ORDER BY nombre"
                )
            elif activos is False:
                cursor.execute(
                    "SELECT * FROM ServicioAdicional WHERE activo = 0 ORDER BY nombre"
                )
            else:
                cursor.execute("SELECT * FROM ServicioAdicional ORDER BY nombre")
            rows = cursor.fetchall()
            return [ServicioAdicional.from_db_row(r) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def buscar_por_nombre(nombre: str) -> List[ServicioAdicional]:
        """
        Busca servicios por nombre (coincidencia parcial).
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            like = f"%{nombre}%"
            cursor.execute(
                """
                SELECT * FROM ServicioAdicional
                WHERE nombre LIKE ?
                ORDER BY nombre
                """,
                (like,),
            )
            rows = cursor.fetchall()
            return [ServicioAdicional.from_db_row(r) for r in rows]
        finally:
            conn.close()

    # UPDATE
    @staticmethod
    def actualizar(servicio: ServicioAdicional) -> bool:
        """
        Actualiza un servicio adicional existente.

        Raises:
            ValueError: Si el servicio no tiene id
        Returns:
            True si se actualizó, False si no existe
        """
        if not servicio.id:
            raise ValueError("El servicio debe tener un ID para actualizar")

        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE ServicioAdicional
                SET nombre = ?, precio_actual = ?, activo = ?
                WHERE id = ?
                """,
                (
                    servicio.nombre,
                    servicio.precio_actual,
                    servicio.activo,
                    servicio.id,
                ),
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar servicio adicional: {e}")
        finally:
            conn.close()

    # DELETE
    @staticmethod
    def eliminar(servicio_id: int) -> bool:
        """
        Elimina un servicio adicional por ID.
        Returns True si eliminó algún registro.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM ServicioAdicional WHERE id = ?", (servicio_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar servicio adicional: {e}")
        finally:
            conn.close()

    # Helpers
    @staticmethod
    def activar(servicio_id: int, activo: bool = True) -> bool:
        """
        Activa/Desactiva un servicio adicional.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE ServicioAdicional SET activo = ? WHERE id = ?",
                (1 if activo else 0, servicio_id),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def existe_nombre(nombre: str, excluir_id: Optional[int] = None) -> bool:
        """
        Verifica si existe un servicio con ese nombre.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            if excluir_id is not None:
                cursor.execute(
                    "SELECT COUNT(*) as c FROM ServicioAdicional WHERE nombre = ? AND id != ?",
                    (nombre, excluir_id),
                )
            else:
                cursor.execute(
                    "SELECT COUNT(*) as c FROM ServicioAdicional WHERE nombre = ?",
                    (nombre,),
                )
            count = cursor.fetchone()[0]
            return count > 0
        finally:
            conn.close()

    @staticmethod
    def contar(activos: Optional[bool] = None) -> int:
        """
        Cuenta servicios.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            if activos is True:
                cursor.execute(
                    "SELECT COUNT(*) FROM ServicioAdicional WHERE activo = 1"
                )
            elif activos is False:
                cursor.execute(
                    "SELECT COUNT(*) FROM ServicioAdicional WHERE activo = 0"
                )
            else:
                cursor.execute("SELECT COUNT(*) FROM ServicioAdicional")
            return cursor.fetchone()[0]
        finally:
            conn.close()
