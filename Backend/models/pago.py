from dataclasses import dataclass
from typing import Optional


@dataclass
class Pago:
    """Modelo de entidad para Pago"""
    id: Optional[int] = None
    id_pedido: int = 0
    monto: float = 0.0
    estado: str = "iniciado"
    metodo_pago: Optional[str] = None
    id_gateway_externo: Optional[str] = None
    fecha_pago: Optional[str] = None
    id_usuario_manual: int = 0
    
    def __post_init__(self):
        """Validación básica"""
        if self.id is not None:
            if not self.id_pedido:
                raise ValueError("El id de pedido es obligatorio")
            if self.monto < 0:
                raise ValueError("El monto no puede ser negativo")
            if not self.id_usuario_manual:
                raise ValueError("El id de usuario manual es obligatorio")
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'id_pedido': self.id_pedido,
            'monto': self.monto,
            'estado': self.estado,
            'metodo_pago': self.metodo_pago,
            'id_gateway_externo': self.id_gateway_externo,
            'fecha_pago': self.fecha_pago,
            'id_usuario_manual': self.id_usuario_manual
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un objeto Pago desde un diccionario"""
        return cls(
            id=data.get('id'),
            id_pedido=data.get('id_pedido', 0),
            monto=data.get('monto', 0.0),
            estado=data.get('estado', 'iniciado'),
            metodo_pago=data.get('metodo_pago'),
            id_gateway_externo=data.get('id_gateway_externo'),
            fecha_pago=data.get('fecha_pago'),
            id_usuario_manual=data.get('id_usuario_manual', 0)
        )
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un objeto Pago desde una fila de la base de datos"""
        return cls(
            id=row['id'],
            id_pedido=row['id_pedido'],
            monto=row['monto'],
            estado=row['estado'],
            metodo_pago=row['metodo_pago'],
            id_gateway_externo=row['id_gateway_externo'],
            fecha_pago=row['fecha_pago'],
            id_usuario_manual=row['id_usuario_manual']
        )
