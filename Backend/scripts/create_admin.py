"""
Script para crear usuario administrador en el sistema.

Uso:
    python scripts/create_admin.py
"""

import sys
import os

# Agregar el directorio Backend al path para importar módulos
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, backend_dir)

from services import usuarios_service


def crear_admin():
    """Crea un usuario administrador en el sistema."""
    
    print("🔧 Creando usuario administrador...\n")
    
    usuario_data = {
        'nombre_usuario': 'admin',
        'email': 'admin@canchas.com',
        'password': 'admin123',
        'id_rol': 1  # 1 = Administrador
    }
    
    try:
        # Usar crear_usuario en vez de registrar_usuario (admin no necesita cliente)
        usuario = usuarios_service.crear_usuario(usuario_data)
        
        print("✅ Usuario administrador creado exitosamente!\n")
        print(f"   📋 Detalles:")
        print(f"   ├─ ID: {usuario.id}")
        print(f"   ├─ Usuario: {usuario.nombre_usuario}")
        print(f"   ├─ Email: {usuario.email}")
        print(f"   ├─ Rol: {usuario.id_rol} (Admin)")
        print(f"   └─ Estado: {'Activo' if usuario.activo else 'Inactivo'}")
        print(f"\n🔑 Credenciales:")
        print(f"   Usuario: admin")
        print(f"   Password: admin123")
        print(f"\n⚠️  IMPORTANTE: Cambia la contraseña después del primer login en producción")
        
        return True
        
    except ValueError as e:
        print(f"❌ Error de validación: {e}")
        if "ya está en uso" in str(e) or "ya está registrado" in str(e):
            print(f"\n💡 El usuario 'admin' ya existe en la base de datos.")
            print(f"   Si necesitas resetear la contraseña, puedes:")
            print(f"   1. Eliminarlo desde la base de datos")
            print(f"   2. Usar el endpoint de actualización")
        return False
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        print(f"\n🔍 Verifica que:")
        print(f"   • La base de datos existe (database.db)")
        print(f"   • Las tablas están creadas")
        print(f"   • El rol 1 (Admin) existe en la tabla Rol")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print(" CREACIÓN DE USUARIO ADMINISTRADOR")
    print("=" * 60)
    print()
    
    success = crear_admin()
    
    print()
    print("=" * 60)
    
    sys.exit(0 if success else 1)
