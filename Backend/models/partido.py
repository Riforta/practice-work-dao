from dataclasses import dataclass
from typing import Optional


@dataclass
class Partido:
    """Modelo de entidad para Partido"""
    id: Optional[int] = None
    id_torneo: int = 0
    id_turno: Optional[int] = None
    id_equipo_local: Optional[int] = None
    id_equipo_visitante: Optional[int] = None
    id_equipo_ganador: Optional[int] = None
    ronda: Optional[str] = None
    marcador_local: Optional[int] = None
    marcador_visitante: Optional[int] = None
    estado: Optional[str] = None
    
    def __post_init__(self):
        """Validación básica"""
        if self.id is not None and not self.id_torneo:
            raise ValueError("El id de torneo es obligatorio")
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'id_torneo': self.id_torneo,
            'id_turno': self.id_turno,
            'id_equipo_local': self.id_equipo_local,
            'id_equipo_visitante': self.id_equipo_visitante,
            'id_equipo_ganador': self.id_equipo_ganador,
            'ronda': self.ronda,
            'marcador_local': self.marcador_local,
            'marcador_visitante': self.marcador_visitante,
            'estado': self.estado
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un objeto Partido desde un diccionario"""
        return cls(
            id=data.get('id'),
            id_torneo=data.get('id_torneo', 0),
            id_turno=data.get('id_turno'),
            id_equipo_local=data.get('id_equipo_local'),
            id_equipo_visitante=data.get('id_equipo_visitante'),
            id_equipo_ganador=data.get('id_equipo_ganador'),
            ronda=data.get('ronda'),
            marcador_local=data.get('marcador_local'),
            marcador_visitante=data.get('marcador_visitante'),
            estado=data.get('estado')
        )
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un objeto Partido desde una fila de la base de datos"""
        return cls(
            id=row['id'],
            id_torneo=row['id_torneo'],
            id_turno=row['id_turno'],
            id_equipo_local=row['id_equipo_local'],
            id_equipo_visitante=row['id_equipo_visitante'],
            id_equipo_ganador=row['id_equipo_ganador'],
            ronda=row['ronda'],
            marcador_local=row['marcador_local'],
            marcador_visitante=row['marcador_visitante'],
            estado=row['estado']
        )
