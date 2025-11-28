from typing import List, Optional
from database.connection import get_connection
from models.equipo_torneo import EquipoTorneo


class EquipoTorneoRepository:
    """Repositorio para gestionar la relación entre Equipos y Torneos"""
    
    @staticmethod
    def inscribir_equipo(equipo_torneo: EquipoTorneo) -> EquipoTorneo:
        """Inscribe un equipo a un torneo"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO EquipoXTorneo (id_equipo, id_torneo, fecha_inscripcion)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (equipo_torneo.id_equipo, equipo_torneo.id_torneo))
            conn.commit()
            return equipo_torneo
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def inscribir_equipos_masivo(id_torneo: int, ids_equipos: List[int]) -> int:
        """Inscribe múltiples equipos a un torneo de forma masiva"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            inscripciones = [(id_equipo, id_torneo) for id_equipo in ids_equipos]
            cursor.executemany("""
                INSERT INTO EquipoXTorneo (id_equipo, id_torneo, fecha_inscripcion)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, inscripciones)
            conn.commit()
            return len(ids_equipos)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obtener_equipos_por_torneo(id_torneo: int) -> List[EquipoTorneo]:
        """Obtiene todos los equipos inscritos en un torneo"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id_equipo, id_torneo, fecha_inscripcion
                FROM EquipoXTorneo
                WHERE id_torneo = ?
                ORDER BY fecha_inscripcion
            """, (id_torneo,))
            rows = cursor.fetchall()
            return [EquipoTorneo.from_db_row(row) for row in rows]
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obtener_torneos_por_equipo(id_equipo: int) -> List[EquipoTorneo]:
        """Obtiene todos los torneos en los que está inscrito un equipo"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id_equipo, id_torneo, fecha_inscripcion
                FROM EquipoXTorneo
                WHERE id_equipo = ?
                ORDER BY fecha_inscripcion DESC
            """, (id_equipo,))
            rows = cursor.fetchall()
            return [EquipoTorneo.from_db_row(row) for row in rows]
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def existe_inscripcion(id_equipo: int, id_torneo: int) -> bool:
        """Verifica si un equipo ya está inscrito en un torneo"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT COUNT(*) FROM EquipoXTorneo
                WHERE id_equipo = ? AND id_torneo = ?
            """, (id_equipo, id_torneo))
            count = cursor.fetchone()[0]
            return count > 0
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def eliminar_inscripcion(id_equipo: int, id_torneo: int) -> bool:
        """Elimina la inscripción de un equipo a un torneo"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM EquipoXTorneo
                WHERE id_equipo = ? AND id_torneo = ?
            """, (id_equipo, id_torneo))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def eliminar_inscripciones_masivo(inscripciones: List[tuple]) -> int:
        """Elimina múltiples inscripciones de forma masiva
        
        Args:
            inscripciones: Lista de tuplas (id_equipo, id_torneo)
        
        Returns:
            Número de inscripciones eliminadas
        """
        if not inscripciones:
            return 0
            
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.executemany("""
                DELETE FROM EquipoXTorneo
                WHERE id_equipo = ? AND id_torneo = ?
            """, inscripciones)
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def contar_equipos_en_torneo(id_torneo: int) -> int:
        """Cuenta cuántos equipos están inscritos en un torneo"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT COUNT(*) FROM EquipoXTorneo
                WHERE id_torneo = ?
            """, (id_torneo,))
            return cursor.fetchone()[0]
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def eliminar_por_torneo(id_torneo: int) -> int:
        """Elimina todas las inscripciones de un torneo"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM EquipoXTorneo
                WHERE id_torneo = ?
            """, (id_torneo,))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def eliminar_por_equipo(id_equipo: int) -> int:
        """Elimina todas las inscripciones de un equipo"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM EquipoXTorneo
                WHERE id_equipo = ?
            """, (id_equipo,))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()
