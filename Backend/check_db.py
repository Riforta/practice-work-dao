import sqlite3

conn = sqlite3.connect('club.db')
cursor = conn.cursor()

# Ver esquema de Cliente
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='Cliente'")
result = cursor.fetchone()
print("=== Tabla Cliente ===")
print(result[0] if result else "No encontrado")

# Ver esquema de Usuario
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='Usuario'")
result = cursor.fetchone()
print("\n=== Tabla Usuario ===")
print(result[0] if result else "No encontrado")

# Ver clientes existentes
cursor.execute("SELECT * FROM Cliente LIMIT 5")
print("\n=== Clientes existentes ===")
for row in cursor.fetchall():
    print(row)

# Ver usuarios existentes
cursor.execute("SELECT * FROM Usuario LIMIT 5")
print("\n=== Usuarios existentes ===")
for row in cursor.fetchall():
    print(row)

conn.close()
