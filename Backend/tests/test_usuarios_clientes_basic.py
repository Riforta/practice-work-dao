"""
Test de integración para verificar los dos flujos de creación de clientes:
1. Usuario se registra (POST /usuarios/register) -> crea Usuario + Cliente vinculado
2. Admin crea cliente sin usuario (POST /clientes/) -> crea Cliente sin id_usuario
"""
import json
import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_1_registro_usuario_crea_cliente_vinculado():
    """
    Test 1: POST /api/usuarios/register debe crear Usuario + Cliente vinculado
    """
    print("\n🧪 Test 1: Registro de usuario con cliente vinculado")
    
    payload = {
        "nombre_usuario": "user_test_001",
        "email": "user001@test.com",
        "password": "password123",
        "id_rol": 2,  # Cliente
        "nombre": "Juan",
        "apellido": "Perez",
        "dni": "11223344",
        "telefono": "3511112222"
    }
    
    res = client.post("/api/usuarios/register", json=payload)
    
    # Verificar respuesta exitosa
    assert res.status_code == 201, f"Esperaba 201, obtuvo {res.status_code}: {res.text}"
    
    data = res.json()
    
    # Verificar estructura de respuesta
    assert "token" in data, "Debe retornar token JWT"
    assert data["token"], "Token no debe estar vacío"
    
    assert "user" in data, "Debe retornar datos del usuario"
    assert data["user"]["nombre_usuario"] == "user_test_001"
    assert data["user"]["email"] == "user001@test.com"
    assert data["user"]["id_rol"] == 2
    assert "password_hash" not in data["user"], "No debe exponer password_hash"
    
    assert "cliente" in data, "Debe retornar datos del cliente"
    assert data["cliente"]["nombre"] == "Juan"
    assert data["cliente"]["apellido"] == "Perez"
    assert data["cliente"]["dni"] == "11223344"
    assert data["cliente"]["telefono"] == "3511112222"
    
    # Verificar vinculación
    assert data["cliente"]["id_usuario"] == data["user"]["id"], \
        "Cliente debe estar vinculado al usuario creado"
    
    print(f"✅ Usuario ID={data['user']['id']} y Cliente ID={data['cliente']['id']} creados y vinculados")
    
    # Guardar IDs para tests posteriores
    return {
        "user_id": data["user"]["id"],
        "cliente_id": data["cliente"]["id"],
        "token": data["token"]
    }


def test_2_crear_cliente_sin_usuario_requiere_admin():
    """
    Test 2: POST /api/clientes/ debe requerir permisos de admin
    """
    print("\n🧪 Test 2: Crear cliente sin usuario requiere admin")
    
    # Intentar crear cliente sin autenticación
    cliente_payload = {
        "nombre": "Cliente Sin Auth",
        "apellido": "Anonimo",
        "dni": "55667788",
        "telefono": "3513334444"
    }
    
    res = client.post("/api/clientes/", json=cliente_payload)
    assert res.status_code == 403, \
        f"Sin autenticación debe retornar 403, obtuvo {res.status_code}"
    
    print("✅ Endpoint protegido correctamente")


