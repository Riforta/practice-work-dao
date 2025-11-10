from dataclasses import dataclass
from typing import Optional


@dataclass
class ServicioAdicional:
    """Modelo de entidad para ServicioAdicional"""
    id: Optional[int] = None
    nombre: str = ""
    precio_actual: float = 0.0
    activo: int = 1
    
    def __post_init__(self):
        """Validación básica"""
        if self.id is not None:
            if not self.nombre:
                raise ValueError("El nombre del servicio es obligatorio")
            if self.precio_actual < 0:
                raise ValueError("El precio no puede ser negativo")
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio_actual': self.precio_actual,
            'activo': self.activo
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un objeto ServicioAdicional desde un diccionario"""
        return cls(
            id=data.get('id'),
            nombre=data.get('nombre', ''),
            precio_actual=data.get('precio_actual', 0.0),
            activo=data.get('activo', 1)
        )
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un objeto ServicioAdicional desde una fila de la base de datos"""
        return cls(
            id=row['id'],
            nombre=row['nombre'],
            precio_actual=row['precio_actual'],
            activo=row['activo']
        )
