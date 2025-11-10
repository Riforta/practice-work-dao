"""
Archivo principal de ejemplo para el sistema de alquiler de canchas.
"""

from models import Cliente, Cancha
from repository import ClienteRepository
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
    
    # Ejemplo de consulta personalizada
    ejemplo_consulta_personalizada()
    
    print("\n" + "="*60)
    print("✅ Ejemplos completados")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
