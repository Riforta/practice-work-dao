from dataclasses import dataclass
from typing import Optional


@dataclass
class Rol:
    """Modelo de entidad para Rol"""
    id: Optional[int] = None
    nombre_rol: str = ""
    descripcion: Optional[str] = None
    
    def __post_init__(self):
        """Validación básica"""
        if not self.nombre_rol and self.id is not None:
            raise ValueError("El nombre del rol es obligatorio")
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'nombre_rol': self.nombre_rol,
            'descripcion': self.descripcion
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un objeto Rol desde un diccionario"""
        return cls(
            id=data.get('id'),
            nombre_rol=data.get('nombre_rol', ''),
            descripcion=data.get('descripcion')
        )
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un objeto Rol desde una fila de la base de datos"""
        return cls(
            id=row['id'],
            nombre_rol=row['nombre_rol'],
            descripcion=row['descripcion']
        )
