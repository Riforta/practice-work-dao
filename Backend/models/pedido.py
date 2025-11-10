from dataclasses import dataclass
from typing import Optional


@dataclass
class Pedido:
    """Modelo de entidad para Pedido"""
    id: Optional[int] = None
    id_cliente: int = 0
    monto_total: float = 0.0
    estado: str = "pendiente_pago"
    fecha_creacion: Optional[str] = None
    fecha_expiracion: Optional[str] = None
    
    def __post_init__(self):
        """Validación básica"""
        if self.id is not None:
            if not self.id_cliente:
                raise ValueError("El id de cliente es obligatorio")
            if self.monto_total < 0:
                raise ValueError("El monto total no puede ser negativo")
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'id_cliente': self.id_cliente,
            'monto_total': self.monto_total,
            'estado': self.estado,
            'fecha_creacion': self.fecha_creacion,
            'fecha_expiracion': self.fecha_expiracion
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un objeto Pedido desde un diccionario"""
        return cls(
            id=data.get('id'),
            id_cliente=data.get('id_cliente', 0),
            monto_total=data.get('monto_total', 0.0),
            estado=data.get('estado', 'pendiente_pago'),
            fecha_creacion=data.get('fecha_creacion'),
            fecha_expiracion=data.get('fecha_expiracion')
        )
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un objeto Pedido desde una fila de la base de datos"""
        return cls(
            id=row['id'],
            id_cliente=row['id_cliente'],
            monto_total=row['monto_total'],
            estado=row['estado'],
            fecha_creacion=row['fecha_creacion'],
            fecha_expiracion=row['fecha_expiracion']
        )
