"""Verificar la estructura migrada de la base de datos."""

import sqlite3
import sys
from pathlib import Path

backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from database import get_connection

conn = get_connection()
cursor = conn.cursor()

print('Estructura de tabla Cliente:')
print('=' * 80)
cursor.execute('PRAGMA table_info(Cliente);')
for col in cursor.fetchall():
    cid, name, col_type, notnull, default_val, pk = col
    constraints = []
    if notnull:
        constraints.append('NOT NULL')
    if pk:
        constraints.append('PRIMARY KEY')
    print(f'  {name:<20} {col_type:<15} {" ".join(constraints)}')

print('\nDatos en Cliente:')
print('=' * 80)
cursor.execute('SELECT id, nombre, apellido, dni, id_usuario FROM Cliente;')
for row in cursor.fetchall():
    print(f'  ID: {row[0]}, Nombre: {row[1]} {row[2]}, DNI: {row[3]}, id_usuario: {row[4]}')

print('\nForeign Keys en Cliente:')
print('=' * 80)
cursor.execute('PRAGMA foreign_key_list(Cliente);')
fks = cursor.fetchall()
if fks:
    for fk in fks:
        print(f'  Columna: {fk[3]} -> Tabla: {fk[2]}.{fk[4]}')
else:
    print('  No hay foreign keys')

print('\nVerificar UNIQUE constraint en id_usuario:')
print('=' * 80)
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='Cliente';")
create_sql = cursor.fetchone()[0]
if 'id_usuario' in create_sql:
    if 'UNIQUE' in create_sql or 'unique' in create_sql.lower():
        print('  ✓ Campo id_usuario tiene constraint UNIQUE')
    else:
        print('  ✗ Campo id_usuario NO tiene constraint UNIQUE')
    print(f'\n  SQL de creacion:\n  {create_sql}')

conn.close()
print('\n' + '=' * 80)
print('Verificacion completada')
