from dataclasses import dataclass
from typing import Optional


@dataclass
class Equipo:
    """Modelo de entidad para Equipo"""
    id: Optional[int] = None
    nombre_equipo: str = ""
    id_capitan: Optional[int] = None
    
    def __post_init__(self):
        """Validación básica"""
        if self.id is not None and not self.nombre_equipo:
            raise ValueError("El nombre del equipo es obligatorio")
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'nombre_equipo': self.nombre_equipo,
            'id_capitan': self.id_capitan
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un objeto Equipo desde un diccionario"""
        return cls(
            id=data.get('id'),
            nombre_equipo=data.get('nombre_equipo', ''),
            id_capitan=data.get('id_capitan')
        )
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un objeto Equipo desde una fila de la base de datos"""
        return cls(
            id=row['id'],
            nombre_equipo=row['nombre_equipo'],
            id_capitan=row['id_capitan']
        )
