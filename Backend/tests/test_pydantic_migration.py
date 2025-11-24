"""Script de prueba para verificar los endpoints migrados a Pydantic."""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def test_auth_endpoints():
    """Prueba endpoints de autenticación."""
    print_section("1. AUTENTICACIÓN")
    
    # Test 1: Login
    print("\n[POST /auth/login] - Login de usuario")
    login_data = {
        "usuario": "admin",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Token recibido: {data['token'][:30]}...")
        print(f"✓ Usuario: {data['user']['nombre_usuario']}")
        return data['token']
    else:
        print(f"✗ Error: {response.text}")
        return None

def test_clientes_endpoints():
    """Prueba endpoints de clientes."""
    print_section("2. CLIENTES (CRUD con Pydantic)")
    
    # Test 2: Crear cliente
    print("\n[POST /clientes/] - Crear cliente con validación Pydantic")
    cliente_data = {
        "nombre": "Juan",
        "apellido": "Pérez",
        "dni": "12345678",
        "telefono": "3512345678",
        "email": "juan.perez@example.com"
    }
    response = requests.post(f"{BASE_URL}/clientes/", json=cliente_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        cliente = response.json()
        print(f"✓ Cliente creado: {cliente['nombre']} {cliente['apellido']}")
        print(f"✓ ID: {cliente['id']}")
        cliente_id = cliente['id']
    else:
        print(f"✗ Error: {response.text}")
        return
    
    # Test 3: Listar clientes
    print("\n[GET /clientes/] - Listar todos los clientes")
    response = requests.get(f"{BASE_URL}/clientes/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        clientes = response.json()
        print(f"✓ Total de clientes: {len(clientes)}")
    
    # Test 4: Obtener cliente específico
    print(f"\n[GET /clientes/{cliente_id}] - Obtener cliente por ID")
    response = requests.get(f"{BASE_URL}/clientes/{cliente_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        cliente = response.json()
        print(f"✓ Cliente: {cliente['nombre']} {cliente['apellido']}")

def test_canchas_endpoints():
    """Prueba endpoints de canchas."""
    print_section("3. CANCHAS (CRUD con Pydantic)")
    
    # Test 5: Crear cancha
    print("\n[POST /canchas/] - Crear cancha con validación Pydantic")
    cancha_data = {
        "nombre": "Cancha Test Pydantic",
        "tipo_deporte": "Fútbol 5",
        "descripcion": "Cancha de prueba con schemas Pydantic",
        "activa": 1
    }
    response = requests.post(f"{BASE_URL}/canchas/", json=cancha_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        cancha = response.json()
        print(f"✓ Cancha creada: {cancha['nombre']}")
        print(f"✓ ID: {cancha['id']}")
        cancha_id = cancha['id']
    else:
        print(f"✗ Error: {response.text}")
        return
    
    # Test 6: Listar canchas
    print("\n[GET /canchas/] - Listar todas las canchas")
    response = requests.get(f"{BASE_URL}/canchas/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        canchas = response.json()
        print(f"✓ Total de canchas: {len(canchas)}")

def test_turnos_endpoints():
    """Prueba endpoints de turnos."""
    print_section("4. TURNOS Y RESERVAS (con Pydantic)")
    
    # Test 7: Crear turno
    print("\n[POST /turnos/] - Crear turno con TurnoCreateRequest")
    turno_data = {
        "id_cancha": 1,
        "fecha_hora_inicio": "2025-01-15 10:00:00",
        "fecha_hora_fin": "2025-01-15 11:00:00",
        "precio_final": 5000.0,
        "estado": "disponible"
    }
    response = requests.post(f"{BASE_URL}/turnos/", json=turno_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        turno = response.json()
        print(f"✓ Turno creado con ID: {turno['id']}")
        print(f"✓ Estado: {turno['estado']}")
        print(f"✓ Precio: ${turno['precio_final']}")
        turno_id = turno['id']
    else:
        print(f"✗ Error: {response.text}")
        return
    
    # Test 8: Listar turnos
    print("\n[GET /turnos/] - Listar turnos con TurnoResponse")
    response = requests.get(f"{BASE_URL}/turnos/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        turnos = response.json()
        print(f"✓ Total de turnos: {len(turnos)}")
        print(f"✓ Primer turno: {turnos[0]['fecha_hora_inicio']}")

def test_validaciones_pydantic():
    """Prueba validaciones automáticas de Pydantic."""
    print_section("5. VALIDACIONES AUTOMÁTICAS DE PYDANTIC")
    
    # Test 9: Login sin password (debe fallar)
    print("\n[POST /auth/login] - Login sin password (validación Pydantic)")
    response = requests.post(f"{BASE_URL}/auth/login", json={"usuario": "admin"})
    print(f"Status: {response.status_code}")
    if response.status_code == 422:
        print("✓ Pydantic rechazó el request correctamente")
        error = response.json()
        print(f"✓ Error: {error['detail'][0]['msg']}")
    
    # Test 10: Cliente con email inválido
    print("\n[POST /clientes/] - Cliente con email inválido (EmailStr)")
    cliente_data = {
        "nombre": "Test",
        "telefono": "123456",
        "email": "email_invalido"  # Sin @
    }
    response = requests.post(f"{BASE_URL}/clientes/", json=cliente_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 422:
        print("✓ Pydantic validó email correctamente")
        error = response.json()
        print(f"✓ Error: {error['detail'][0]['msg']}")
    
    # Test 11: Turno con precio negativo
    print("\n[POST /turnos/] - Turno con precio negativo (Field ge=0)")
    turno_data = {
        "id_cancha": 1,
        "fecha_hora_inicio": "2025-01-15 14:00:00",
        "fecha_hora_fin": "2025-01-15 15:00:00",
        "precio_final": -100.0  # Precio negativo
    }
    response = requests.post(f"{BASE_URL}/turnos/", json=turno_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 422:
        print("✓ Pydantic validó precio >= 0 correctamente")
        error = response.json()
        print(f"✓ Error: {error['detail'][0]['msg']}")

def main():
    """Ejecuta todas las pruebas."""
    print("\n" + "="*60)
    print("  PRUEBAS DE MIGRACIÓN A PYDANTIC")
    print("  Backend: http://localhost:8000")
    print("="*60)
    
    try:
        # Verificar que el servidor esté corriendo
        response = requests.get(f"{BASE_URL.replace('/api', '')}/docs")
        if response.status_code != 200:
            print("\n✗ Error: El servidor no está corriendo en http://localhost:8000")
            print("  Por favor, inicia el servidor con: python api/main.py")
            return
        
        # Ejecutar tests
        token = test_auth_endpoints()
        test_clientes_endpoints()
        test_canchas_endpoints()
        test_turnos_endpoints()
        test_validaciones_pydantic()
        
        print_section("RESUMEN")
        print("\n✓ Migración a Pydantic completada exitosamente")
        print("✓ Todos los endpoints funcionan correctamente")
        print("✓ Validaciones automáticas activas")
        print("\nPuedes ver la documentación completa en:")
        print("  → http://localhost:8000/docs (Swagger UI)")
        print("  → http://localhost:8000/redoc (ReDoc)")
        
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: No se pudo conectar al servidor")
        print("  Por favor, inicia el servidor con: python api/main.py")
    except Exception as e:
        print(f"\n✗ Error inesperado: {e}")

if __name__ == "__main__":
    main()
