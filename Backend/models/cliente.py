from dataclasses import dataclass
from typing import Optional


@dataclass
class Cliente:
    """Modelo de entidad para Cliente"""
    id: Optional[int] = None
    nombre: str = ""
    apellido: Optional[str] = None
    dni: Optional[str] = None
    telefono: str = ""
    id_usuario: int = None
    
    def __post_init__(self):
        """Validación básica"""
        if self.id is not None:
            if not self.nombre:
                raise ValueError("El nombre es obligatorio")
            if not self.telefono:
                raise ValueError("El teléfono es obligatorio")
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'dni': self.dni,
            'telefono': self.telefono,
            'id_usuario': self.id_usuario
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un objeto Cliente desde un diccionario"""
        return cls(
            id=data.get('id'),
            nombre=data.get('nombre', ''),
            apellido=data.get('apellido'),
            dni=data.get('dni'),
            telefono=data.get('telefono', ''),
            id_usuario=data.get('id_usuario')
        )
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un objeto Cliente desde una fila de la base de datos"""
        return cls(
            id=row['id'],
            nombre=row['nombre'],
            apellido=row['apellido'],
            dni=row['dni'],
            telefono=row['telefono'],
            id_usuario=row['id_usuario']
        )
