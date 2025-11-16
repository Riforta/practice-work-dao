import sys
import os

# Ensure the package root (the Backend folder) is on sys.path so imports like
# 'models' and 'repository' resolve when running this script directly.
HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

"""
Archivo de ejemplo para el sistema de alquiler de canchas.
Movido desde Backend/main.py para evitar conflicto con api/main.py (FastAPI app).
"""

from models import Cliente, Cancha, ServicioAdicional, Usuario
from repositories import ClienteRepository, ServicioAdicionalRepository, UsuarioRepository
from database.connection import get_connection


def ejemplo_uso_clientes():
    """Ejemplo de uso del sistema de clientes"""
    print("\n" + "="*60)
    print("📋 EJEMPLO: Gestión de Clientes")
    print("="*60)
    
    # 1. Crear un nuevo cliente
    print("\n1️⃣ Creando nuevo cliente...")
    nuevo_cliente = Cliente(
        nombre="Fernando",
        apellido="López",
        dni="40123456",
        telefono="351-5551234",
        email="fernando.lopez@example.com"
    )
    
    try:
        cliente_id = ClienteRepository.crear(nuevo_cliente)
        print(f"   ✓ Cliente creado con ID: {cliente_id}")
    except Exception as e:
        print(f"   ✗ Error al crear cliente: {e}")
        return
    
    # 2. Obtener cliente por ID
    print("\n2️⃣ Obteniendo cliente por ID...")
    cliente = ClienteRepository.obtener_por_id(cliente_id)
    if cliente:
        print(f"   ✓ Cliente encontrado: {cliente.nombre} {cliente.apellido}")
        print(f"     - DNI: {cliente.dni}")
        print(f"     - Teléfono: {cliente.telefono}")
        print(f"     - Email: {cliente.email}")
    
    # 3. Buscar clientes por nombre
    print("\n3️⃣ Buscando clientes por nombre...")
    resultados = ClienteRepository.buscar_por_nombre("Fernando")
    print(f"   ✓ Encontrados {len(resultados)} cliente(s)")
    for c in resultados:
        print(f"     - {c.nombre} {c.apellido} (DNI: {c.dni})")
    
    # 4. Actualizar cliente
    print("\n4️⃣ Actualizando teléfono del cliente...")
    if cliente:
        cliente.telefono = "351-5559999"
        actualizado = ClienteRepository.actualizar(cliente)
        if actualizado:
            print(f"   ✓ Cliente actualizado correctamente")
            print(f"     - Nuevo teléfono: {cliente.telefono}")
    
    # 5. Listar todos los clientes
    print("\n5️⃣ Listando todos los clientes...")
    todos = ClienteRepository.obtener_todos()
    print(f"   ✓ Total de clientes: {len(todos)}")
    for c in todos:
        print(f"     - [{c.id}] {c.nombre} {c.apellido} - {c.telefono}")


def ejemplo_uso_servicios_adicionales():
    """Ejemplo de uso del sistema de servicios adicionales"""
    print("\n" + "="*60)
    print("🧩 EJEMPLO: Servicios Adicionales")
    print("="*60)

    # 1. Crear servicio
    print("\n1️⃣ Creando servicio adicional...")
    servicio = ServicioAdicional(nombre="Estacionamiento", precio_actual=1500.0, activo=1)
    try:
        servicio_id = ServicioAdicionalRepository.crear(servicio)
        print(f"   ✓ Servicio creado con ID: {servicio_id}")
    except Exception as e:
        print(f"   ✗ Error al crear servicio: {e}")
        return

    # 2. Obtener por ID
    print("\n2️⃣ Obteniendo servicio por ID...")
    s = ServicioAdicionalRepository.obtener_por_id(servicio_id)
    if s:
        print(f"   ✓ Servicio: {s.nombre} - ${s.precio_actual} (activo={s.activo})")

    # 3. Buscar por nombre
    print("\n3️⃣ Buscando por nombre 'Estaci' ...")
    encontrados = ServicioAdicionalRepository.buscar_por_nombre("Estaci")
    print(f"   ✓ Encontrados: {len(encontrados)}")

    # 4. Actualizar precio
    print("\n4️⃣ Actualizando precio...")
    if s:
        s.precio_actual = 1800.0
        actualizado = ServicioAdicionalRepository.actualizar(s)
        print(f"   ✓ Actualizado: {actualizado}")

    # 5. Listar activos
    print("\n5️⃣ Listando activos...")
    activos = ServicioAdicionalRepository.obtener_todos(activos=True)
    print(f"   ✓ Activos: {len(activos)}")

    # 6. Desactivar
    print("\n6️⃣ Desactivando servicio...")
    ServicioAdicionalRepository.activar(servicio_id, False)
    s2 = ServicioAdicionalRepository.obtener_por_id(servicio_id)
    print(f"   ✓ Estado actual: {'activo' if s2 and s2.activo == 1 else 'inactivo'}")

    # 7. Eliminar
    print("\n7️⃣ Eliminando servicio...")
    eliminado = ServicioAdicionalRepository.eliminar(servicio_id)
    print(f"   ✓ Eliminado: {eliminado}")


