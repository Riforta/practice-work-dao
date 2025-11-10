from dataclasses import dataclass


@dataclass
class EquipoMiembro:
    """Modelo de entidad para EquipoMiembro (tabla intermedia)"""
    id_equipo: int = 0
    id_cliente: int = 0
    
    def __post_init__(self):
        """Validación básica"""
        if not self.id_equipo:
            raise ValueError("El id de equipo es obligatorio")
        if not self.id_cliente:
            raise ValueError("El id de cliente es obligatorio")
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id_equipo': self.id_equipo,
            'id_cliente': self.id_cliente
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un objeto EquipoMiembro desde un diccionario"""
        return cls(
            id_equipo=data.get('id_equipo', 0),
            id_cliente=data.get('id_cliente', 0)
        )
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un objeto EquipoMiembro desde una fila de la base de datos"""
        return cls(
            id_equipo=row['id_equipo'],
            id_cliente=row['id_cliente']
        )
