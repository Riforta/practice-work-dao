"""
Repository (DAO) para la entidad Torneo.
Maneja todas las operaciones de base de datos relacionadas con torneos.
"""

from typing import List, Optional
from models.torneo import Torneo
from database.connection import get_connection

class TorneoRepository:
    """Repositorio para operaciones CRUD de Torneo"""

    @staticmethod
    def crear(torneo: Torneo) -> int:
        """
        Crea un nuevo torneo en la base de datos.
        
        Args:
            torneo: Objeto Torneo a crear
            
        Returns:
            ID del torneo creado
            
        Raises:
            Exception: Si hay error al insertar
        """

        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(""" INSERT INTO Torneo (nombre, tipo_deporte, created_at, fecha_inicio,
                        fecha_fin, costo_inscripcion, cupos, reglas, estado) VALUES (?, ?, ?, ?, ?,
                            ?, ?, ? ,?)""",
                            (torneo.nombre, torneo.tipo_deporte, torneo.created_at, torneo.fecha_inicio,
                                torneo.fecha_fin, torneo.costo_inscripcion, torneo.cupos,
                                torneo.reglas, torneo.estado))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear torneo: {e}")
        finally:
            conn.close()

    @staticmethod
    def actualizar(torneo: Torneo) -> None:
        """
        Actualiza un torneo existente en la base de datos.
        
        Args:
            torneo: Objeto Torneo a actualizar
            
        Raises:
            Exception: Si hay error al actualizar
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Torneo
                SET nombre = ?, tipo_deporte = ?, created_at = ?, fecha_inicio = ?, fecha_fin = ?,
                    costo_inscripcion = ?, cupos = ?, reglas = ?, estado = ?
                WHERE id = ?
            """, (torneo.nombre, torneo.tipo_deporte, torneo.created_at, torneo.fecha_inicio,
                torneo.fecha_fin, torneo.costo_inscripcion, torneo.cupos,
                torneo.reglas, torneo.estado, torneo.id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar torneo: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def eliminar(torneo_id: int) -> None:
        """
        Elimina un torneo de la base de datos.
        
        Args:
            torneo_id: ID del torneo a eliminar
            
        Raises:
            Exception: Si hay error al eliminar
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Torneo WHERE id = ?", (torneo_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar torneo: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def obtener_por_id(torneo_id: int) -> Optional[Torneo]:
        """
        Obtiene un torneo por su ID.
        
        Args:
            torneo_id: ID del torneo a buscar
            
        Returns:
            Objeto Torneo si se encuentra, None si no existe
            
        Raises:
            Exception: Si hay error al consultar
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Torneo WHERE id = ?", (torneo_id,))
            row = cursor.fetchone()
            if row:
                return Torneo.from_db_row(row)
            return None
        except Exception as e:
            raise Exception(f"Error al obtener torneo: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def obtener_por_nombre(nombre: str) -> Optional[Torneo]:
        """
        Obtiene un torneo por su nombre.
        
        Args:
            nombre: Nombre del torneo a buscar
            
        Returns:
            Objeto Torneo si se encuentra, None si no existe
            
        Raises:
            Exception: Si hay error al consultar
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Torneo WHERE nombre = ?", (nombre,))
            row = cursor.fetchone()
            if row:
                return Torneo.from_db_row(row)
            return None
        except Exception as e:
            raise Exception(f"Error al obtener torneo por nombre: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def listar_todos() -> List[Torneo]:
        """
        Lista todos los torneos en la base de datos.
        
        Returns:
            Lista de objetos Torneo
            
        Raises:
            Exception: Si hay error al consultar
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Torneo")
            rows = cursor.fetchall()
            return [Torneo.from_db_row(row) for row in rows]
        except Exception as e:
            raise Exception(f"Error al listar torneos: {e}")
        finally:
            conn.close()