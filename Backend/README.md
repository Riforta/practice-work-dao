# Backend - Sistema de Alquiler de Canchas Deportivas

Este es el backend del sistema de gestión de alquiler de canchas deportivas, que incluye gestión de usuarios, reservas de turnos, torneos y pagos.

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
- **Lenguaje**: Python 3
- **Patrón**: DAO (Data Access Object)
