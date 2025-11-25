"""Script de migración de base de datos para agregar campo id_usuario a Cliente."""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime

# Añadir Backend al path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from database import get_connection, DB_PATH

def backup_database():
    """Crea una copia de seguridad de la base de datos."""
    backup_path = DB_PATH.parent / f"database_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    
    import shutil
    shutil.copy2(DB_PATH, backup_path)
    print(f"✅ Backup creado: {backup_path}")
    return backup_path

def check_column_exists(cursor, table_name, column_name):
    """Verifica si una columna existe en una tabla."""
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = [col[1] for col in cursor.fetchall()]
    return column_name in columns

def migrate_database():
    """Ejecuta la migración de la base de datos."""
    
    print("🔄 Iniciando migración de base de datos...")
    print("=" * 80)
    
    # Crear backup
    backup_path = backup_database()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar si el campo id_usuario ya existe
        if check_column_exists(cursor, 'Cliente', 'id_usuario'):
            print("✓ El campo 'id_usuario' ya existe en la tabla Cliente")
        else:
            print("➕ Agregando campo 'id_usuario' a la tabla Cliente...")
            
            # SQLite no soporta ALTER TABLE ADD COLUMN con UNIQUE y FOREIGN KEY directamente
            # Necesitamos recrear la tabla
            
            # 1. Crear tabla temporal con la nueva estructura
            cursor.execute("""
                CREATE TABLE Cliente_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT,
                    dni TEXT UNIQUE,
                    telefono TEXT NOT NULL,
                    email TEXT,
                    id_usuario INTEGER UNIQUE,
                    FOREIGN KEY (id_usuario) REFERENCES Usuario(id)
                );
            """)
            
            # 2. Copiar datos existentes
            cursor.execute("""
                INSERT INTO Cliente_new (id, nombre, apellido, dni, telefono, email, id_usuario)
                SELECT id, nombre, apellido, dni, telefono, email, NULL
                FROM Cliente;
            """)
            
            # 3. Eliminar tabla antigua
            cursor.execute("DROP TABLE Cliente;")
            
            # 4. Renombrar tabla nueva
            cursor.execute("ALTER TABLE Cliente_new RENAME TO Cliente;")
            
            print("✅ Campo 'id_usuario' agregado correctamente")
        
        # Verificar que todas las tablas existen según el DER
        expected_tables = [
            'Usuario', 'Rol', 'Cliente', 'Cancha', 'Turno', 'Tarifa',
            'ServicioAdicional', 'TurnoXServicio', 'Torneo', 'Equipo',
            'EquipoMiembro', 'Inscripcion', 'Partido', 'Pedido',
            'PedidoItem', 'Pago'
        ]
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        existing_tables = [row[0] for row in cursor.fetchall() if row[0] != 'sqlite_sequence']
        
        print("\n📊 Verificación de tablas:")
        for table in expected_tables:
            status = "✅" if table in existing_tables else "❌"
            print(f"  {status} {table}")
        
        # Commit de cambios
        conn.commit()
        
        print("\n" + "=" * 80)
        print("✅ Migración completada exitosamente")
        print(f"📁 Backup disponible en: {backup_path}")
        
        # Mostrar conteo de registros
        print("\n📈 Registros por tabla:")
        for table in expected_tables:
            if table in existing_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                count = cursor.fetchone()[0]
                if count > 0:
                    print(f"  • {table}: {count} registros")
        
    except Exception as e:
        print(f"\n❌ Error durante la migración: {e}")
        conn.rollback()
        print(f"💾 Puede restaurar desde: {backup_path}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
