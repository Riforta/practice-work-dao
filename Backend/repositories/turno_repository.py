"""
Repository (DAO) para la entidad Turno.
Maneja todas las operaciones de base de datos relacionadas con turnos/reservas.
"""

from typing import List, Optional
from models.turno import Turno
from database.connection import get_connection


class TurnoRepository:
    """Repositorio para operaciones CRUD de Turno"""

    @staticmethod
    def obtener_por_id(turno_id: int) -> Optional[Turno]:
        """
        Obtiene un turno (reserva, bloqueo, etc.) por su ID.
        
        Args:
            turno_id: ID del turno
            
        Returns:
            Objeto Turno o None si no existe
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Turno WHERE id = ?", (turno_id,))
            row = cursor.fetchone()
            
            if row:
                return Turno.from_db_row(row)
            return None
        finally:
            conn.close()

    @staticmethod
    def actualizar(turno: Turno) -> bool:
        """
        Actualiza un turno completo en la base de datos.
        
        Args:
            turno: Objeto Turno con datos actualizados (debe tener id)
            
        Returns:
            True si se actualizó, False si no existe
            
        Raises:
            ValueError: Si el turno no tiene id
            Exception: Si hay error al actualizar
        """
        if not turno.id:
            raise ValueError("El turno debe tener un ID para actualizar")
            
        conn = get_connection()
        try:
            cursor = conn.cursor()
            sql = """
                UPDATE Turno SET
                    id_cancha = ?, 
                    fecha_hora_inicio = ?, 
                    fecha_hora_fin = ?, 
                    estado = ?, 
                    precio_final = ?, 
                    id_cliente = ?, 
                    id_usuario_registro = ?, 
                    reserva_created_at = ?, 
                    id_usuario_bloqueo = ?, 
                    motivo_bloqueo = ?
                WHERE id = ?
            """
            
            cursor.execute(sql, (
                turno.id_cancha,
                turno.fecha_hora_inicio,
                turno.fecha_hora_fin,
                turno.estado,
                turno.precio_final,
                turno.id_cliente,
                turno.id_usuario_registro,
                turno.reserva_created_at,
                turno.id_usuario_bloqueo,
                turno.motivo_bloqueo,
                turno.id
            ))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar el turno: {e}")
        finally:
            conn.close()

    @staticmethod
    def crear(turno: Turno) -> int:
        """
        Crea un nuevo turno en la base de datos.
        
        Args:
            turno: Objeto Turno a crear
            
        Returns:
            ID del turno creado
            
        Raises:
            Exception: Si hay error al insertar
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Turno (
                    id_cancha, fecha_hora_inicio, fecha_hora_fin, estado,
                    precio_final, id_cliente, id_usuario_registro, 
                    reserva_created_at, id_usuario_bloqueo, motivo_bloqueo
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                turno.id_cancha, turno.fecha_hora_inicio, turno.fecha_hora_fin,
                turno.estado, turno.precio_final, turno.id_cliente,
                turno.id_usuario_registro, turno.reserva_created_at,
                turno.id_usuario_bloqueo, turno.motivo_bloqueo
            ))
            
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear turno: {e}")
        finally:
            conn.close()

    @staticmethod
    def obtener_por_cancha(id_cancha: int, estado: Optional[str] = None) -> List[Turno]:
        """
        Obtiene todos los turnos de una cancha, opcionalmente filtrados por estado.
        
        Args:
            id_cancha: ID de la cancha
            estado: Estado del turno (opcional)
            
        Returns:
            Lista de objetos Turno
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            if estado:
                cursor.execute(
                    "SELECT * FROM Turno WHERE id_cancha = ? AND estado = ? ORDER BY fecha_hora_inicio",
                    (id_cancha, estado)
                )
            else:
                cursor.execute(
                    "SELECT * FROM Turno WHERE id_cancha = ? ORDER BY fecha_hora_inicio",
                    (id_cancha,)
                )
            
            rows = cursor.fetchall()
            return [Turno.from_db_row(row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def obtener_disponibles() -> List[Turno]:
        """
        Obtiene todos los turnos disponibles.
        
        Returns:
            Lista de objetos Turno con estado 'disponible'
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM Turno WHERE estado = 'disponible' ORDER BY fecha_hora_inicio"
            )
            rows = cursor.fetchall()
            return [Turno.from_db_row(row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def obtener_por_cliente(id_cliente: int) -> List[Turno]:
        """
        Obtiene todos los turnos reservados por un cliente.
        
        Args:
            id_cliente: ID del cliente
            
        Returns:
            Lista de objetos Turno
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM Turno WHERE id_cliente = ? ORDER BY fecha_hora_inicio DESC",
                (id_cliente,)
            )
            rows = cursor.fetchall()
            return [Turno.from_db_row(row) for row in rows]
        finally:
            conn.close()
    
    @staticmethod
    def obtener_todos_filtrados(
        id_cancha: Optional[int] = None,
        estado: Optional[str] = None,
        id_cliente: Optional[int] = None
    ) -> List[Turno]:
        """
        Obtiene una lista de turnos, permitiendo filtrar por cancha,
        estado y/o cliente.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            
            # Construcción dinámica de la consulta SQL
            sql = "SELECT * FROM Turno"
            params = []
            conditions = []

            if id_cancha is not None:
                conditions.append("id_cancha = ?")
                params.append(id_cancha)
            
            if estado is not None:
                conditions.append("estado = ?")
                params.append(estado)
                
            if id_cliente is not None:
                conditions.append("id_cliente = ?")
                params.append(id_cliente)

            # Si hay filtros, los añadimos al SQL
            if conditions:
                sql += " WHERE " + " AND ".join(conditions)
            
            # Siempre es buena idea ordenar los turnos
            sql += " ORDER BY fecha_hora_inicio"
            
            cursor.execute(sql, tuple(params))
            rows = cursor.fetchall()
            
            # Convertimos cada fila en un objeto Turno
            return [Turno.from_db_row(row) for row in rows]
        except Exception as e:
            raise Exception(f"Error al obtener turnos filtrados: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def eliminar(turno_id: int) -> bool:
        """Elimina un turno.
        
        Args:
            turno_id: ID del turno a eliminar
            
        Returns:
            True si se eliminó correctamente
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Turno WHERE id = ?", (turno_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def existe_solapado(
        id_cancha: int,
        fecha_hora_inicio: str,
        fecha_hora_fin: str,
        excluir_id: Optional[int] = None
    ) -> bool:
        """
        Verifica si existe algún turno en la misma cancha cuyo rango [inicio, fin)
        se solape con el rango proporcionado.

        Se considera solape si:
        nuevo_inicio < existente_fin AND nuevo_fin > existente_inicio
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            sql = """
                SELECT COUNT(*) as c
                FROM Turno
                WHERE id_cancha = ?
                  AND fecha_hora_inicio < ?
                  AND fecha_hora_fin > ?
            """
            params = [id_cancha, fecha_hora_fin, fecha_hora_inicio]

            if excluir_id is not None:
                sql += " AND id != ?"
                params.append(excluir_id)

            cursor.execute(sql, tuple(params))
            row = cursor.fetchone()
            return (row[0] if row else 0) > 0
        finally:
            conn.close()
