# Backend - Sistema de Alquiler de Canchas Deportivas

Este es el backend del sistema de gestión de alquiler de canchas deportivas, que incluye gestión de usuarios, reservas de turnos, torneos y pagos.

## 🚀 Inicio Rápido

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Inicializar base de datos
```bash
# Crear base de datos e insertar datos básicos
python scripts/init_database.py

# O resetear completamente la base de datos
python scripts/init_database.py --reset
```

El script `init_database.py` crea automáticamente:
- ✅ 3 roles (administrador, cliente, empleado)
- ✅ Usuario admin (usuario: `admin`, password: `admin123`)
- ✅ 5 canchas deportivas (fútbol, tenis, paddle, básquet)
- ✅ 7 servicios adicionales
- ✅ 210+ turnos disponibles (próximos 3 días)
- ✅ 1 torneo de ejemplo

### 3. Iniciar la API
```bash
python -m uvicorn api.main:app --reload
```

La API estará disponible en: `http://localhost:8000`

### 4. Login como administrador
```http
POST http://localhost:8000/api/auth/login
Content-Type: application/json

{
  "nombre_usuario": "admin",
  "password": "admin123"
}
```

## 📚 Scripts Disponibles

### `scripts/init_database.py`
Inicializa la base de datos con estructura y datos básicos.
```bash
python scripts/init_database.py          # Inicializar
python scripts/init_database.py --reset  # Resetear y reinicializar
```

### `scripts/migrate_to_new_pago.py`
Migra la base de datos al nuevo modelo de Pago (sin Pedido/PedidoItem).
```bash
python scripts/migrate_to_new_pago.py --check    # Ver estado
python scripts/migrate_to_new_pago.py --execute  # Ejecutar migración
```

### `scripts/create_admin.py`
Crea un usuario administrador adicional.
```bash
python scripts/create_admin.py
```

## 🗂️ Estructura del Proyecto

```
Backend/
├── database/
│   ├── __init__.py
│   └── connection.py          # Gestión de conexión a SQLite
├── models/                    # Modelos de entidad
│   ├── __init__.py
│   ├── rol.py
│   ├── usuario.py
│   ├── cliente.py
│   ├── cancha.py
│   ├── turno.py
│   ├── tarifa.py
│   ├── servicio_adicional.py
│   ├── turno_servicio.py
│   ├── torneo.py
│   ├── equipo.py
│   ├── equipo_miembro.py
│   ├── inscripcion.py
│   ├── partido.py
│   ├── pedido.py
│   ├── pedido_item.py
│   └── pago.py
├── repository/                # Capa de acceso a datos (DAO)
├── services/                  # Lógica de negocio
├── DER_TP_DAO_V2.sql         # Script SQL del esquema
└── database.db               # Base de datos SQLite
```

## 🚀 Inicio Rápido

### Crear/Recrear la Base de Datos

```bash
cd Backend
python database/connection.py
```

Este comando:
- Elimina la base de datos existente (si existe)
- Crea una nueva base de datos SQLite
- Ejecuta el script SQL para crear todas las tablas

### Levantar el backend (desarrollo)

Hay dos entradas distintas en este repositorio:

- `api/main.py` — la aplicación FastAPI principal (la que debe usar `uvicorn`).
- `scripts/demo_main.py` — script de ejemplos y demo movido desde `Backend/main.py` para evitar confusiones.

Para arrancar el servidor HTTP (FastAPI) en desarrollo usa el Python del virtualenv y `uvicorn` desde la carpeta `Backend`:

PowerShell (recomendado):
```powershell
cd 'C:\ruta\a\tu\proyecto\Backend'
..\.venv\Scripts\python.exe -m uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

Si prefieres usar el script de ayuda (`start-backend.ps1` o `start-backend.bat`) creado en el proyecto, puedes ejecutarlo desde la carpeta `Backend`:

PowerShell:
```powershell
cd 'C:\ruta\a\tu\proyecto\Backend'
.\start-backend.ps1 -Port 8000
```

CMD (.bat):
```
cd /d C:\ruta\a\tu\proyecto\Backend
start-backend.bat
```

Verifica que el servidor está arriba abriendo `http://127.0.0.1:8000/docs` en el navegador o:

```powershell
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8000/health
```

### Script de ejemplo / demo

El antiguo `Backend/main.py` que contenía ejemplos se movió a `Backend/scripts/demo_main.py` para evitar conflictos con la aplicación FastAPI (`api/main.py`). Ejecuta el demo con:

```powershell
cd 'C:\ruta\a\tu\proyecto\Backend'
python .\scripts\demo_main.py
```

El script añade automáticamente el path del paquete para que las importaciones relativas funcionen (igual que `scripts/test_register2.py`).

