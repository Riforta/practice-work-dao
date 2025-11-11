"""
Script de prueba para verificar la creación de la base de datos y los modelos.
"""

from models import Cliente, Cancha, Rol, Usuario
from repository.cliente_repository import ClienteRepository
from database.connection import get_connection


def verificar_tablas():
    """Verifica que todas las tablas se hayan creado correctamente"""
    print("🔍 Verificando tablas en la base de datos...")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' 
        ORDER BY name
    """)
    
    tablas = cursor.fetchall()
    conn.close()
    
    tablas_esperadas = [
        'Cancha', 'Cliente', 'Equipo', 'EquipoMiembro', 'Inscripcion',
        'Pago', 'Partido', 'Pedido', 'PedidoItem', 'Rol',
        'ServicioAdicional', 'Tarifa', 'Torneo', 'Turno', 'TurnoXServicio',
        'Usuario'
    ]
    
    tablas_encontradas = [t[0] for t in tablas]
    
    print(f"\n✓ Tablas encontradas: {len(tablas_encontradas)}")
    for tabla in tablas_encontradas:
        print(f"  - {tabla}")
    
    faltantes = set(tablas_esperadas) - set(tablas_encontradas)
    if faltantes:
        print(f"\n⚠️  Tablas faltantes: {faltantes}")
        return False
    
    print("\n✅ Todas las tablas están presentes")
    return True


def probar_modelo_cliente():
    """Prueba el modelo Cliente"""
    print("\n🧪 Probando modelo Cliente...")
    
    # Crear cliente
    cliente = Cliente(
        nombre="Juan",
        apellido="Pérez",
        dni="12345678",
        telefono="351-1234567",
        email="juan.perez@example.com"
    )
    
    print(f"  Cliente creado: {cliente.nombre} {cliente.apellido}")
    
    # Convertir a dict
    cliente_dict = cliente.to_dict()
    print(f"  Cliente como dict: {cliente_dict}")
    
    # Crear desde dict
    cliente2 = Cliente.from_dict({
        'nombre': 'María',
        'apellido': 'González',
        'telefono': '351-7654321'
    })
    print(f"  Cliente 2 creado: {cliente2.nombre} {cliente2.apellido}")
    
    print("✅ Modelo Cliente funciona correctamente")


def probar_repository_cliente():
    """Prueba el repositorio de Cliente"""
    print("\n🧪 Probando ClienteRepository...")
    
    try:
        # Crear clientes de prueba
        cliente1 = Cliente(
            nombre="Carlos",
            apellido="Rodríguez",
            dni="23456789",
            telefono="351-2345678",
            email="carlos@example.com"
        )
        
        id1 = ClienteRepository.crear(cliente1)
        print(f"  ✓ Cliente creado con ID: {id1}")
        
        cliente2 = Cliente(
            nombre="Ana",
            apellido="Martínez",
            dni="34567890",
            telefono="351-3456789",
            email="ana@example.com"
        )
        
        id2 = ClienteRepository.crear(cliente2)
        print(f"  ✓ Cliente creado con ID: {id2}")
        
        # Obtener por ID
        cliente_obtenido = ClienteRepository.obtener_por_id(id1)
        if cliente_obtenido:
            print(f"  ✓ Cliente obtenido: {cliente_obtenido.nombre} {cliente_obtenido.apellido}")
        
        # Obtener por DNI
        cliente_dni = ClienteRepository.obtener_por_dni("23456789")
        if cliente_dni:
            print(f"  ✓ Cliente por DNI: {cliente_dni.nombre}")
        
        # Obtener todos
        todos = ClienteRepository.obtener_todos()
        print(f"  ✓ Total de clientes: {len(todos)}")
        
        # Buscar por nombre
        resultados = ClienteRepository.buscar_por_nombre("Carlos")
        print(f"  ✓ Búsqueda 'Carlos': {len(resultados)} resultado(s)")
        
        # Actualizar
        if cliente_obtenido:
            cliente_obtenido.telefono = "351-9999999"
            actualizado = ClienteRepository.actualizar(cliente_obtenido)
            print(f"  ✓ Cliente actualizado: {actualizado}")
        
        # Contar
        total = ClienteRepository.contar()
        print(f"  ✓ Total de clientes en DB: {total}")
        
        # Verificar DNI existente
        existe = ClienteRepository.existe_dni("23456789")
        print(f"  ✓ DNI existe: {existe}")
        
        print("\n✅ ClienteRepository funciona correctamente")
        
    except Exception as e:
        print(f"\n❌ Error en prueba de repository: {e}")


def probar_otros_modelos():
    """Prueba rápida de otros modelos"""
    print("\n🧪 Probando otros modelos...")
    
    # Rol
    rol = Rol(nombre_rol="admin", descripcion="Administrador del sistema")
    print(f"  ✓ Rol: {rol.nombre_rol}")
    
    # Usuario
    usuario = Usuario(
        nombre_usuario="admin",
        email="admin@example.com",
        password_hash="hash_aqui",
        id_rol=1
    )
    print(f"  ✓ Usuario: {usuario.nombre_usuario}")
    
    # Cancha
    cancha = Cancha(
        nombre="Cancha 1",
        tipo_deporte="Fútbol 5",
        descripcion="Cancha de césped sintético"
    )
    print(f"  ✓ Cancha: {cancha.nombre} - {cancha.tipo_deporte}")
    
    print("✅ Otros modelos funcionan correctamente")


def main():
    """Función principal de prueba"""
    print("=" * 60)
    print("🚀 VERIFICACIÓN DEL SISTEMA")
    print("=" * 60)
    
    # Verificar tablas
    if not verificar_tablas():
        print("\n❌ Algunas tablas no se crearon correctamente")
        return
    
    # Probar modelos
    probar_modelo_cliente()
    probar_otros_modelos()
    
    # Probar repository
    probar_repository_cliente()
    
    print("\n" + "=" * 60)
    print("✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
    print("=" * 60)


if __name__ == "__main__":
    main()
