import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.turnos import router as turno_router
from models.turno import Turno

app = FastAPI()
app.include_router(turno_router, prefix="/api")
client = TestClient(app)

# Simulación simple de repositorios usando monkeypatch
from repositories import turno_repository, cliente_repository, usuario_repository

# Estado en memoria para un turno
_turno_mem = Turno(
    id=1,
    id_cancha=5,
    fecha_hora_inicio="2025-12-01 10:00:00",
    fecha_hora_fin="2025-12-01 11:00:00",
    estado="disponible",
    precio_final=2000.0,
    id_cliente=None,
    id_usuario_registro=None,
    reserva_created_at=None,
    id_usuario_bloqueo=None,
    motivo_bloqueo=None
)

# Helpers

def fake_cliente_get(id_cliente):
    return True if id_cliente in (10, 11) else None

def fake_usuario_get(id_usuario):
    return True if id_usuario in (99, 100) else None

def fake_turno_get(turno_id):
    return _turno_mem if turno_id == _turno_mem.id else None

def fake_turno_actualizar(turno):
    global _turno_mem
    _turno_mem = turno
    return True

@pytest.fixture(autouse=True)
def apply_monkeypatches(monkeypatch):
    monkeypatch.setattr(cliente_repository.ClienteRepository, "obtener_por_id", staticmethod(fake_cliente_get))
    monkeypatch.setattr(usuario_repository.UsuarioRepository, "obtener_por_id", staticmethod(fake_usuario_get))
    monkeypatch.setattr(turno_repository.TurnoRepository, "obtener_por_id", staticmethod(fake_turno_get))
    monkeypatch.setattr(turno_repository.TurnoRepository, "actualizar", staticmethod(fake_turno_actualizar))


def test_flujo_reserva_modificar_cancelar():
    global _turno_mem
    # 1. Reservar turno disponible
    resp = client.post("/api/turnos/1/reservar", json={"id_cliente": 10, "id_usuario_registro": 99})
    assert resp.status_code == 200
    data = resp.json()
    assert data["estado"] == "reservado"
    assert data["id_cliente"] == 10

    # 2. Modificar reserva (cambiar cliente y precio)
    resp = client.patch("/api/turnos/1", json={"id_usuario_mod": 100, "id_cliente": 11, "precio_final": 2500})
    assert resp.status_code == 200
    data = resp.json()
    assert data["id_cliente"] == 11
    assert data["precio_final"] == 2500
    assert data["id_usuario_registro"] == 100  # Último modificador

    # 3. Cancelar reserva -> debe volver a disponible y limpiar cliente
    resp = client.post("/api/turnos/1/cancelar", json={"id_usuario_cancelacion": 99})
    assert resp.status_code == 200
    data = resp.json()
    assert data["estado"] == "disponible"
    assert data["id_cliente"] is None
    assert data["id_usuario_registro"] is None
    assert data["reserva_created_at"] is None

    # 4. No debería poder modificar ahora (ya no está reservado)
    resp = client.patch("/api/turnos/1", json={"id_usuario_mod": 100, "precio_final": 3000})
    assert resp.status_code == 400
    assert "solo se pueden modificar" in resp.json()["detail"].lower()

    # 5. No debería poder cancelar (ya está disponible)
    resp = client.post("/api/turnos/1/cancelar", json={"id_usuario_cancelacion": 99})
    assert resp.status_code == 400
    assert "solo se pueden cancelar" in resp.json()["detail"].lower()
