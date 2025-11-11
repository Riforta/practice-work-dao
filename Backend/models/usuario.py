from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:
    """Modelo de entidad para Usuario"""
    id: Optional[int] = None
    nombre_usuario: str = ""
    email: str = ""
    password_hash: str = ""
    id_rol: Optional[int] = None
    activo: int = 1
    
    def __post_init__(self):
        """Validación básica"""
        if self.id is not None:
            if not self.nombre_usuario:
                raise ValueError("El nombre de usuario es obligatorio")
            if not self.email:
                raise ValueError("El email es obligatorio")
            if not self.password_hash:
                raise ValueError("El password es obligatorio")
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'nombre_usuario': self.nombre_usuario,
            'email': self.email,
            'password_hash': self.password_hash,
            'id_rol': self.id_rol,
            'activo': self.activo
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un objeto Usuario desde un diccionario"""
        return cls(
            id=data.get('id'),
            nombre_usuario=data.get('nombre_usuario', ''),
            email=data.get('email', ''),
            password_hash=data.get('password_hash', ''),
            id_rol=data.get('id_rol'),
            activo=data.get('activo', 1)
        )
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un objeto Usuario desde una fila de la base de datos"""
        return cls(
            id=row['id'],
            nombre_usuario=row['nombre_usuario'],
            email=row['email'],
            password_hash=row['password_hash'],
            id_rol=row['id_rol'],
            activo=row['activo']
        )
