from typing import List, Dict, Any, Optional

from models.tarifa import Tarifa
from repositories.tarifa_repository import TarifaRepository
from repositories.cancha_repository import CanchaRepository


def _validar_datos_tarifa(data: Dict[str, Any], para_actualizar: bool = False) -> None:
    if not para_actualizar and not data.get("id_cancha"):
        raise ValueError("El campo 'id_cancha' es requerido")

    if "precio_hora" in data:
        try:
            precio = float(data["precio_hora"])
        except (TypeError, ValueError):
            raise ValueError("El campo 'precio_hora' debe ser numérico")
        if precio < 0:
            raise ValueError("El precio por hora no puede ser negativo")


def _seed_tarifas_desde_canchas() -> int:
    """Genera tarifas base usando el precio de la cancha si no existen."""
    creadas = 0
    canchas = CanchaRepository.listar_todas()
    for cancha in canchas:
        if cancha.id is None:
            continue
        if TarifaRepository.existe_para_cancha(cancha.id):
            continue
        if cancha.precio_hora is None:
            continue
        tarifa = Tarifa(
            id_cancha=cancha.id,
            descripcion="Tarifa base generada automáticamente",
            precio_hora=cancha.precio_hora,
        )
        tarifa.id = TarifaRepository.crear(tarifa)
        creadas += 1
    return creadas


def listar_tarifas(id_cancha: Optional[int] = None, autogenerar: bool = True) -> List[Tarifa]:
    TarifaRepository.ensure_schema()

    if autogenerar:
        _seed_tarifas_desde_canchas()

    if id_cancha is not None:
        return TarifaRepository.obtener_por_cancha(id_cancha)
    return TarifaRepository.listar_todas()


def obtener_tarifa_por_id(tarifa_id: int) -> Tarifa:
    tarifa = TarifaRepository.obtener_por_id(tarifa_id)
    if tarifa is None:
        raise LookupError(f"Tarifa con ID {tarifa_id} no encontrada")
    return tarifa


def crear_tarifa(data: Dict[str, Any]) -> Tarifa:
    _validar_datos_tarifa(data)

    cancha = CanchaRepository.obtener_por_id(data["id_cancha"])
    if cancha is None:
        raise ValueError(f"No existe la cancha con ID {data['id_cancha']}")

    if TarifaRepository.existe_para_cancha(cancha.id):
        raise ValueError("Ya existe una tarifa para esta cancha")

    tarifa = Tarifa.from_dict(data)
    tarifa.id = TarifaRepository.crear(tarifa)
    return tarifa


def actualizar_tarifa(tarifa_id: int, data: Dict[str, Any]) -> Tarifa:
    _validar_datos_tarifa(data, para_actualizar=True)

    existente = TarifaRepository.obtener_por_id(tarifa_id)
    if existente is None:
        raise LookupError(f"Tarifa con ID {tarifa_id} no encontrada")

    if "id_cancha" in data:
        cancha = CanchaRepository.obtener_por_id(data["id_cancha"])
        if cancha is None:
            raise ValueError(f"No existe la cancha con ID {data['id_cancha']}")
        if TarifaRepository.existe_para_cancha(data["id_cancha"], excluir_id=tarifa_id):
            raise ValueError("Ya existe una tarifa para esta cancha")

    merged = existente.to_dict()
    merged.update(data)
    tarifa_actualizada = Tarifa.from_dict(merged)
    tarifa_actualizada.id = tarifa_id

    ok = TarifaRepository.actualizar(tarifa_actualizada)
    if not ok:
        raise Exception("No se pudo actualizar la tarifa")
    return tarifa_actualizada


def eliminar_tarifa(tarifa_id: int) -> bool:
    if not TarifaRepository.eliminar(tarifa_id):
        raise LookupError(f"Tarifa con ID {tarifa_id} no encontrada")
    return True
