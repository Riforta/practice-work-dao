from typing import Optional
from datetime import datetime


class EquipoTorneo:
    """Modelo para la tabla intermedia EquipoXTorneo (relación N:M entre Equipo y Torneo)"""
    
    def __init__(
        self,
        id_equipo: int,
        id_torneo: int,
        fecha_inscripcion: Optional[str] = None
    ):
        self.id_equipo = id_equipo
        self.id_torneo = id_torneo
        self.fecha_inscripcion = fecha_inscripcion

    def to_dict(self):
        return {
            'id_equipo': self.id_equipo,
            'id_torneo': self.id_torneo,
            'fecha_inscripcion': self.fecha_inscripcion
        }

    @staticmethod
    def from_dict(data: dict):
        return EquipoTorneo(
            id_equipo=data['id_equipo'],
            id_torneo=data['id_torneo'],
            fecha_inscripcion=data.get('fecha_inscripcion')
        )

    @staticmethod
    def from_db_row(row: tuple):
        """Crea una instancia desde una fila de la base de datos
        
        Args:
            row: Tupla con (id_equipo, id_torneo, fecha_inscripcion)
        """
        return EquipoTorneo(
            id_equipo=row[0],
            id_torneo=row[1],
            fecha_inscripcion=row[2]
        )
