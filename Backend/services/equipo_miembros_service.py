from typing import List, Dict, Any

from models.equipo_miembro import EquipoMiembro
from repositories.equipo_miembro_repository import EquipoMiembroRepository


def agregar_miembro(data: Dict[str, Any]) -> None:
    miembro = EquipoMiembro.from_dict(data)
    try:
        EquipoMiembroRepository.agregar(miembro)
    except Exception as e:
        raise Exception(f'Error al agregar miembro: {e}')


def listar_miembros_por_equipo(equipo_id: int) -> List[EquipoMiembro]:
    return EquipoMiembroRepository.listar_por_equipo(equipo_id)


def eliminar_miembro(equipo_id: int, cliente_id: int) -> bool:
    try:
        return EquipoMiembroRepository.eliminar(equipo_id, cliente_id)
    except Exception as e:
        raise Exception(f'Error al eliminar miembro: {e}')
