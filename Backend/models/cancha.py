from dataclasses import dataclass
from typing import Optional


@dataclass
class Cancha:
    """Modelo de entidad para Cancha"""
    id: Optional[int] = None
    nombre: str = ""
    tipo_deporte: Optional[str] = None
    descripcion: Optional[str] = None
    activa: int = 1
    precio_hora: Optional[float] = None
    
    def __post_init__(self):
        """Validación básica"""
        if self.id is not None and not self.nombre:
            raise ValueError("El nombre de la cancha es obligatorio")
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'tipo_deporte': self.tipo_deporte,
            'descripcion': self.descripcion,
            'activa': self.activa,
            'precio_hora': self.precio_hora
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un objeto Cancha desde un diccionario"""
        return cls(
            id=data.get('id'),
            nombre=data.get('nombre', ''),
            tipo_deporte=data.get('tipo_deporte'),
            descripcion=data.get('descripcion'),
            activa=data.get('activa', 1),
            precio_hora=data.get('precio_hora')
        )
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un objeto Cancha desde una fila de la base de datos"""
        return cls(
            id=row['id'],
            nombre=row['nombre'],
            tipo_deporte=row['tipo_deporte'],
            descripcion=row['descripcion'],
            activa=row['activa'],
            precio_hora=row['precio_hora']
        )
