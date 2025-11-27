"""
Repository (DAO) para la entidad Cancha.
Maneja todas las operaciones de base de datos relacionadas con canchas.
"""

from typing import List, Optional
from models.cancha import Cancha
from database.connection import get_connection

class CanchaRepository:
    """Repositorio para operaciones CRUD de Cancha"""
    
    @staticmethod
    def crear(cancha: Cancha) -> int:
        """
        Crea una nueva cancha en la base de datos.
        
        Args:
            cancha: Objeto Cancha a crear
            
        Returns:
            ID de la cancha creada
            
        Raises:
            Exception: Si hay error al insertar
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Cancha (nombre, tipo_deporte, descripcion, activa)
                VALUES (?, ?, ?, ?)
            """, (cancha.nombre, cancha.tipo_deporte, 
                cancha.descripcion, cancha.activa))
            
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear cancha: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def actualizar(cancha: Cancha) -> None:
        """
        Actualiza una cancha existente en la base de datos.
        
        Args:
            cancha: Objeto Cancha a actualizar
            
        Raises:
            Exception: Si hay error al actualizar
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Cancha
                SET nombre = ?, tipo_deporte = ?, descripcion = ?, activa = ?
                WHERE id = ?
            """, (cancha.nombre, cancha.tipo_deporte, 
                cancha.descripcion, cancha.activa, cancha.id))
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar cancha: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def eliminar(cancha_id: int) -> None:
        """
        Elimina una cancha de la base de datos.
        
        Args:
            cancha_id: ID de la cancha a eliminar
            
        Raises:
            Exception: Si hay error al eliminar
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Cancha WHERE id = ?", (cancha_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar cancha: {e}")
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(cancha_id: int) -> Optional[Cancha]:
        """
        Obtiene una cancha por su ID.
        
        Args:
            cancha_id: ID de la cancha
            
        Returns:
            Objeto Cancha o None si no existe
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Cancha WHERE id = ?", (cancha_id,))
            row = cursor.fetchone()
            if row:
                return Cancha.from_db_row(row)
            return None
        except Exception as e:
            raise Exception(f"Error al obtener cancha por ID: {e}")
    
        finally:
            conn.close()

    @staticmethod
    def obtener_por_nombre(nombre: str) -> Optional[Cancha]:
        """
        Obtiene una cancha por su nombre.
        
        Args:
            nombre: Nombre de la cancha
            
        Returns:
            Objeto Cancha o None si no existe
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Cancha WHERE nombre = ?", (nombre,))
            row = cursor.fetchone()
            if row:
                return Cancha.from_db_row(row)
            return None
        except Exception as e:
            raise Exception(f"Error al obtener cancha por nombre: {e}")
        finally:
            conn.close()

    @staticmethod
    def listar_todas() -> List[Cancha]:
        """
        Lista todas las canchas en la base de datos.
        
        Returns:
            Lista de objetos Cancha
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Cancha")
            rows = cursor.fetchall()
            canchas = [Cancha.from_db_row(row) for row in rows]
            return canchas
        except Exception as e:
            raise Exception(f"Error al listar canchas: {e}")
        finally:
            conn.close()