from dataclasses import dataclass
from typing import Optional


@dataclass
class Pago:
    """Modelo de entidad para Pago - vinculado directamente a Turno o Inscripción"""
    id: Optional[int] = None
    id_turno: Optional[int] = None
    id_inscripcion: Optional[int] = None
    monto_turno: Optional[float] = None
    monto_servicios: float = 0.0
    monto_total: float = 0.0
    id_cliente: int = 0
    id_usuario_registro: Optional[int] = None
    estado: str = "iniciado"
    metodo_pago: Optional[str] = None
    id_gateway_externo: Optional[str] = None
    fecha_creacion: Optional[str] = None
    fecha_expiracion: Optional[str] = None
    fecha_completado: Optional[str] = None
    
    def __post_init__(self):
        """Validación básica"""
        if self.id is not None:
            # Debe tener id_turno O id_inscripcion (exclusivo)
            if not self.id_turno and not self.id_inscripcion:
                raise ValueError("El pago debe estar vinculado a un turno o una inscripción")
            if self.id_turno and self.id_inscripcion:
                raise ValueError("El pago no puede estar vinculado a turno e inscripción simultáneamente")
            if self.monto_total < 0:
                raise ValueError("El monto total no puede ser negativo")
            if not self.id_cliente:
                raise ValueError("El id de cliente es obligatorio")
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'id_turno': self.id_turno,
            'id_inscripcion': self.id_inscripcion,
            'monto_turno': self.monto_turno,
            'monto_servicios': self.monto_servicios,
            'monto_total': self.monto_total,
            'id_cliente': self.id_cliente,
            'id_usuario_registro': self.id_usuario_registro,
            'estado': self.estado,
            'metodo_pago': self.metodo_pago,
            'id_gateway_externo': self.id_gateway_externo,
            'fecha_creacion': self.fecha_creacion,
            'fecha_expiracion': self.fecha_expiracion,
            'fecha_completado': self.fecha_completado
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un objeto Pago desde un diccionario"""
        return cls(
            id=data.get('id'),
            id_turno=data.get('id_turno'),
            id_inscripcion=data.get('id_inscripcion'),
            monto_turno=data.get('monto_turno'),
            monto_servicios=data.get('monto_servicios', 0.0),
            monto_total=data.get('monto_total', 0.0),
            id_cliente=data.get('id_cliente', 0),
            id_usuario_registro=data.get('id_usuario_registro'),
            estado=data.get('estado', 'iniciado'),
            metodo_pago=data.get('metodo_pago'),
            id_gateway_externo=data.get('id_gateway_externo'),
            fecha_creacion=data.get('fecha_creacion'),
            fecha_expiracion=data.get('fecha_expiracion'),
            fecha_completado=data.get('fecha_completado')
        )
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un objeto Pago desde una fila de la base de datos"""
        return cls(
            id=row['id'],
            id_turno=row.get('id_turno'),
            id_inscripcion=row.get('id_inscripcion'),
            monto_turno=row.get('monto_turno'),
            monto_servicios=row.get('monto_servicios', 0.0),
            monto_total=row['monto_total'],
            id_cliente=row['id_cliente'],
            id_usuario_registro=row.get('id_usuario_registro'),
            estado=row.get('estado', 'iniciado'),
            metodo_pago=row.get('metodo_pago'),
            id_gateway_externo=row.get('id_gateway_externo'),
            fecha_creacion=row.get('fecha_creacion'),
            fecha_expiracion=row.get('fecha_expiracion'),
            fecha_completado=row.get('fecha_completado')
        )