def ejemplo_consulta_personalizada():
    """Ejemplo de consulta SQL personalizada"""
    print("\n" + "="*60)
    print("🔍 EJEMPLO: Consulta Personalizada")
    print("="*60)
    
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        # Contar clientes
        cursor.execute("SELECT COUNT(*) as total FROM Cliente")
        total = cursor.fetchone()['total']
        print(f"\n   Total de clientes en la base de datos: {total}")
        
        # Obtener clientes con email
        cursor.execute("""
            SELECT nombre, apellido, email 
            FROM Cliente 
            WHERE email IS NOT NULL
            ORDER BY nombre
        """)
        
        clientes_con_email = cursor.fetchall()
        print(f"\n   Clientes con email registrado: {len(clientes_con_email)}")
        for row in clientes_con_email:
            print(f"     - {row['nombre']} {row['apellido']}: {row['email']}")
            
    finally:
        conn.close()


def ejemplo_uso_usuarios():
    """Ejemplo de uso del sistema de usuarios"""
    print("\n" + "="*60)
    print("👤 EJEMPLO: Gestión de Usuarios")
    print("="*60)

    # 1. Crear usuario
    print("\n1️⃣ Creando usuario...")
    usuario = Usuario(
        nombre_usuario="admin",
        email="admin@example.com",
        password_hash="hash_demo",
        id_rol=1,
        activo=1,
    )
    try:
        usuario_id = UsuarioRepository.crear(usuario)
        print(f"   ✓ Usuario creado con ID: {usuario_id}")
    except Exception as e:
        print(f"   ✗ Error al crear usuario: {e}")
        return

    # 2. Obtener por ID
    print("\n2️⃣ Obtener por ID...")
    u = UsuarioRepository.obtener_por_id(usuario_id)
    if u:
        print(f"   ✓ Usuario: {u.nombre_usuario} ({u.email})")

    # 3. Buscar por email
    print("\n3️⃣ Buscar por email...")
    u2 = UsuarioRepository.obtener_por_email("admin@example.com")
    print(f"   ✓ Encontrado: {bool(u2)}")

    # 4. Actualizar
    print("\n4️⃣ Actualizar email...")
    if u:
        u.email = "administrador@example.com"
        actualizado = UsuarioRepository.actualizar(u)
        print(f"   ✓ Actualizado: {actualizado}")

    # 5. Cambiar password
    print("\n5️⃣ Cambiar password...")
    UsuarioRepository.cambiar_password(usuario_id, "hash_demo_2")
    print("   ✓ Password cambiado")

    # 6. Listar activos
    print("\n6️⃣ Listar activos...")
    activos = UsuarioRepository.obtener_todos(activos=True)
    print(f"   ✓ Usuarios activos: {len(activos)}")

    # 7. Desactivar y eliminar
    print("\n7️⃣ Desactivar y eliminar...")
    UsuarioRepository.activar(usuario_id, False)
    eliminado = UsuarioRepository.eliminar(usuario_id)
    print(f"   ✓ Eliminado: {eliminado}")


def verificar_estructura_db():
    """Verifica y muestra información sobre la estructura de la base de datos"""
    print("\n" + "="*60)
    print("🗄️  INFORMACIÓN DE LA BASE DE DATOS")
    print("="*60)
    
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        # Listar todas las tablas
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        tablas = cursor.fetchall()
        
        print(f"\n📊 Tablas en la base de datos ({len(tablas)}):")
        for tabla in tablas:
            nombre_tabla = tabla['name']
            
            # Contar registros en cada tabla
            cursor.execute(f"SELECT COUNT(*) as count FROM {nombre_tabla}")
            count = cursor.fetchone()['count']
            
            print(f"   • {nombre_tabla}: {count} registro(s)")
            
    finally:
        conn.close()


def main():
    """Función principal"""
    print("\n" + "="*60)
    print("🏟️  SISTEMA DE ALQUILER DE CANCHAS DEPORTIVAS")
    print("="*60)
    
    # Verificar estructura de la DB
    verificar_estructura_db()
    
    # Ejemplo de uso de clientes
    ejemplo_uso_clientes()
    # Ejemplo de uso de servicios adicionales
    ejemplo_uso_servicios_adicionales()
    # Ejemplo de uso de usuarios
    ejemplo_uso_usuarios()
    
    # Ejemplo de consulta personalizada
    ejemplo_consulta_personalizada()
    
    print("\n" + "="*60)
    print("✅ Ejemplos completados")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
