from typing import List, Dict, Any

from models.inscripcion import Inscripcion
from repository.inscripcion_repository import InscripcionRepository


def crear_inscripcion(data: Dict[str, Any]) -> Inscripcion:
    ins = Inscripcion.from_dict(data)
    try:
        ins.id = InscripcionRepository.crear(ins)
        return ins
    except Exception as e:
        raise Exception(f'Error al crear inscripción: {e}')


def obtener_inscripcion_por_id(inscripcion_id: int) -> Inscripcion:
    ins = InscripcionRepository.obtener_por_id(inscripcion_id)
    if ins is None:
        raise LookupError(f'Inscripción con ID {inscripcion_id} no encontrada')
    return ins


def listar_inscripciones_por_torneo(torneo_id: int) -> List[Inscripcion]:
    return InscripcionRepository.listar_por_torneo(torneo_id)


def actualizar_inscripcion(inscripcion_id: int, data: Dict[str, Any]) -> Inscripcion:
    existente = InscripcionRepository.obtener_por_id(inscripcion_id)
    if existente is None:
        raise LookupError(f'Inscripción con ID {inscripcion_id} no encontrada')

    updated = existente.to_dict()
    updated.update(data)
    ins_actualizada = Inscripcion.from_dict(updated)
    ins_actualizada.id = inscripcion_id

    try:
        ok = InscripcionRepository.actualizar(ins_actualizada)
        if not ok:
            raise Exception('No se actualizó la inscripción')
        return ins_actualizada
    except Exception as e:
        raise Exception(f'Error al actualizar inscripción: {e}')


def cambiar_estado_inscripcion(inscripcion_id: int, nuevo_estado: str) -> bool:
    try:
        return InscripcionRepository.cambiar_estado(inscripcion_id, nuevo_estado)
    except Exception as e:
        raise Exception(f'Error al cambiar estado de la inscripción: {e}')


def eliminar_inscripcion(inscripcion_id: int) -> bool:
    try:
        return InscripcionRepository.eliminar(inscripcion_id)
    except Exception as e:
        raise Exception(f'Error al eliminar inscripción: {e}')
