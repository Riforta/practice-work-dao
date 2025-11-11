from dataclasses import dataclass
from typing import Optional


@dataclass
class Inscripcion:
    """Modelo de entidad para Inscripcion"""
    id: Optional[int] = None
    id_equipo: int = 0
    id_torneo: int = 0
    fecha_inscripcion: Optional[str] = None
    estado: str = "pendiente_pago"
    
    def __post_init__(self):
        """Validación básica"""
        if self.id is not None:
            if not self.id_equipo:
                raise ValueError("El id de equipo es obligatorio")
            if not self.id_torneo:
                raise ValueError("El id de torneo es obligatorio")
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'id_equipo': self.id_equipo,
            'id_torneo': self.id_torneo,
            'fecha_inscripcion': self.fecha_inscripcion,
            'estado': self.estado
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un objeto Inscripcion desde un diccionario"""
        return cls(
            id=data.get('id'),
            id_equipo=data.get('id_equipo', 0),
            id_torneo=data.get('id_torneo', 0),
            fecha_inscripcion=data.get('fecha_inscripcion'),
            estado=data.get('estado', 'pendiente_pago')
        )
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un objeto Inscripcion desde una fila de la base de datos"""
        return cls(
            id=row['id'],
            id_equipo=row['id_equipo'],
            id_torneo=row['id_torneo'],
            fecha_inscripcion=row['fecha_inscripcion'],
            estado=row['estado']
        )
