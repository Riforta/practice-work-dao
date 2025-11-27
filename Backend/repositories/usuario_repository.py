"""
Repository (DAO) para la entidad Usuario.
Maneja todas las operaciones de base de datos relacionadas con usuarios.
"""

from typing import List, Optional
from models.usuario import Usuario
from database.connection import get_connection


class UsuarioRepository:
    """Repositorio para operaciones CRUD de Usuario"""

    # CREATE
    @staticmethod
    def crear(usuario: Usuario) -> int:
        """
        Crea un nuevo usuario en la base de datos.

        Returns: ID del usuario creado
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO Usuario (nombre_usuario, email, password_hash, id_rol)
                VALUES (?, ?, ?, ?)
                """,
                (
                    usuario.nombre_usuario,
                    usuario.email,
                    usuario.password_hash,
                    usuario.id_rol
                ),
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear usuario: {e}")
        finally:
            conn.close()

    # READ
    @staticmethod
    def obtener_por_id(usuario_id: int) -> Optional[Usuario]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Usuario WHERE id = ?", (usuario_id,))
            row = cursor.fetchone()
            return Usuario.from_db_row(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def obtener_por_email(email: str) -> Optional[Usuario]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Usuario WHERE email = ?", (email,))
            row = cursor.fetchone()
            return Usuario.from_db_row(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def obtener_por_nombre_usuario(nombre_usuario: str) -> Optional[Usuario]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM Usuario WHERE nombre_usuario = ?", (nombre_usuario,)
            )
            row = cursor.fetchone()
            return Usuario.from_db_row(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def obtener_todos() -> List[Usuario]:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Usuario ORDER BY nombre_usuario")
            rows = cursor.fetchall()
            return [Usuario.from_db_row(r) for r in rows]
        finally:
            conn.close()

    # UPDATE
    @staticmethod
    def actualizar(usuario: Usuario) -> bool:
        if not usuario.id:
            raise ValueError("El usuario debe tener un ID para actualizar")
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE Usuario
                SET nombre_usuario = ?, email = ?, password_hash = ?, id_rol = ?
                WHERE id = ?
                """,
                (
                    usuario.nombre_usuario,
                    usuario.email,
                    usuario.password_hash,
                    usuario.id_rol,
                    usuario.id,
                ),
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar usuario: {e}")
        finally:
            conn.close()

    @staticmethod
    def cambiar_password(usuario_id: int, nuevo_hash: str) -> bool:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Usuario SET password_hash = ? WHERE id = ?",
                (nuevo_hash, usuario_id),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    # DELETE
    @staticmethod
    def eliminar(usuario_id: int) -> bool:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Usuario WHERE id = ?", (usuario_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar usuario: {e}")
        finally:
            conn.close()

    # HELPERS
    @staticmethod
    def existe_email(email: str, excluir_id: Optional[int] = None) -> bool:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            if excluir_id is not None:
                cursor.execute(
                    "SELECT COUNT(*) FROM Usuario WHERE email = ? AND id != ?",
                    (email, excluir_id),
                )
            else:
                cursor.execute("SELECT COUNT(*) FROM Usuario WHERE email = ?", (email,))
            count = cursor.fetchone()[0]
            return count > 0
        finally:
            conn.close()

    @staticmethod
    def existe_nombre_usuario(nombre_usuario: str, excluir_id: Optional[int] = None) -> bool:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            if excluir_id is not None:
                cursor.execute(
                    "SELECT COUNT(*) FROM Usuario WHERE nombre_usuario = ? AND id != ?",
                    (nombre_usuario, excluir_id),
                )
            else:
                cursor.execute(
                    "SELECT COUNT(*) FROM Usuario WHERE nombre_usuario = ?",
                    (nombre_usuario,),
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
            cursor.execute("SELECT COUNT(*) FROM Usuario")
            return cursor.fetchone()[0]
        finally:
            conn.close()
