from dataclasses import dataclass
from typing import Optional


@dataclass
class Tarifa:
    """Modelo de entidad para Tarifa"""
    id: Optional[int] = None
    id_cancha: int = 0
    descripcion: Optional[str] = None
    precio_hora: float = 0.0
    
    def __post_init__(self):
        """Validación básica"""
        if self.id is not None:
            if not self.id_cancha:
                raise ValueError("El id de cancha es obligatorio")
            if self.precio_hora < 0:
                raise ValueError("El precio por hora no puede ser negativo")
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'id_cancha': self.id_cancha,
            'descripcion': self.descripcion,
            'precio_hora': self.precio_hora
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un objeto Tarifa desde un diccionario"""
        return cls(
            id=data.get('id'),
            id_cancha=data.get('id_cancha', 0),
            descripcion=data.get('descripcion'),
            precio_hora=data.get('precio_hora', 0.0)
        )
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un objeto Tarifa desde una fila de la base de datos"""
        return cls(
            id=row['id'],
            id_cancha=row['id_cancha'],
            descripcion=row['descripcion'],
            precio_hora=row['precio_hora']
        )
