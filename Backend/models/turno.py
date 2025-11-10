from dataclasses import dataclass
from typing import Optional


@dataclass
class Turno:
    """Modelo de entidad para Turno"""
    id: Optional[int] = None
    id_cancha: int = 0
    fecha_hora_inicio: str = ""
    fecha_hora_fin: str = ""
    estado: str = "disponible"
    precio_final: float = 0.0
    id_cliente: Optional[int] = None
    id_usuario_registro: Optional[int] = None
    reserva_created_at: Optional[str] = None
    id_usuario_bloqueo: Optional[int] = None
    motivo_bloqueo: Optional[str] = None
    
    def __post_init__(self):
        """Validación básica"""
        if self.id is not None:
            if not self.id_cancha:
                raise ValueError("El id de cancha es obligatorio")
            if not self.fecha_hora_inicio:
                raise ValueError("La fecha y hora de inicio es obligatoria")
            if not self.fecha_hora_fin:
                raise ValueError("La fecha y hora de fin es obligatoria")
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'id_cancha': self.id_cancha,
            'fecha_hora_inicio': self.fecha_hora_inicio,
            'fecha_hora_fin': self.fecha_hora_fin,
            'estado': self.estado,
            'precio_final': self.precio_final,
            'id_cliente': self.id_cliente,
            'id_usuario_registro': self.id_usuario_registro,
            'reserva_created_at': self.reserva_created_at,
            'id_usuario_bloqueo': self.id_usuario_bloqueo,
            'motivo_bloqueo': self.motivo_bloqueo
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un objeto Turno desde un diccionario"""
        return cls(
            id=data.get('id'),
            id_cancha=data.get('id_cancha', 0),
            fecha_hora_inicio=data.get('fecha_hora_inicio', ''),
            fecha_hora_fin=data.get('fecha_hora_fin', ''),
            estado=data.get('estado', 'disponible'),
            precio_final=data.get('precio_final', 0.0),
            id_cliente=data.get('id_cliente'),
            id_usuario_registro=data.get('id_usuario_registro'),
            reserva_created_at=data.get('reserva_created_at'),
            id_usuario_bloqueo=data.get('id_usuario_bloqueo'),
            motivo_bloqueo=data.get('motivo_bloqueo')
        )
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un objeto Turno desde una fila de la base de datos"""
        return cls(
            id=row['id'],
            id_cancha=row['id_cancha'],
            fecha_hora_inicio=row['fecha_hora_inicio'],
            fecha_hora_fin=row['fecha_hora_fin'],
            estado=row['estado'],
            precio_final=row['precio_final'],
            id_cliente=row['id_cliente'],
            id_usuario_registro=row['id_usuario_registro'],
            reserva_created_at=row['reserva_created_at'],
            id_usuario_bloqueo=row['id_usuario_bloqueo'],
            motivo_bloqueo=row['motivo_bloqueo']
        )
