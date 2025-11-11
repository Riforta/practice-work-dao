# 🚀 Guía de Inicio Rápido

## Configuración Inicial

### 1. Crear la Base de Datos

```bash
cd Backend
python database/connection.py
```

Esto creará el archivo `database.db` con todas las tablas definidas en el esquema SQL.

### 2. Verificar la Instalación

```bash
python test_setup.py
```

Este script verifica que:
- ✅ Todas las tablas se crearon correctamente
- ✅ Los modelos funcionan
- ✅ El repositorio funciona
- ✅ Se pueden realizar operaciones CRUD

### 3. Ejecutar el Ejemplo

```bash
python main.py
```

## 📁 Estructura del Proyecto

```
Backend/
├── database/              # Gestión de conexión a DB
│   ├── __init__.py
│   └── connection.py     # get_connection(), init_database()
│
├── models/               # Modelos de entidad (dataclasses)
│   ├── cliente.py       # Cliente, Cancha, Turno, etc.
│   └── ...
│
├── repository/          # Capa DAO (Data Access Object)
│   ├── cliente_repository.py   # CRUD de Cliente
│   └── ...                     # Crear más según necesites
│
├── services/            # Lógica de negocio
│   └── ...              # A implementar
│
├── DER_TP_DAO_V2.sql   # Script SQL del esquema
├── database.db          # Base de datos SQLite
├── main.py             # Ejemplo de uso
└── test_setup.py       # Script de verificación
```

## 💡 Ejemplos de Uso

### Modelo Cliente

```python
from models import Cliente
from repository import ClienteRepository

# Crear cliente
cliente = Cliente(
    nombre="Juan",
    apellido="Pérez",
    dni="12345678",
    telefono="351-1234567",
    email="juan@example.com"
)

# Guardar en DB
cliente_id = ClienteRepository.crear(cliente)

# Obtener por ID
cliente = ClienteRepository.obtener_por_id(cliente_id)

# Buscar por nombre
resultados = ClienteRepository.buscar_por_nombre("Juan")

# Actualizar
cliente.telefono = "351-9999999"
ClienteRepository.actualizar(cliente)

# Listar todos
todos = ClienteRepository.obtener_todos()
```

### Consulta SQL Directa

```python
from database.connection import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT * FROM Cliente WHERE nombre LIKE ?", ("%Juan%",))
resultados = cursor.fetchall()

for row in resultados:
    print(row['nombre'], row['email'])

conn.close()
```

## 🔄 Próximos Pasos

### 1. Implementar más Repositories

Crear archivos similares a `cliente_repository.py` para:
- `cancha_repository.py`
- `turno_repository.py`
- `usuario_repository.py`
- etc.

### 2. Crear Servicios de Negocio

En la carpeta `services/`, implementar la lógica de negocio:
- Validaciones complejas
- Reglas de negocio
- Cálculo de precios
- Gestión de reservas

### 3. Agregar API REST

Puedes usar FastAPI o Flask:

```python
# Con FastAPI
from fastapi import FastAPI
from models import Cliente

app = FastAPI()

@app.post("/clientes")
def crear_cliente(cliente: Cliente):
    cliente_id = ClienteRepository.crear(cliente)
    return {"id": cliente_id}
```

### 4. Agregar Validaciones

```python
# En el repository o service
def crear_cliente(self, cliente: Cliente):
    # Validar DNI único
    if ClienteRepository.existe_dni(cliente.dni):
        raise ValueError("El DNI ya existe")
    
    # Validar email
    if not self._validar_email(cliente.email):
        raise ValueError("Email inválido")
    
    return ClienteRepository.crear(cliente)
```

### 5. Implementar Autenticación

```python
# Hash de contraseñas
import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())
```

## 📝 Comandos Útiles

```bash
# Recrear la base de datos desde cero
python database/connection.py

# Verificar que todo funciona
python test_setup.py

# Ver ejemplo completo
python main.py

# Acceder a la DB con SQLite (si tienes el cliente)
sqlite3 database.db
```

## 🐛 Solución de Problemas

### Error: "no such table"
- Ejecuta `python database/connection.py` para crear las tablas

### Error: "FOREIGN KEY constraint failed"
- Asegúrate de que los registros referenciados existen
- Verifica que `PRAGMA foreign_keys = ON` esté activo

### Error: "UNIQUE constraint failed"
- Estás intentando insertar un valor duplicado en un campo único (ej: DNI, email)

## 📚 Recursos

- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Python sqlite3 Module](https://docs.python.org/3/library/sqlite3.html)
- [Python Dataclasses](https://docs.python.org/3/library/dataclasses.html)

---

**¿Necesitas ayuda?** Revisa los archivos de ejemplo o contacta al equipo de desarrollo.