## 📊 Modelo de Datos

### Entidades Principales

#### **Rol**
- `id`: INTEGER (PK, autoincremental)
- `nombre_rol`: VARCHAR(255) UNIQUE NOT NULL
- `descripcion`: VARCHAR(255)

#### **Usuario**
- `id`: INTEGER (PK, autoincremental)
- `nombre_usuario`: VARCHAR(255) UNIQUE NOT NULL
- `email`: VARCHAR(255) UNIQUE NOT NULL
- `password_hash`: VARCHAR(255) NOT NULL
- `id_rol`: INTEGER (FK → Rol)
- `activo`: INTEGER DEFAULT 1

#### **Cliente**
- `id`: INTEGER (PK, autoincremental)
- `nombre`: VARCHAR(255) NOT NULL
- `apellido`: VARCHAR(255)
- `dni`: VARCHAR(255) UNIQUE
- `telefono`: VARCHAR(255) NOT NULL
- `email`: VARCHAR(255)

#### **Cancha**
- `id`: INTEGER (PK, autoincremental)
- `nombre`: VARCHAR(255) NOT NULL
- `tipo_deporte`: VARCHAR(255)
- `descripcion`: TEXT
- `activa`: INTEGER DEFAULT 1

#### **Turno**
- `id`: INTEGER (PK, autoincremental)
- `id_cancha`: INTEGER NOT NULL (FK → Cancha)
- `fecha_hora_inicio`: TEXT NOT NULL
- `fecha_hora_fin`: TEXT NOT NULL
- `estado`: VARCHAR(255) NOT NULL DEFAULT 'disponible'
- `precio_final`: REAL NOT NULL
- `id_cliente`: INTEGER (FK → Cliente)
- `id_usuario_registro`: INTEGER (FK → Usuario)
- `reserva_created_at`: TEXT
- `id_usuario_bloqueo`: INTEGER (FK → Usuario)
- `motivo_bloqueo`: VARCHAR(255)

#### **Tarifa**
- `id`: INTEGER (PK, autoincremental)
- `id_cancha`: INTEGER NOT NULL (FK → Cancha)
- `descripcion`: VARCHAR(255)
- `precio_hora`: REAL NOT NULL

#### **ServicioAdicional**
- `id`: INTEGER (PK, autoincremental)
- `nombre`: VARCHAR(255) NOT NULL
- `precio_actual`: REAL NOT NULL
- `activo`: INTEGER DEFAULT 1

#### **TurnoXServicio** (tabla intermedia)
- `id_turno`: INTEGER (PK, FK → Turno)
- `id_servicio`: INTEGER (PK, FK → ServicioAdicional)
- `cantidad`: INTEGER NOT NULL DEFAULT 1
- `precio_unitario_congelado`: REAL NOT NULL

#### **Torneo**
- `id`: INTEGER (PK, autoincremental)
- `nombre`: VARCHAR(255) NOT NULL
- `tipo_deporte`: VARCHAR(255) NOT NULL
- `created_at`: TEXT DEFAULT CURRENT_TIMESTAMP
- `fecha_inicio`: TEXT
- `fecha_fin`: TEXT
- `costo_inscripcion`: REAL DEFAULT 0
- `cupos`: INTEGER
- `reglas`: TEXT
- `estado`: VARCHAR(255)

#### **Equipo**
- `id`: INTEGER (PK, autoincremental)
- `nombre_equipo`: VARCHAR(255) UNIQUE NOT NULL
- `id_capitan`: INTEGER (FK → Cliente)

#### **EquipoMiembro** (tabla intermedia)
- `id_equipo`: INTEGER (PK, FK → Equipo)
- `id_cliente`: INTEGER (PK, FK → Cliente)

#### **Inscripcion**
- `id`: INTEGER (PK, autoincremental)
- `id_equipo`: INTEGER NOT NULL (FK → Equipo)
- `id_torneo`: INTEGER NOT NULL (FK → Torneo)
- `fecha_inscripcion`: TEXT DEFAULT CURRENT_TIMESTAMP
- `estado`: VARCHAR(255) NOT NULL DEFAULT 'pendiente_pago'

#### **Partido**
- `id`: INTEGER (PK, autoincremental)
- `id_torneo`: INTEGER NOT NULL (FK → Torneo)
- `id_turno`: INTEGER UNIQUE (FK → Turno)
- `id_equipo_local`: INTEGER (FK → Equipo)
- `id_equipo_visitante`: INTEGER (FK → Equipo)
- `id_equipo_ganador`: INTEGER (FK → Equipo)
- `ronda`: VARCHAR(255)
- `marcador_local`: INTEGER
- `marcador_visitante`: INTEGER
- `estado`: VARCHAR(255)

