from dataclasses import dataclass
from typing import Optional


@dataclass
class Torneo:
    """Modelo de entidad para Torneo"""
    id: Optional[int] = None
    nombre: str = ""
    tipo_deporte: str = ""
    created_at: Optional[str] = None
    fecha_inicio: Optional[str] = None
    fecha_fin: Optional[str] = None
    costo_inscripcion: float = 0.0
    cupos: Optional[int] = None
    reglas: Optional[str] = None
    estado: Optional[str] = None
    
    def __post_init__(self):
        """Validación básica"""
        if self.id is not None:
            if not self.nombre:
                raise ValueError("El nombre del torneo es obligatorio")
            if not self.tipo_deporte:
                raise ValueError("El tipo de deporte es obligatorio")
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'tipo_deporte': self.tipo_deporte,
            'created_at': self.created_at,
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
            'costo_inscripcion': self.costo_inscripcion,
            'cupos': self.cupos,
            'reglas': self.reglas,
            'estado': self.estado
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un objeto Torneo desde un diccionario"""
        return cls(
            id=data.get('id'),
            nombre=data.get('nombre', ''),
            tipo_deporte=data.get('tipo_deporte', ''),
            created_at=data.get('created_at'),
            fecha_inicio=data.get('fecha_inicio'),
            fecha_fin=data.get('fecha_fin'),
            costo_inscripcion=data.get('costo_inscripcion', 0.0),
            cupos=data.get('cupos'),
            reglas=data.get('reglas'),
            estado=data.get('estado')
        )
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un objeto Torneo desde una fila de la base de datos"""
        return cls(
            id=row['id'],
            nombre=row['nombre'],
            tipo_deporte=row['tipo_deporte'],
            created_at=row['created_at'],
            fecha_inicio=row['fecha_inicio'],
            fecha_fin=row['fecha_fin'],
            costo_inscripcion=row['costo_inscripcion'],
            cupos=row['cupos'],
            reglas=row['reglas'],
            estado=row['estado']
        )