def test_3_admin_crea_cliente_sin_usuario():
    """
    Test 3: Admin crea cliente SIN usuario vinculado
    """
    print("\n🧪 Test 3: Admin crea cliente sin usuario")
    
    # Paso 1: Crear usuario admin
    admin_payload = {
        "nombre_usuario": "admin_test_001",
        "email": "admin001@test.com",
        "password": "adminpass123",
        "id_rol": 1,  # Admin
        "nombre": "Admin",
        "apellido": "Sistema",
        "dni": "99887766",
        "telefono": "3519998877"
    }
    
    res_admin = client.post("/api/usuarios/register", json=admin_payload)
    assert res_admin.status_code == 201, f"Error al crear admin: {res_admin.text}"
    
    admin_data = res_admin.json()
    admin_token = admin_data["token"]
    
    print(f"✅ Admin creado con ID={admin_data['user']['id']}")
    
    # Paso 2: Admin crea cliente sin usuario
    cliente_payload = {
        "nombre": "Cliente Sin Usuario",
        "apellido": "Autonomo",
        "dni": "22334455",
        "telefono": "3515556666"
    }
    
    res_cliente = client.post(
        "/api/clientes/",
        json=cliente_payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert res_cliente.status_code == 201, \
        f"Error al crear cliente: {res_cliente.status_code} - {res_cliente.text}"
    
    cliente_data = res_cliente.json()
    
    # Verificar que el cliente no tiene usuario vinculado
    assert cliente_data["id_usuario"] is None, \
        "Cliente debe tener id_usuario=None cuando se crea sin usuario"
    assert cliente_data["nombre"] == "Cliente Sin Usuario"
    assert cliente_data["dni"] == "22334455"
    
    print(f"✅ Cliente ID={cliente_data['id']} creado sin usuario vinculado")
    
    return {
        "admin_token": admin_token,
        "cliente_id": cliente_data["id"]
    }


def test_4_listar_clientes_muestra_ambos_tipos():
    """
    Test 4: GET /api/clientes/ debe mostrar clientes con y sin usuario
    """
    print("\n🧪 Test 4: Listar todos los clientes")
    
    res = client.get("/api/clientes/")
    assert res.status_code == 200, f"Error al listar: {res.status_code}"
    
    clientes = res.json()
    assert isinstance(clientes, list), "Debe retornar una lista"
    
    # Verificar que ambos DNIs existen
    dnis = [c["dni"] for c in clientes]
    
    assert "11223344" in dnis, "Debe existir cliente vinculado a usuario"
    assert "22334455" in dnis, "Debe existir cliente sin usuario"
    
    # Verificar estructura
    cliente_con_usuario = next((c for c in clientes if c["dni"] == "11223344"), None)
    cliente_sin_usuario = next((c for c in clientes if c["dni"] == "22334455"), None)
    
    assert cliente_con_usuario is not None
    assert cliente_con_usuario["id_usuario"] is not None, \
        "Cliente vinculado debe tener id_usuario"
    
    assert cliente_sin_usuario is not None
    assert cliente_sin_usuario["id_usuario"] is None, \
        "Cliente sin vincular debe tener id_usuario=None"
    
    print(f"✅ {len(clientes)} clientes listados correctamente")


def test_5_no_duplicar_dni():
    """
    Test 5: No debe permitir crear clientes con DNI duplicado
    """
    print("\n🧪 Test 5: Validar unicidad de DNI")
    
    # Crear admin token primero
    admin_payload = {
        "nombre_usuario": "admin_test_002",
        "email": "admin002@test.com",
        "password": "adminpass",
        "id_rol": 1,
        "nombre": "Admin2",
        "apellido": "Test",
        "dni": "88776655",
        "telefono": "3518887766"
    }
    res_admin = client.post("/api/usuarios/register", json=admin_payload)
    token = res_admin.json()["token"]
    
    # Intentar crear cliente con DNI duplicado
    cliente_dup = {
        "nombre": "Otro",
        "apellido": "Cliente",
        "dni": "11223344",  # DNI ya usado en test_1
        "telefono": "3517778888"
    }
    
    res = client.post(
        "/api/clientes/",
        json=cliente_dup,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert res.status_code == 400, \
        f"Debe rechazar DNI duplicado con 400, obtuvo {res.status_code}"
    
    assert "ya existe" in res.text.lower() or "duplicado" in res.text.lower(), \
        "Mensaje de error debe indicar DNI duplicado"
    
    print("✅ DNI duplicado rechazado correctamente")


def test_6_no_vincular_usuario_no_cliente():
    """
    Test 6: No debe permitir vincular usuario con rol no-cliente
    """
    print("\n🧪 Test 6: Validar rol de usuario vinculado")
    
    # Crear admin
    admin_payload = {
        "nombre_usuario": "admin_test_003",
        "email": "admin003@test.com",
        "password": "adminpass",
        "id_rol": 1,
        "nombre": "Admin3",
        "apellido": "Test",
        "dni": "77665544",
        "telefono": "3517776655"
    }
    res_admin = client.post("/api/usuarios/register", json=admin_payload)
    admin_data = res_admin.json()
    admin_user_id = admin_data["user"]["id"]
    token = admin_data["token"]
    
    # Intentar crear cliente vinculado al usuario admin (rol != cliente)
    cliente_payload = {
        "nombre": "Cliente",
        "apellido": "Mal Vinculado",
        "dni": "66554433",
        "telefono": "3516665544",
        "id_usuario": admin_user_id  # Intentar vincular a admin
    }
    
    res = client.post(
        "/api/clientes/",
        json=cliente_payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert res.status_code == 400, \
        f"Debe rechazar vinculación a no-cliente con 400, obtuvo {res.status_code}"
    
    assert "rol" in res.text.lower(), \
        "Mensaje debe mencionar problema con el rol"
    
    print("✅ Vinculación a usuario no-cliente rechazada correctamente")


def test_7_actualizar_cliente_sin_cambiar_usuario():
    """
    Test 7: Actualizar cliente sin modificar id_usuario
    """
    print("\n🧪 Test 7: Actualizar cliente manteniendo vínculo")
    
    # Obtener cliente del test 1
    res = client.get("/api/clientes/")
    clientes = res.json()
    cliente = next((c for c in clientes if c["dni"] == "11223344"), None)
    assert cliente is not None, "Cliente del test 1 debe existir"
    
    # Crear admin para tener permisos
    admin_payload = {
        "nombre_usuario": "admin_test_004",
        "email": "admin004@test.com",
        "password": "adminpass",
        "id_rol": 1,
        "nombre": "Admin4",
        "apellido": "Test",
        "dni": "55443322",
        "telefono": "3515554433"
    }
    res_admin = client.post("/api/usuarios/register", json=admin_payload)
    token = res_admin.json()["token"]
    
    # Actualizar teléfono del cliente
    update_payload = {
        "telefono": "3519999999"
    }
    
    res = client.put(
        f"/api/clientes/{cliente['id']}",
        json=update_payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert res.status_code == 200, \
        f"Error al actualizar: {res.status_code} - {res.text}"
    
    updated = res.json()
    assert updated["telefono"] == "3519999999", "Teléfono debe actualizarse"
    assert updated["id_usuario"] == cliente["id_usuario"], \
        "id_usuario no debe cambiar si no se especifica"
    
    print(f"✅ Cliente ID={cliente['id']} actualizado correctamente")


if __name__ == "__main__":
    print("=" * 70)
    print("🚀 TEST DE INTEGRACIÓN: CLIENTES CON/SIN USUARIO")
    print("=" * 70)
    
    test_1_registro_usuario_crea_cliente_vinculado()
    test_2_crear_cliente_sin_usuario_requiere_admin()
    test_3_admin_crea_cliente_sin_usuario()
    test_4_listar_clientes_muestra_ambos_tipos()
    test_5_no_duplicar_dni()
    test_6_no_vincular_usuario_no_cliente()
    test_7_actualizar_cliente_sin_cambiar_usuario()
    
    print("\n" + "=" * 70)
    print("✅ TODOS LOS TESTS PASARON EXITOSAMENTE")
    print("=" * 70)

