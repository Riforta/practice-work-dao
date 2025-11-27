import sqlite3
import os

# Eliminar base de datos anterior si existe
if os.path.exists('database.db'):
    os.remove('database.db')
    print("Base de datos anterior eliminada")

# Crear nueva base de datos
conn = sqlite3.connect('database.db')
conn.execute("PRAGMA foreign_keys = ON")

# Ejecutar script SQL
with open('init_db.sql', 'r', encoding='utf-8') as f:
    sql_script = f.read()

conn.executescript(sql_script)
conn.commit()

# Verificar tablas creadas
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("\n✓ Base de datos creada exitosamente!")
print(f"\nTablas creadas ({len(tables)}):")
for table in tables:
    print(f"  - {table[0]}")

# Verificar datos de prueba
cursor.execute("SELECT COUNT(*) FROM Usuario")
usuarios = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM Cancha")
canchas = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM ServicioAdicional")
servicios = cursor.fetchone()[0]

print(f"\nDatos de prueba insertados:")
print(f"  - Usuarios: {usuarios}")
print(f"  - Canchas: {canchas}")
print(f"  - Servicios: {servicios}")

conn.close()
