"""
Repository de Partidos (DAO).
Maneja todas las operaciones de base de datos relacionadas con partidos.
"""

from typing import List, Optional
from models.partido import Partido
from database.connection import get_connection

class PartidoRepository:
    """Repositorio para operaciones CRUD de Partido"""

    @staticmethod
    def crear(partido: Partido) -> int:
        """
        Crea un nuevo partido en la base de datos.
        
        Args:
            partido: Objeto Partido a crear
            
        Returns:
            ID del partido creado
            
        Raises:
            Exception: Si hay error al insertar
        """

        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(""" INSERT INTO Partido (torneo_id, equipo_local, equipo_visitante, 
                        fecha_hora, cancha_id, estado) VALUES (?, ?, ?, ?, ?, ?)""",
                            (partido.torneo_id, partido.equipo_local, partido.equipo_visitante,
                            partido.fecha_hora, partido.cancha_id, partido.estado))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear partido: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def actualizar(partido: Partido) -> None:
        """
        Actualiza un partido existente en la base de datos.
        
        Args:
            partido: Objeto Partido a actualizar
            
        Raises:
            Exception: Si hay error al actualizar
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Partido
                SET torneo_id = ?, equipo_local = ?, equipo_visitante = ?, 
                    fecha_hora = ?, cancha_id = ?, estado = ?
                WHERE id = ?
            """, (partido.torneo_id, partido.equipo_local, partido.equipo_visitante,
                partido.fecha_hora, partido.cancha_id, partido.estado, partido.id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar partido: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def eliminar(partido_id: int) -> None:
        """
        Elimina un partido por su ID.
        
        Args:
            partido_id: ID del partido a eliminar
            
        Raises:
            Exception: Si hay error al eliminar
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Partido WHERE id = ?", (partido_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar partido: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def obtener_por_id(partido_id: int) -> Optional[Partido]:
        """
        Obtiene un partido por su ID.
        
        Args:
            partido_id: ID del partido
            
        Returns:
            Objeto Partido o None si no existe
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Partido WHERE id = ?", (partido_id,))
            row = cursor.fetchone()
            
            if row:
                return Partido.from_db_row(row)
            return None
        finally:
            conn.close()
    
    @staticmethod
    def obtener_todos() -> List[Partido]:
        """
        Obtiene todos los partidos.
        
        Returns:
            Lista de objetos Partido
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Partido")
            rows = cursor.fetchall()
            
            partidos = [Partido.from_db_row(row) for row in rows]
            return partidos
        finally:
            conn.close()
    
    @staticmethod
    def obtener_por_torneo(torneo_id: int) -> List[Partido]:
        """
        Obtiene todos los partidos de un torneo específico.
        
        Args:
            torneo_id: ID del torneo
            
        Returns:
            Lista de objetos Partido
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Partido WHERE torneo_id = ?", (torneo_id,))
            rows = cursor.fetchall()
            
            partidos = [Partido.from_db_row(row) for row in rows]
            return partidos
        finally:
            conn.close()