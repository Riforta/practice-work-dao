"""
Repository (DAO) para la entidad Tarifa.
"""

from typing import List, Optional

from models.tarifa import Tarifa
from database.connection import get_connection


class TarifaRepository:
    """Repositorio para operaciones CRUD de Tarifa."""

    @staticmethod
    def _ensure_table(conn) -> None:
        """Crea la tabla Tarifa si no existe."""
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS Tarifa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cancha INTEGER NOT NULL,
                descripcion TEXT,
                precio_hora REAL NOT NULL DEFAULT 0,
                FOREIGN KEY (id_cancha) REFERENCES Cancha(id)
            )
            """
        )

    @staticmethod
    def ensure_schema() -> None:
        """Expone la creación de la tabla para inicializaciones puntuales."""
        conn = get_connection()
        try:
            TarifaRepository._ensure_table(conn)
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def crear(tarifa: Tarifa) -> int:
        conn = get_connection()
        try:
            TarifaRepository._ensure_table(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO Tarifa (id_cancha, descripcion, precio_hora)
                VALUES (?, ?, ?)
                """,
                (tarifa.id_cancha, tarifa.descripcion, tarifa.precio_hora),
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear tarifa: {e}")
        finally:
            conn.close()

    @staticmethod
    def actualizar(tarifa: Tarifa) -> bool:
        conn = get_connection()
        try:
            TarifaRepository._ensure_table(conn)
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE Tarifa
                SET id_cancha = ?, descripcion = ?, precio_hora = ?
                WHERE id = ?
                """,
                (tarifa.id_cancha, tarifa.descripcion, tarifa.precio_hora, tarifa.id),
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar tarifa: {e}")
        finally:
            conn.close()

    @staticmethod
    def eliminar(tarifa_id: int) -> bool:
        conn = get_connection()
        try:
            TarifaRepository._ensure_table(conn)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Tarifa WHERE id = ?", (tarifa_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar tarifa: {e}")
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(tarifa_id: int) -> Optional[Tarifa]:
        conn = get_connection()
        try:
            TarifaRepository._ensure_table(conn)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Tarifa WHERE id = ?", (tarifa_id,))
            row = cursor.fetchone()
            return Tarifa.from_db_row(row) if row else None
        except Exception as e:
            raise Exception(f"Error al obtener tarifa por ID: {e}")
        finally:
            conn.close()

    @staticmethod
    def obtener_por_cancha(id_cancha: int) -> List[Tarifa]:
        conn = get_connection()
        try:
            TarifaRepository._ensure_table(conn)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Tarifa WHERE id_cancha = ?", (id_cancha,))
            rows = cursor.fetchall()
            return [Tarifa.from_db_row(row) for row in rows]
        except Exception as e:
            raise Exception(f"Error al obtener tarifas por cancha: {e}")
        finally:
            conn.close()

    @staticmethod
    def listar_todas() -> List[Tarifa]:
        conn = get_connection()
        try:
            TarifaRepository._ensure_table(conn)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Tarifa")
            rows = cursor.fetchall()
            return [Tarifa.from_db_row(row) for row in rows]
        except Exception as e:
            raise Exception(f"Error al listar tarifas: {e}")
        finally:
            conn.close()

    @staticmethod
    def contar() -> int:
        conn = get_connection()
        try:
            TarifaRepository._ensure_table(conn)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Tarifa")
            return cursor.fetchone()[0]
        except Exception as e:
            raise Exception(f"Error al contar tarifas: {e}")
        finally:
            conn.close()

    @staticmethod
    def existe_para_cancha(id_cancha: int, excluir_id: Optional[int] = None) -> bool:
        conn = get_connection()
        try:
            TarifaRepository._ensure_table(conn)
            cursor = conn.cursor()
            if excluir_id is not None:
                cursor.execute(
                    "SELECT 1 FROM Tarifa WHERE id_cancha = ? AND id != ? LIMIT 1",
                    (id_cancha, excluir_id),
                )
            else:
                cursor.execute("SELECT 1 FROM Tarifa WHERE id_cancha = ? LIMIT 1", (id_cancha,))
            return cursor.fetchone() is not None
        except Exception as e:
            raise Exception(f"Error al verificar tarifa por cancha: {e}")
        finally:
            conn.close()
