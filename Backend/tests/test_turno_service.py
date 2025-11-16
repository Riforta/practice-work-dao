import pytest
from models.turno import Turno
from services.reservas_service import ReservasService
from repositories import turno_repository, cliente_repository, usuario_repository
from datetime import datetime

# --- Infra mínima de BD simulada usando monkeypatch ---

class MemState:
    def __init__(self):
        self.turnos = {}
        self.clientes = {1: True, 2: True}
        self.usuarios = {10: True, 11: True}

STATE = MemState()

# Helpers para crear turnos

def make_turno(id_, estado='disponible', id_cliente=None):
    t = Turno(
        id=id_, id_cancha=1,
        fecha_hora_inicio="2025-12-01 10:00:00",
        fecha_hora_fin="2025-12-01 11:00:00",
        estado=estado,
        precio_final=1000.0,
        id_cliente=id_cliente,
        id_usuario_registro=None,
        reserva_created_at=None,
        id_usuario_bloqueo=None,
        motivo_bloqueo=None
    )
    STATE.turnos[id_] = t
    return t

# Monkeypatch repository methods

@pytest.fixture(autouse=True)
def patch_repositories(monkeypatch):
    def obtener_por_id_turno(turno_id):
        return STATE.turnos.get(turno_id)
    def actualizar_turno(turno):
        STATE.turnos[turno.id] = turno
        return True
    def obtener_filtrados(id_cancha=None, estado=None, id_cliente=None):
        result = list(STATE.turnos.values())
        if id_cancha is not None:
            result = [t for t in result if t.id_cancha == id_cancha]
        if estado is not None:
            result = [t for t in result if t.estado == estado]
        if id_cliente is not None:
            result = [t for t in result if t.id_cliente == id_cliente]
        return result
    def obtener_cliente(cid):
        return True if STATE.clientes.get(cid) else None
    def obtener_usuario(uid):
        return True if STATE.usuarios.get(uid) else None

    monkeypatch.setattr(turno_repository.TurnoRepository, 'obtener_por_id', staticmethod(obtener_por_id_turno))
    monkeypatch.setattr(turno_repository.TurnoRepository, 'actualizar', staticmethod(actualizar_turno))
    monkeypatch.setattr(turno_repository.TurnoRepository, 'obtener_todos_filtrados', staticmethod(obtener_filtrados))
    monkeypatch.setattr(cliente_repository.ClienteRepository, 'obtener_por_id', staticmethod(obtener_cliente))
    monkeypatch.setattr(usuario_repository.UsuarioRepository, 'obtener_por_id', staticmethod(obtener_usuario))

    # Reset state per test
    STATE.turnos.clear()
    make_turno(1, 'disponible')
    make_turno(2, 'reservado', id_cliente=1)
    make_turno(3, 'reservado', id_cliente=2)

# --- Tests registrar_reserva ---

def test_registrar_reserva_ok():
    turno = ReservasService.registrar_reserva(1, id_cliente=1, id_usuario_registro=10)
    assert turno.estado == 'reservado'
    assert turno.id_cliente == 1
    assert turno.id_usuario_registro == 10
    assert turno.reserva_created_at is not None

def test_registrar_reserva_turno_no_disponible():
    with pytest.raises(ValueError):
        ReservasService.registrar_reserva(2, id_cliente=1, id_usuario_registro=10)


def test_registrar_reserva_cliente_no_existe():
    with pytest.raises(ValueError):
        ReservasService.registrar_reserva(1, id_cliente=999, id_usuario_registro=10)

# --- Tests consultar_turno_por_id ---

def test_consultar_turno_pertenencia_ok():
    t = ReservasService.consultar_turno_por_id(2, id_cliente=1)
    assert t.id == 2


def test_consultar_turno_pertenencia_incorrecta():
    with pytest.raises(PermissionError):
        ReservasService.consultar_turno_por_id(2, id_cliente=2)

# --- Tests modificar_reserva ---

def test_modificar_reserva_ok():
    turno = ReservasService.modificar_reserva(2, {'precio_final': 1500, 'id_cliente': 1}, id_usuario_mod=10)
    assert turno.precio_final == 1500
    assert turno.id_cliente == 1
    assert turno.id_usuario_registro == 10


def test_modificar_reserva_estado_invalido():
    with pytest.raises(ValueError):
        ReservasService.modificar_reserva(1, {'precio_final': 1500}, id_usuario_mod=10)


def test_modificar_reserva_cliente_inexistente():
    with pytest.raises(ValueError):
        ReservasService.modificar_reserva(2, {'id_cliente': 999}, id_usuario_mod=10)


def test_modificar_reserva_sin_cambios():
    with pytest.raises(ValueError):
        ReservasService.modificar_reserva(2, {}, id_usuario_mod=10)

# --- Tests cancelar_reserva ---

def test_cancelar_reserva_ok():
    turno = ReservasService.cancelar_reserva(2, id_usuario_cancelacion=10)
    assert turno.estado == 'disponible'
    assert turno.id_cliente is None
    assert turno.id_usuario_registro is None
    assert turno.reserva_created_at is None


def test_cancelar_reserva_estado_invalido():
    with pytest.raises(ValueError):
        ReservasService.cancelar_reserva(1, id_usuario_cancelacion=10)

# --- Tests listado ---

def test_listar_reservas_cliente_ok():
    turnos = ReservasService.listar_reservas_cliente(1)
    assert all(t.id_cliente == 1 for t in turnos)


def test_listar_reservas_cliente_estado_invalido():
    with pytest.raises(ValueError):
        ReservasService.listar_reservas_cliente(1, estado='no_valido')


def test_listar_turnos_wrapper_general():
    # Sin id_cliente devuelve todos
    turnos = ReservasService.listar_turnos()
    assert len(turnos) == 3


def test_listar_turnos_wrapper_con_cliente():
    turnos = ReservasService.listar_turnos(id_cliente=2)
    assert all(t.id_cliente == 2 for t in turnos)
