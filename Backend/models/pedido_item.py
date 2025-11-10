from dataclasses import dataclass
from typing import Optional


@dataclass
class PedidoItem:
    """Modelo de entidad para PedidoItem"""
    id: Optional[int] = None
    id_pedido: int = 0
    id_turno: Optional[int] = None
    id_inscripcion: Optional[int] = None
    descripcion: str = ""
    monto: float = 0.0
    
    def __post_init__(self):
        """Validación básica"""
        if self.id is not None:
            if not self.id_pedido:
                raise ValueError("El id de pedido es obligatorio")
            if not self.descripcion:
                raise ValueError("La descripción es obligatoria")
            if self.monto < 0:
                raise ValueError("El monto no puede ser negativo")
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'id_pedido': self.id_pedido,
            'id_turno': self.id_turno,
            'id_inscripcion': self.id_inscripcion,
            'descripcion': self.descripcion,
            'monto': self.monto
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un objeto PedidoItem desde un diccionario"""
        return cls(
            id=data.get('id'),
            id_pedido=data.get('id_pedido', 0),
            id_turno=data.get('id_turno'),
            id_inscripcion=data.get('id_inscripcion'),
            descripcion=data.get('descripcion', ''),
            monto=data.get('monto', 0.0)
        )
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un objeto PedidoItem desde una fila de la base de datos"""
        return cls(
            id=row['id'],
            id_pedido=row['id_pedido'],
            id_turno=row['id_turno'],
            id_inscripcion=row['id_inscripcion'],
            descripcion=row['descripcion'],
            monto=row['monto']
        )
