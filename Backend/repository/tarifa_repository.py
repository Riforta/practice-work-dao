"""
Repository (DAO) para la entidad Tarifa.
Maneja todas las operaciones de base de datos relacionadas con tarifa.
"""

from typing import List, Optional
from models.tarifa import Tarifa
from database.connection import get_connection

class TarifaRepository:
    """Repositorio para operaciones CRUD de Tarifa"""

    @staticmethod
    def crear(tarifa: Tarifa) -> int:
        """
        Crea una nueva tarifa en la base de datos.
        
        Args:
            tarifa: Objeto Tarifa a crear
            
        Returns:
            ID de la tarifa creada
            
        Raises:
            Exception: Si hay error al insertar
        """

        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(""" INSERT INTO Tarifa (descripcion, monto, tipo_deporte, vigente) 
                            VALUES (?, ?, ?, ?)""",
                            (tarifa.descripcion, tarifa.monto, tarifa.tipo_deporte, tarifa.vigente))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear tarifa: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def actualizar(tarifa: Tarifa) -> None:
        """
        Actualiza una tarifa existente en la base de datos.
        
        Args:
            tarifa: Objeto Tarifa a actualizar
            
        Raises:
            Exception: Si hay error al actualizar
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Tarifa
                SET descripcion = ?, monto = ?, tipo_deporte = ?, vigente = ?
                WHERE id = ?
            """, (tarifa.descripcion, tarifa.monto, tarifa.tipo_deporte, tarifa.vigente, tarifa.id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar tarifa: {e}")
        finally:
            conn.close()

    @staticmethod
    def eliminar(tarifa_id: int) -> None:
        """
        Elimina una tarifa por su ID.
        
        Args:
            tarifa_id: ID de la tarifa a eliminar
            
        Raises:
            Exception: Si hay error al eliminar
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Tarifa WHERE id = ?", (tarifa_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar tarifa: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def obtener_por_id(tarifa_id: int) -> Optional[Tarifa]:
        """
        Obtiene una tarifa por su ID.
        
        Args:
            tarifa_id: ID de la tarifa
            
        Returns:
            Objeto Tarifa o None si no existe
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Tarifa WHERE id = ?", (tarifa_id,))
            row = cursor.fetchone()
            
            if row:
                return Tarifa.from_db_row(row)
            return None
        finally:
            conn.close()

    @staticmethod
    def obtener_por_descripcion(descripcion: str) -> Optional[Tarifa]:
        """
        Obtiene una tarifa por su descripción.
        
        Args:
            descripcion: Descripción de la tarifa
            
        Returns:
            Objeto Tarifa o None si no existe
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Tarifa WHERE descripcion = ?", (descripcion,))
            row = cursor.fetchone()
            
            if row:
                return Tarifa.from_db_row(row)
            return None
        finally:
            conn.close()
    
    @staticmethod
    def obtener_todas() -> List[Tarifa]:
        """
        Obtiene todas las tarifas de la base de datos.
        
        Returns:
            Lista de objetos Tarifa
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Tarifa")
            rows = cursor.fetchall()
            
            tarifas = [Tarifa.from_db_row(row) for row in rows]
            return tarifas
        finally:
            conn.close()
    

