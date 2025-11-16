import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.turnos import router as turno_router
from models.turno import Turno
from repositories import turno_repository, cliente_repository, usuario_repository

app = FastAPI()
app.include_router(turno_router, prefix="/api")
client = TestClient(app)

class MemState:
    def __init__(self):
        self.turnos = {}

STATE = MemState()

def make_turno(id_, estado='reservado', id_cliente=1):
    t = Turno(
        id=id_, id_cancha=1,
        fecha_hora_inicio="2025-12-01 10:00:00",
        fecha_hora_fin="2025-12-01 11:00:00",
        estado=estado,
        precio_final=1000.0,
        id_cliente=id_cliente,
        id_usuario_registro=10,
        reserva_created_at="2025-11-01 12:00:00",
        id_usuario_bloqueo=None,
        motivo_bloqueo=None
    )
    STATE.turnos[id_] = t
    return t

@pytest.fixture(autouse=True)
def patch_repositories(monkeypatch):
    STATE.turnos.clear()
    make_turno(1, 'reservado', 1)
    make_turno(2, 'reservado', 2)

    def obtener_por_id_turno(turno_id):
        return STATE.turnos.get(turno_id)
    def actualizar_turno(turno):
        STATE.turnos[turno.id] = turno
        return True
    def obtener_filtrados(id_cancha=None, estado=None, id_cliente=None):
        result = list(STATE.turnos.values())
        if id_cliente is not None:
            result = [t for t in result if t.id_cliente == id_cliente]
        if estado is not None:
            result = [t for t in result if t.estado == estado]
        if id_cancha is not None:
            result = [t for t in result if t.id_cancha == id_cancha]
        return result
    def obtener_cliente(cid):
        return True
    def obtener_usuario(uid):
        return True

    monkeypatch.setattr(turno_repository.TurnoRepository, 'obtener_por_id', staticmethod(obtener_por_id_turno))
    monkeypatch.setattr(turno_repository.TurnoRepository, 'actualizar', staticmethod(actualizar_turno))
    monkeypatch.setattr(turno_repository.TurnoRepository, 'obtener_todos_filtrados', staticmethod(obtener_filtrados))
    monkeypatch.setattr(cliente_repository.ClienteRepository, 'obtener_por_id', staticmethod(obtener_cliente))
    monkeypatch.setattr(usuario_repository.UsuarioRepository, 'obtener_por_id', staticmethod(obtener_usuario))

# --- Tests rutas ---

def test_listar_requiere_id_cliente():
    resp = client.get('/api/turnos')
    # Sin id_cliente lista todos los turnos (200)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


def test_listar_por_cliente_ok():
    resp = client.get('/api/turnos', params={'id_cliente': 1})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 1
    assert all(item['id_cliente'] == 1 for item in data)


def test_consultar_turno_ok():
    resp = client.get('/api/turnos/1')
    assert resp.status_code == 200
    data = resp.json()
    assert data['id'] == 1
