from dataclasses import dataclass
from typing import Optional


@dataclass
class Tarifa:
    """Modelo para tarifas de cancha."""

    id: Optional[int] = None
    id_cancha: int = 0
    descripcion: Optional[str] = None
    precio_hora: float = 0.0

    def __post_init__(self):
        if not self.id_cancha:
            raise ValueError("La tarifa debe estar asociada a una cancha (id_cancha requerido)")
        if self.precio_hora is None:
            raise ValueError("El precio por hora es obligatorio")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "id_cancha": self.id_cancha,
            "descripcion": self.descripcion,
            "precio_hora": self.precio_hora,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Tarifa":
        return cls(
            id=data.get("id"),
            id_cancha=data.get("id_cancha", 0),
            descripcion=data.get("descripcion"),
            precio_hora=data.get("precio_hora", 0.0),
        )

    @classmethod
    def from_db_row(cls, row) -> "Tarifa":
        return cls(
            id=row["id"],
            id_cancha=row["id_cancha"],
            descripcion=row["descripcion"],
            precio_hora=row["precio_hora"],
        )
