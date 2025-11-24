"""Script para analizar la estructura actual de la base de datos."""

import sqlite3
import sys
from pathlib import Path

# Añadir Backend al path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from database import get_connection, DB_PATH

def analyze_database():
    """Analiza y muestra la estructura de la base de datos actual."""
    
    if not DB_PATH.exists():
        print("❌ Base de datos no encontrada")
        return
    
    print(f"📊 Analizando base de datos: {DB_PATH}")
    print(f"📏 Tamaño: {DB_PATH.stat().st_size} bytes\n")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Obtener lista de tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = [row[0] for row in cursor.fetchall()]
    
    print(f"🗂️  Tablas encontradas ({len(tables)}):")
    print("=" * 80)
    
    for table_name in tables:
        # Obtener estructura de la tabla
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        # Contar registros
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cursor.fetchone()[0]
        
        print(f"\n📋 {table_name} ({count} registros)")
        print("-" * 80)
        print(f"{'ID':<5} {'Columna':<25} {'Tipo':<15} {'NOT NULL':<10} {'PK':<5}")
        print("-" * 80)
        
        for col in columns:
            cid, name, col_type, notnull, default_val, pk = col
            print(f"{cid:<5} {name:<25} {col_type:<15} {'YES' if notnull else 'NO':<10} {'YES' if pk else 'NO':<5}")
        
        # Mostrar algunos datos de ejemplo
        if count > 0:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
            rows = cursor.fetchall()
            print(f"\n📝 Ejemplos de datos (primeros 3):")
            for i, row in enumerate(rows, 1):
                print(f"  {i}. {dict(zip([col[1] for col in columns], row))}")
    
    conn.close()
    
    print("\n" + "=" * 80)
    print("✅ Análisis completado")

if __name__ == "__main__":
    analyze_database()
