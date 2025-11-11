from dataclasses import dataclass


@dataclass
class TurnoServicio:
    """Modelo de entidad para TurnoXServicio (tabla intermedia)"""
    id_turno: int = 0
    id_servicio: int = 0
    cantidad: int = 1
    precio_unitario_congelado: float = 0.0
    
    def __post_init__(self):
        """Validación básica"""
        if not self.id_turno:
            raise ValueError("El id de turno es obligatorio")
        if not self.id_servicio:
            raise ValueError("El id de servicio es obligatorio")
        if self.cantidad < 1:
            raise ValueError("La cantidad debe ser al menos 1")
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id_turno': self.id_turno,
            'id_servicio': self.id_servicio,
            'cantidad': self.cantidad,
            'precio_unitario_congelado': self.precio_unitario_congelado
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un objeto TurnoServicio desde un diccionario"""
        return cls(
            id_turno=data.get('id_turno', 0),
            id_servicio=data.get('id_servicio', 0),
            cantidad=data.get('cantidad', 1),
            precio_unitario_congelado=data.get('precio_unitario_congelado', 0.0)
        )
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un objeto TurnoServicio desde una fila de la base de datos"""
        return cls(
            id_turno=row['id_turno'],
            id_servicio=row['id_servicio'],
            cantidad=row['cantidad'],
            precio_unitario_congelado=row['precio_unitario_congelado']
        )
