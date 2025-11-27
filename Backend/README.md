# 🔧 Backend - Sistema de Gestión de Canchas Deportivas

> API REST construida con **FastAPI** y **SQLite** siguiendo el patrón DAO (Data Access Object) y arquitectura en capas.

---

## 📑 Tabla de Contenidos

- [Arquitectura](#️-arquitectura)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [Configuración de Base de Datos](#️-configuración-de-base-de-datos)
- [Ejecución](#-ejecución)
- [Estructura de Carpetas](#-estructura-de-carpetas)
- [Modelo de Datos](#-modelo-de-datos)
- [API Endpoints](#-api-endpoints)
- [Autenticación](#-autenticación)
- [Testing](#-testing)

---

## 🏗️ Arquitectura

### Patrón de Capas

```
┌──────────────────────────────────────┐
│     API Layer (Routers)             │  ← FastAPI, HTTP, Validación
├──────────────────────────────────────┤
│     Business Logic (Services)       │  ← Lógica de negocio, Validaciones
├──────────────────────────────────────┤
│     Data Access (Repositories)      │  ← Patrón DAO, SQL Queries
├──────────────────────────────────────┤
│     Domain Models                    │  ← Entidades del dominio
├──────────────────────────────────────┤
│     Database (SQLite)                │  ← Persistencia
└──────────────────────────────────────┘
```

### Flujo de una Request

```
HTTP Request (POST /api/turnos)
        ↓
Router (turnos.py)
  • Validación de entrada
  • Autenticación JWT
        ↓
Service (turnos_service.py)
  • Validaciones de negocio
  • Cálculo de precios
  • Orquestación de repositories
        ↓
Repository (turno_repository.py)
  • Queries SQL
  • Mapeo objeto-relacional
        ↓
Database (SQLite)
  • Persistencia
        ↓
Response (JSON)
```

---

## 🛠️ Tecnologías

| Tecnología | Versión | Propósito |
|-----------|---------|-----------|
| Python | 3.13+ | Lenguaje base |
| FastAPI | 0.104+ | Framework web |
| SQLite | 3.x | Base de datos |
| python-jose | 3.3+ | JWT tokens |
| passlib | 1.7+ | Password hashing |
| uvicorn | 0.24+ | Servidor ASGI |
| pytest | 7.4+ | Testing |

---

## 💾 Instalación

### 1. Prerrequisitos

- Python 3.13 o superior
- pip (gestor de paquetes Python)
- Git

### 2. Clonar el repositorio

```bash
git clone https://github.com/Ignagg/TP-DAO---4K1---G22---2025.git
cd TP-DAO---4K1---G22---2025/Backend
```

### 3. Crear entorno virtual

```bash
# Crear venv
python -m venv .venv

# Activar venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# Windows CMD:
.venv\Scripts\activate.bat

# Linux/Mac:
source .venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 🗄️ Configuración de Base de Datos

### Opción 1: Script de Inicialización (Recomendado)

El script `init_database.py` crea todas las tablas e inserta datos de prueba:

```bash
# Inicialización normal
python scripts/init_database.py

# Resetear BD (elimina y recrea todo)
python scripts/init_database.py --reset
```

**Datos creados automáticamente:**
- ✅ 3 Roles (Admin, Cliente, Organizador)
- ✅ 1 Usuario Admin (admin/admin123)
- ✅ 5 Canchas (Fútbol, Básquet, Pádel)
- ✅ 7 Servicios Adicionales (luces, equipos)
- ✅ 210 Turnos (próximos 3 días)
- ✅ 1 Torneo de ejemplo

### Opción 2: Solo crear las tablas

```bash
python database/connection.py
```

### Opción 3: Ejecutar SQL manualmente

```bash
sqlite3 database.db < DER_TP_DAO_V2.sql
```

### Verificar la base de datos

```bash
# Entrar a SQLite
sqlite3 database.db

# Listar tablas
.tables

# Ver estructura de tabla
.schema Usuario

# Contar registros
SELECT COUNT(*) FROM Usuario;

# Salir
.exit
```

---

## 🚀 Ejecución

### Modo Desarrollo

```bash
# Desde la carpeta Backend/
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

**Opciones útiles:**
- `--reload`: Recarga automática al cambiar código
- `--host 127.0.0.1`: IP del servidor
- `--port 8000`: Puerto del servidor
- `--log-level debug`: Logs detallados

### Modo Producción

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Acceso a la API

- **API Base**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## 📂 Estructura de Carpetas

```
Backend/
│
├── api/                                # Capa de Presentación
│   ├── main.py                         # ⭐ App FastAPI principal
│   ├── dependencies/
│   │   └── auth.py                     # Middleware autenticación JWT
│   └── routers/                        # 13 routers REST
│       ├── __init__.py                 # Registro de routers
│       ├── auth.py                     # Login, registro
│       ├── usuarios.py                 # CRUD usuarios
│       ├── clientes.py                 # CRUD clientes
│       ├── roles.py                    # CRUD roles
│       ├── canchas.py                  # CRUD canchas
│       ├── turnos.py                   # Gestión turnos y reservas
│       ├── servicios_adicionales.py    # CRUD servicios
│       ├── pagos.py                    # Sistema de pagos
│       ├── torneos.py                  # CRUD torneos
│       ├── equipos.py                  # CRUD equipos
│       ├── equipo_miembros.py          # Miembros de equipos
│       ├── inscripciones.py            # Inscripciones a torneos
│       └── partidos.py                 # CRUD partidos
│
├── services/                           # Capa de Lógica de Negocio
│   ├── __init__.py
│   ├── auth_service.py                 # Autenticación, JWT, passwords
│   ├── usuarios_service.py             # Lógica usuarios
│   ├── clientes_service.py             # Lógica clientes
│   ├── roles_service.py                # Lógica roles
│   ├── canchas_service.py              # Lógica canchas
│   ├── turnos_service.py               # Validaciones turnos, cálculo precios
│   ├── turno_servicios_service.py      # Asociación turnos-servicios
│   ├── servicios_adicionales_service.py # Lógica servicios
│   ├── pagos_service.py                # Flujo de pagos, timer 15min
│   ├── torneos_service.py              # Lógica torneos
│   ├── equipos_service.py              # Lógica equipos
│   ├── equipo_miembros_service.py      # Lógica miembros
│   ├── inscripciones_service.py        # Lógica inscripciones
│   └── partidos_service.py             # Lógica partidos
│
├── repositories/                       # Capa de Acceso a Datos (DAO)
│   ├── __init__.py
│   ├── usuario_repository.py           # CRUD Usuario
│   ├── cliente_repository.py           # CRUD Cliente
│   ├── rol_repository.py               # CRUD Rol
│   ├── cancha_repository.py            # CRUD Cancha
│   ├── turno_repository.py             # CRUD Turno
│   ├── turno_servicio_repository.py    # CRUD TurnoServicio
│   ├── servicio_adicional_repository.py # CRUD ServicioAdicional
│   ├── pago_repository.py              # CRUD Pago
│   ├── torneo_repository.py            # CRUD Torneo
│   ├── equipo_repository.py            # CRUD Equipo
│   ├── equipo_miembro_repository.py    # CRUD EquipoMiembro
│   ├── inscripcion_repository.py       # CRUD Inscripcion
│   └── partido_repository.py           # CRUD Partido
│
├── models/                             # Capa de Dominio
│   ├── __init__.py
│   ├── usuario.py                      # @dataclass Usuario
│   ├── cliente.py                      # @dataclass Cliente
│   ├── rol.py                          # @dataclass Rol
│   ├── cancha.py                       # @dataclass Cancha
│   ├── turno.py                        # @dataclass Turno
│   ├── turno_servicio.py               # @dataclass TurnoServicio
│   ├── servicio_adicional.py           # @dataclass ServicioAdicional
│   ├── pago.py                         # @dataclass Pago
│   ├── torneo.py                       # @dataclass Torneo
│   ├── equipo.py                       # @dataclass Equipo
│   ├── equipo_miembro.py               # @dataclass EquipoMiembro
│   ├── inscripcion.py                  # @dataclass Inscripcion
│   └── partido.py                      # @dataclass Partido
│
├── database/
│   └── connection.py                   # Conexión SQLite, get_connection()
│
├── scripts/                            # Scripts utilitarios
│   ├── init_database.py                # ⭐ Inicialización completa
│   ├── create_admin.py                 # Crear admin manualmente
│   └── migrate_to_new_pago.py          # Migración sistema pagos
│
├── tests/                              # Tests unitarios
│   ├── test_usuarios_clientes_basic.py
│   ├── test_turno_routes.py
│   ├── test_turno_service.py
│   ├── test_turno_routes_pertenencia.py
│   └── test_flujo_reserva.py
│
├── database.db                         # Base de datos SQLite
├── DER_TP_DAO_V2.sql                  # Schema completo
├── requirements.txt                    # Dependencias
├── utils.py                            # Utilidades generales
└── README.md                           # Este archivo
```

---

## 📊 Modelo de Datos

### Entidades Principales

#### 1. Gestión de Acceso

**Rol**
```python
@dataclass
class Rol:
    id: Optional[int]
    nombre_rol: str              # Admin, Cliente, Organizador
    descripcion: Optional[str]
```

**Usuario**
```python
@dataclass
class Usuario:
    id: Optional[int]
    nombre_usuario: str          # Único
    email: str                   # Único
    password_hash: str           # pbkdf2_sha256
    id_rol: int                  # FK → Rol
```

**Cliente**
```python
@dataclass
class Cliente:
    id: Optional[int]
    nombre: str
    apellido: Optional[str]
    dni: Optional[str]           # Único
    telefono: str
    direccion: Optional[str]
    id_usuario: int              # FK → Usuario (único)
```

#### 2. Gestión de Canchas

**Cancha**
```python
@dataclass
class Cancha:
    id: Optional[int]
    nombre: str
    tipo_deporte: Optional[str]  # Fútbol, Básquet, Pádel
    descripcion: Optional[str]
    activa: int                  # 1=activa, 0=inactiva
    precio_hora: Optional[float] # ⭐ Precio base por hora
```

**ServicioAdicional**
```python
@dataclass
class ServicioAdicional:
    id: Optional[int]
    nombre: str
    precio_actual: float
    activo: int                  # 1=activo, 0=inactivo
```

#### 3. Gestión de Turnos

**Turno**
```python
@dataclass
class Turno:
    id: Optional[int]
    id_cancha: int                    # FK → Cancha
    fecha_hora_inicio: str            # ISO datetime
    fecha_hora_fin: str               # ISO datetime
    estado: str                       # disponible, reservado, pendiente_pago, etc.
    precio_final: float               # Calculado
    id_cliente: Optional[int]         # FK → Cliente
    id_usuario_registro: Optional[int] # FK → Usuario
    reserva_created_at: Optional[str]
    id_usuario_bloqueo: Optional[int]
    motivo_bloqueo: Optional[str]
```

**Estados de Turno:**
- `disponible`: Turno libre
- `reservado`: Turno confirmado con cliente
- `pendiente_pago`: Reserva iniciada, esperando pago
- `bloqueado`: Bloqueado por admin
- `cancelado`: Turno cancelado
- `finalizado`: Turno completado

**TurnoServicio** (Tabla de relación N:M)
```python
@dataclass
class TurnoServicio:
    id: Optional[int]
    id_turno: int                # FK → Turno
    id_servicio: int             # FK → ServicioAdicional
    cantidad: int
    precio_unitario: float
```

#### 4. Gestión de Pagos

**Pago**
```python
@dataclass
class Pago:
    id: Optional[int]
    id_cliente: int               # FK → Cliente
    id_turno: Optional[int]       # FK → Turno (XOR con id_inscripcion)
    id_inscripcion: Optional[int] # FK → Inscripcion (XOR con id_turno)
    monto_turno: float
    monto_servicios: float
    monto_inscripcion: float
    descuento: float
    recargo: float
    monto_total: float
    metodo_pago: Optional[str]
    estado: str                   # iniciado, completado, fallido
    fecha_creacion: str
    fecha_vencimiento: str        # +15 minutos desde creación
    fecha_pago: Optional[str]
```

**Flujo de Pago:**
1. Cliente reserva turno/inscripción → Pago `iniciado`
2. Timer 15 minutos comienza
3. Cliente confirma → Pago `completado` + Turno/Inscripción actualizado
4. Si expira timer → Job marca Pago `fallido` + libera Turno

#### 5. Gestión de Torneos

**Torneo**
```python
@dataclass
class Torneo:
    id: Optional[int]
    nombre: str
    descripcion: Optional[str]
    fecha_inicio: str
    fecha_fin: str
    deporte: Optional[str]
    ubicacion: Optional[str]
    id_organizador: Optional[int]  # FK → Usuario
    estado: str                    # pendiente, en_curso, finalizado
    precio_inscripcion: float
```

**Equipo**
```python
@dataclass
class Equipo:
    id: Optional[int]
    nombre: str
    id_capitan: int                # FK → Cliente
```

**EquipoMiembro**
```python
@dataclass
class EquipoMiembro:
    id: Optional[int]
    id_equipo: int                 # FK → Equipo
    id_cliente: int                # FK → Cliente
    posicion: Optional[str]
    numero_camiseta: Optional[int]
```

**Inscripcion** (Equipo inscrito en Torneo)
```python
@dataclass
class Inscripcion:
    id: Optional[int]
    id_torneo: int                 # FK → Torneo
    id_equipo: int                 # FK → Equipo
    fecha_inscripcion: str
    estado: str                    # pendiente, confirmada, cancelada
```

**Partido**
```python
@dataclass
class Partido:
    id: Optional[int]
    id_torneo: int                 # FK → Torneo
    id_equipo_local: int           # FK → Equipo
    id_equipo_visitante: int       # FK → Equipo
    fecha_hora: str
    id_cancha: Optional[int]       # FK → Cancha
    resultado_local: Optional[int]
    resultado_visitante: Optional[int]
    estado: str                    # programado, en_curso, finalizado, suspendido
```

### Relaciones

```
Usuario 1:1 Cliente
Usuario N:1 Rol

Turno N:1 Cancha
Turno N:1 Cliente
Turno N:M ServicioAdicional (TurnoServicio)

Pago N:1 Cliente
Pago 1:0..1 Turno
Pago 1:0..1 Inscripcion

Equipo N:1 Cliente (capitán)
EquipoMiembro N:1 Equipo
EquipoMiembro N:1 Cliente

Inscripcion N:1 Torneo
Inscripcion N:1 Equipo

Partido N:1 Torneo
Partido N:1 Equipo (local)
Partido N:1 Equipo (visitante)
Partido N:1 Cancha
```

### Índices y Constraints

✅ **Índice único compuesto**: `(id_cancha, fecha_hora_inicio)` en Turno  
✅ **Índice**: `id_usuario_email` en Usuario  
✅ **Índice**: `id_turno_cancha` en Turno  
✅ **Foreign Keys** activadas con `PRAGMA foreign_keys = ON`  
✅ **Unique constraints** en nombre_usuario, email, dni  

---

## 🔌 API Endpoints

### Convenciones

- **Base URL**: `/api`
- **Content-Type**: `application/json`
- **Auth**: Bearer token en header `Authorization`

### Autenticación

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/auth/login` | Login usuario | No |
| POST | `/auth/register` | Registro usuario + cliente | No |

**Request Login:**
```json
{
  "usuario": "admin",
  "password": "admin123"
}
```

**Response Login:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "nombre_usuario": "admin",
    "email": "admin@canchas.com",
    "id_rol": 1
  }
}
```

### Usuarios

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/usuarios` | Listar todos | Sí |
| GET | `/usuarios/{id}` | Obtener por ID | Sí |
| POST | `/usuarios` | Crear | Admin |
| PUT | `/usuarios/{id}` | Actualizar | Admin |
| DELETE | `/usuarios/{id}` | Eliminar | Admin |

### Clientes

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/clientes` | Listar todos | Sí |
| GET | `/clientes/{id}` | Obtener por ID | Sí |
| GET | `/clientes/usuario/{id}` | Por usuario | Sí |
| POST | `/clientes` | Crear | Admin |
| PUT | `/clientes/{id}` | Actualizar | Sí |
| DELETE | `/clientes/{id}` | Eliminar | Admin |

### Canchas

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/canchas` | Listar todas | No |
| GET | `/canchas/{id}` | Obtener por ID | No |
| POST | `/canchas` | Crear | Admin |
| PUT | `/canchas/{id}` | Actualizar | Admin |
| DELETE | `/canchas/{id}` | Eliminar | Admin |

### Turnos

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/turnos` | Listar todos | Sí |
| GET | `/turnos/{id}` | Obtener por ID | Sí |
| GET | `/turnos/cancha/{id}` | Por cancha | Sí |
| GET | `/turnos/cliente/{id}` | Por cliente | Sí |
| GET | `/turnos/disponibles` | Buscar disponibles | Sí |
| POST | `/turnos` | Crear turno | Admin |
| POST | `/turnos/{id}/reservar-simple` | Reservar | Sí |
| PUT | `/turnos/{id}` | Actualizar | Admin |
| PATCH | `/turnos/{id}/estado` | Cambiar estado | Admin |
| DELETE | `/turnos/{id}` | Eliminar | Admin |

**Request Crear Turno:**
```json
{
  "id_cancha": 1,
  "fecha_hora_inicio": "2025-11-28T18:00:00",
  "fecha_hora_fin": "2025-11-28T19:30:00",
  "estado": "disponible",
  "precio_final": 1500.0
}
```

**Request Reservar:**
```json
{
  "id_cliente": 5,
  "id_usuario_registro": 1
}
```

### Pagos

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/pagos/turno` | Iniciar pago turno | Sí |
| POST | `/pagos/inscripcion` | Iniciar pago inscripción | Sí |
| POST | `/pagos/{id}/confirmar` | Confirmar pago | Sí |
| POST | `/pagos/{id}/marcar-fallido` | Marcar fallido | Admin |
| GET | `/pagos/cliente/{id}` | Pagos de cliente | Sí |
| GET | `/pagos/turno/{id}` | Pago de turno | Sí |
| GET | `/pagos/inscripcion/{id}` | Pago de inscripción | Sí |

**Request Iniciar Pago Turno:**
```json
{
  "id_turno": 10,
  "id_cliente": 5,
  "metodo_pago": "efectivo"
}
```

**Response Pago:**
```json
{
  "id": 15,
  "id_cliente": 5,
  "id_turno": 10,
  "monto_turno": 1500.0,
  "monto_servicios": 300.0,
  "monto_total": 1800.0,
  "estado": "iniciado",
  "fecha_vencimiento": "2025-11-27T19:15:00"
}
```

### Torneos

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/torneos` | Listar todos | No |
| GET | `/torneos/{id}` | Obtener por ID | No |
| POST | `/torneos` | Crear | Admin |
| PUT | `/torneos/{id}` | Actualizar | Admin |
| DELETE | `/torneos/{id}` | Eliminar | Admin |

### Equipos

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/equipos` | Listar todos | Sí |
| GET | `/equipos/{id}` | Obtener por ID | Sí |
| POST | `/equipos` | Crear | Sí |
| PUT | `/equipos/{id}` | Actualizar | Sí |
| DELETE | `/equipos/{id}` | Eliminar | Admin |

### Inscripciones

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/inscripciones` | Listar todas | Sí |
| GET | `/inscripciones/{id}` | Obtener por ID | Sí |
| GET | `/inscripciones/torneo/{id}` | Por torneo | Sí |
| POST | `/inscripciones` | Inscribir equipo | Sí |
| PUT | `/inscripciones/{id}` | Actualizar estado | Admin |
| DELETE | `/inscripciones/{id}` | Cancelar | Admin |

### Partidos

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/partidos` | Listar todos | Sí |
| GET | `/partidos/{id}` | Obtener por ID | Sí |
| GET | `/partidos/torneo/{id}` | Por torneo | Sí |
| POST | `/partidos` | Crear | Admin |
| PUT | `/partidos/{id}` | Actualizar | Admin |
| DELETE | `/partidos/{id}` | Eliminar | Admin |

---

## 🔐 Autenticación

### JWT (JSON Web Tokens)

El sistema usa tokens JWT con las siguientes características:

- **Algoritmo**: HS256
- **Expiración**: 5 minutos
- **Claims**:
  - `sub`: nombre_usuario
  - `user_id`: ID del usuario
  - `id_rol`: ID del rol
  - `iat`: Issued at (timestamp)
  - `exp`: Expiration (timestamp)

### Flujo de Autenticación

```
1. Cliente → POST /api/auth/login
             {usuario, password}

2. Backend → Valida credenciales
             Genera JWT token

3. Backend → Responde con token
             {access_token, user}

4. Cliente → Guarda token
             (localStorage/sessionStorage)

5. Cliente → Requests subsiguientes
             Header: Authorization: Bearer <token>

6. Backend → Valida token en cada request
             Dependency: get_current_user()
```

### Middleware de Autenticación

```python
# api/dependencies/auth.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Usuario:
    token = credentials.credentials
    usuario = AuthService.validar_token(token)
    if not usuario:
        raise HTTPException(401, "Token inválido o expirado")
    return usuario

def require_admin(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    if current_user.id_rol != 1:  # 1 = Admin
        raise HTTPException(403, "Requiere permisos de administrador")
    return current_user
```

### Uso en Routers

```python
from api.dependencies.auth import get_current_user, require_admin

# Endpoint público
@router.get("/canchas")
def listar_canchas(): ...

# Endpoint autenticado
@router.get("/turnos")
def listar_turnos(current_user: Usuario = Depends(get_current_user)): ...

# Endpoint admin
@router.post("/canchas")
def crear_cancha(admin: Usuario = Depends(require_admin)): ...
```

### Password Hashing

```python
from passlib.hash import pbkdf2_sha256

# Hash password
hashed = pbkdf2_sha256.hash("admin123")

# Verificar password
is_valid = pbkdf2_sha256.verify("admin123", hashed)
```

---

## 🧪 Testing

### Ejecutar tests

```bash
# Todos los tests
pytest

# Con coverage
pytest --cov=. --cov-report=html

# Test específico
pytest tests/test_usuarios_clientes_basic.py

# Verbose
pytest -v

# Con prints
pytest -s
```

### Tests disponibles

| Test | Descripción |
|------|-------------|
| `test_usuarios_clientes_basic.py` | CRUD básico usuarios/clientes |
| `test_turno_routes.py` | Endpoints de turnos |
| `test_turno_service.py` | Lógica de negocio turnos |
| `test_turno_routes_pertenencia.py` | Autorización turnos |
| `test_flujo_reserva.py` | Flujo completo de reserva |

### Estructura de un Test

```python
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_crear_usuario():
    response = client.post("/api/usuarios", json={
        "nombre_usuario": "test",
        "email": "test@test.com",
        "password": "test123",
        "id_rol": 2
    })
    assert response.status_code == 201
    data = response.json()
    assert data["nombre_usuario"] == "test"
```

---

## 🔧 Scripts Utilitarios

### init_database.py

Inicialización completa de la base de datos con datos de prueba.

```bash
# Normal
python scripts/init_database.py

# Reset completo
python scripts/init_database.py --reset
```

**Funciones:**
- `crear_tablas()`: Crea schema completo
- `crear_indices()`: Crea índices optimizados
- `insertar_datos_basicos()`: Inserta datos seed
- `resetear_base_datos()`: Elimina y recrea todo

**Datos insertados:**
- 3 Roles
- 1 Admin (admin/admin123)
- 5 Canchas
- 7 Servicios
- 210 Turnos (próximos 3 días)
- 1 Torneo

### create_admin.py

Crear usuario administrador manualmente.

```bash
python scripts/create_admin.py
```

Crea:
- Usuario: `admin`
- Email: `admin@canchas.com`
- Password: `admin123`
- Rol: Administrador

### migrate_to_new_pago.py

Migración del sistema de pagos (Pedido → Pago directo).

```bash
# Ver cambios
python scripts/migrate_to_new_pago.py --check

# Ejecutar migración
python scripts/migrate_to_new_pago.py --execute
```

---

## 🐛 Troubleshooting

### Error: No such table

```bash
# Recrear base de datos
python scripts/init_database.py --reset
```

### Error: Token expired

Los tokens expiran a los 5 minutos. Volver a hacer login.

### Error: Foreign key constraint failed

Verificar que las foreign keys existen antes de insertar:

```sql
PRAGMA foreign_keys = ON;
SELECT * FROM Rol WHERE id = 1;
```

### Error: Port already in use

```bash
# Cambiar puerto
uvicorn api.main:app --reload --port 8001

# O matar proceso
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9
```

### Error: Module not found

```bash
# Reinstalar dependencias
pip install -r requirements.txt

# O recrear venv
rm -rf .venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 📚 Referencias

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLite Docs](https://www.sqlite.org/docs.html)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [JWT.io](https://jwt.io/)

---

## 👥 Contribución

Este es un proyecto académico. Para consultas, contactar al equipo.

---

## 📝 Notas de Versión

### v2.0 - Noviembre 2025
- ✅ Eliminada tabla Tarifa (usar Cancha.precio_hora)
- ✅ Sistema de pagos directo (sin Pedido/PedidoItem)
- ✅ JWT con timezone-aware (Python 3.12+)
- ✅ Password hashing unificado (pbkdf2_sha256)
- ✅ Índice único en Turno para prevenir doble reserva
- ✅ Timer 15 minutos para pagos
- ✅ Script init_database.py completo
