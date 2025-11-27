"""
Repository (DAO) para la entidad Cliente.
Maneja todas las operaciones de base de datos relacionadas con clientes.
"""

from typing import List, Optional
from models.cliente import Cliente
from database.connection import get_connection


class ClienteRepository:
    """Repositorio para operaciones CRUD de Cliente"""
    
    @staticmethod
    def crear(cliente: Cliente) -> int:
        """
        Crea un nuevo cliente en la base de datos.
        
        Args:
            cliente: Objeto Cliente a crear
            
        Returns:
            ID del cliente creado
            
        Raises:
            Exception: Si hay error al insertar
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Cliente (nombre, apellido, dni, telefono, id_usuario)
                VALUES (?, ?, ?, ?, ?)
            """, (cliente.nombre, cliente.apellido, cliente.dni, 
                cliente.telefono, cliente.id_usuario))
            
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear cliente: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def obtener_por_id(cliente_id: int) -> Optional[Cliente]:
        """
        Obtiene un cliente por su ID.
        
        Args:
            cliente_id: ID del cliente
            
        Returns:
            Objeto Cliente o None si no existe
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Cliente WHERE id = ?", (cliente_id,))
            row = cursor.fetchone()
            
            if row:
                return Cliente.from_db_row(row)
            return None
        finally:
            conn.close()
    
    @staticmethod
    def obtener_por_dni(dni: str) -> Optional[Cliente]:
        """
        Obtiene un cliente por su DNI.
        
        Args:
            dni: DNI del cliente
            
        Returns:
            Objeto Cliente o None si no existe
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Cliente WHERE dni = ?", (dni,))
            row = cursor.fetchone()
            
            if row:
                return Cliente.from_db_row(row)
            return None
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id_usuario(id_usuario: int) -> Optional[Cliente]:
        """
        Obtiene un cliente asociado a un usuario dado.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Cliente WHERE id_usuario = ?", (id_usuario,))
            row = cursor.fetchone()
            return Cliente.from_db_row(row) if row else None
        finally:
            conn.close()
    
    @staticmethod
    def obtener_todos() -> List[Cliente]:
        """
        Obtiene todos los clientes.
        
        Returns:
            Lista de objetos Cliente
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Cliente ORDER BY nombre, apellido")
            rows = cursor.fetchall()
            
            return [Cliente.from_db_row(row) for row in rows]
        finally:
            conn.close()
    
    @staticmethod
    def buscar_por_nombre(nombre: str) -> List[Cliente]:
        """
        Busca clientes por nombre (coincidencia parcial).
        
        Args:
            nombre: Nombre o parte del nombre a buscar
            
        Returns:
            Lista de objetos Cliente que coinciden
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM Cliente 
                WHERE nombre LIKE ? OR apellido LIKE ?
                ORDER BY nombre, apellido
            """, (f"%{nombre}%", f"%{nombre}%"))
            rows = cursor.fetchall()
            
            return [Cliente.from_db_row(row) for row in rows]
        finally:
            conn.close()
    
    @staticmethod
    def actualizar(cliente: Cliente) -> bool:
        """
        Actualiza un cliente existente.
        
        Args:
            cliente: Objeto Cliente con datos actualizados (debe tener id)
            
        Returns:
            True si se actualizó, False si no existe
            
        Raises:
            ValueError: Si el cliente no tiene id
            Exception: Si hay error al actualizar
        """
        if not cliente.id:
            raise ValueError("El cliente debe tener un ID para actualizar")
        
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Cliente 
                SET nombre = ?, apellido = ?, dni = ?, telefono = ?
                WHERE id = ?
            """, (cliente.nombre, cliente.apellido, cliente.dni, 
                cliente.telefono, cliente.id))
            
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar cliente: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def eliminar(cliente_id: int) -> bool:
        """
        Elimina un cliente por su ID.
        
        Args:
            cliente_id: ID del cliente a eliminar
            
        Returns:
            True si se eliminó, False si no existe
            
        Raises:
            Exception: Si hay error al eliminar (ej: violación de FK)
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Cliente WHERE id = ?", (cliente_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar cliente: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def existe_dni(dni: str, excluir_id: Optional[int] = None) -> bool:
        """
        Verifica si ya existe un cliente con el DNI dado.
        
        Args:
            dni: DNI a verificar
            excluir_id: ID de cliente a excluir de la búsqueda (para updates)
            
        Returns:
            True si existe, False si no
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            if excluir_id:
                cursor.execute(
                    "SELECT COUNT(*) FROM Cliente WHERE dni = ? AND id != ?",
                    (dni, excluir_id)
                )
            else:
                cursor.execute("SELECT COUNT(*) FROM Cliente WHERE dni = ?", (dni,))
            
            count = cursor.fetchone()[0]
            return count > 0
        finally:
            conn.close()
    
    @staticmethod
    def contar() -> int:
        """
        Cuenta el total de clientes.
        
        Returns:
            Número total de clientes
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Cliente")
            return cursor.fetchone()[0]
        finally:
            conn.close()
