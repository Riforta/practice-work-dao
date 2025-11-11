"""
Repository de Partidos (DAO).
Maneja todas las operaciones de base de datos relacionadas con partidos.
"""

from typing import List, Optional
from models.partido import Partido
from database.connection import get_connection

class PartidoRepository:
    """Repositorio para operaciones CRUD de Partido.

    Modelo Partido (models/partido.py):
    - id_torneo, id_turno, id_equipo_local, id_equipo_visitante,
      id_equipo_ganador, ronda, marcador_local, marcador_visitante, estado
    """

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
            cursor.execute(
                """
                INSERT INTO Partido (
                    id_torneo, id_turno, id_equipo_local, id_equipo_visitante,
                    id_equipo_ganador, ronda, marcador_local, marcador_visitante, estado
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    partido.id_torneo, partido.id_turno, partido.id_equipo_local,
                    partido.id_equipo_visitante, partido.id_equipo_ganador,
                    partido.ronda, partido.marcador_local, partido.marcador_visitante,
                    partido.estado,
                ),
            )
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
            cursor.execute(
                """
                UPDATE Partido SET
                    id_torneo = ?, id_turno = ?, id_equipo_local = ?, id_equipo_visitante = ?,
                    id_equipo_ganador = ?, ronda = ?, marcador_local = ?, marcador_visitante = ?, estado = ?
                WHERE id = ?
                """,
                (
                    partido.id_torneo, partido.id_turno, partido.id_equipo_local,
                    partido.id_equipo_visitante, partido.id_equipo_ganador,
                    partido.ronda, partido.marcador_local, partido.marcador_visitante,
                    partido.estado, partido.id,
                ),
            )
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
            cursor.execute("SELECT * FROM Partido WHERE id_torneo = ?", (torneo_id,))
            rows = cursor.fetchall()
            
            partidos = [Partido.from_db_row(row) for row in rows]
            return partidos
        finally:
            conn.close()