#### **Pedido**
- `id`: INTEGER (PK, autoincremental)
- `id_cliente`: INTEGER NOT NULL (FK → Cliente)
- `monto_total`: REAL NOT NULL
- `estado`: VARCHAR(255) NOT NULL DEFAULT 'pendiente_pago'
- `fecha_creacion`: TEXT DEFAULT CURRENT_TIMESTAMP
- `fecha_expiracion`: TEXT

#### **PedidoItem**
- `id`: INTEGER (PK, autoincremental)
- `id_pedido`: INTEGER NOT NULL (FK → Pedido)
- `id_turno`: INTEGER UNIQUE (FK → Turno)
- `id_inscripcion`: INTEGER UNIQUE (FK → Inscripcion)
- `descripcion`: VARCHAR(255) NOT NULL
- `monto`: REAL NOT NULL

#### **Pago**
- `id`: INTEGER (PK, autoincremental)
- `id_pedido`: INTEGER NOT NULL (FK → Pedido)
- `monto`: REAL NOT NULL
- `estado`: VARCHAR(255) NOT NULL DEFAULT 'iniciado'
- `metodo_pago`: VARCHAR(255)
- `id_gateway_externo`: VARCHAR(255)
- `fecha_pago`: TEXT DEFAULT CURRENT_TIMESTAMP
- `id_usuario_manual`: INTEGER NOT NULL (FK → Usuario)

## 💡 Uso de los Modelos

Todos los modelos incluyen:

### Métodos de clase:
- `from_dict(data: dict)`: Crea una instancia desde un diccionario
- `from_db_row(row)`: Crea una instancia desde una fila de base de datos

### Métodos de instancia:
- `to_dict()`: Convierte la instancia a diccionario

### Ejemplo de uso:

```python
from models import Cliente
from database.connection import get_connection

# Crear un nuevo cliente
cliente = Cliente(
    nombre="Juan",
    apellido="Pérez",
    dni="12345678",
    telefono="1234567890",
    email="juan@example.com"
)

# Convertir a diccionario
cliente_dict = cliente.to_dict()

# Crear desde un diccionario
cliente2 = Cliente.from_dict({
    'nombre': 'María',
    'telefono': '0987654321'
})

# Desde una fila de base de datos
conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM Cliente WHERE id = ?", (1,))
row = cursor.fetchone()
if row:
    cliente_db = Cliente.from_db_row(row)
conn.close()
```

## 🔑 Características de la Base de Datos

- **Foreign Keys**: Habilitadas con `PRAGMA foreign_keys = ON`
- **Índices únicos**:
  - `Turno`: (`id_cancha`, `fecha_hora_inicio`)
  - `Inscripcion`: (`id_equipo`, `id_torneo`)
- **Row Factory**: Configurado para acceder a columnas por nombre

## 📝 Próximos Pasos

1. Implementar la capa de repositorio (DAO) para cada entidad
2. Crear los servicios de negocio
3. Desarrollar las rutas/endpoints de la API
4. Implementar validaciones adicionales
5. Agregar tests unitarios

## 🛠️ Tecnologías

- **Base de datos**: SQLite3
- **Lenguaje**: Python 3.13+
- **Framework**: FastAPI
- **Patrón**: DAO (Data Access Object)
- **Autenticación**: JWT (JSON Web Tokens)

## 📖 Documentación Adicional

- **[COMPARACION_DER_BD.md](COMPARACION_DER_BD.md)** - Análisis detallado: DER vs Base de Datos actual
- **[MIGRACION_NUEVO_PAGO.md](MIGRACION_NUEVO_PAGO.md)** - Documentación del nuevo flujo de pagos sin carrito
- **[DER_TP_DAO_V2.sql](DER_TP_DAO_V2.sql)** - Diagrama Entidad-Relación exportado para MySQL

## 🔄 Flujo de Negocio Principal

### Reserva de Turno
1. Cliente selecciona turno + servicios opcionales
2. Se crea Pago con estado `iniciado` y timer de 15 minutos
3. Turno cambia a `pendiente_pago`
4. Si pago se confirma → Turno: `reservado`, Pago: `completado`
5. Si expira timer → Turno: `disponible`, Pago: `fallido`

### Inscripción a Torneo
1. Equipo se inscribe con estado `pendiente_pago`
2. Se crea Pago con timer de 15 minutos
3. Si pago se confirma → Inscripcion: `confirmada`
4. Si expira timer → Inscripcion: `cancelada`

## 🔐 Credenciales por Defecto

Después de ejecutar `init_database.py`:

| Usuario | Password | Rol | Email |
|---------|----------|-----|-------|
| admin | admin123 | administrador | admin@canchas.com |

⚠️ **IMPORTANTE**: Cambiar estas credenciales en producción.
