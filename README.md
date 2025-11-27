# 🏟️ Sistema de Gestión de Canchas Deportivas

> Sistema completo de gestión y reserva de canchas deportivas con torneos, equipos y pagos.  
> **Stack**: FastAPI + SQLite + React + TypeScript + Vite

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-3178C6.svg)](https://www.typescriptlang.org/)

---

## 📑 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#️-arquitectura)
- [Modelo de Datos](#-modelo-de-datos)
- [Inicio Rápido](#-inicio-rápido)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [API Endpoints](#-api-endpoints)
- [Documentación](#-documentación)

---

## ✨ Características

### 🔐 Gestión de Usuarios y Autenticación
- Registro de usuarios con roles (Admin, Cliente)
- Autenticación JWT con tokens de 5 minutos
- Password hashing con pbkdf2_sha256
- Control de acceso basado en roles

### 🏟️ Gestión de Canchas
- CRUD completo de canchas deportivas
- Múltiples tipos de deporte (Fútbol, Básquet, Pádel)
- Precio por hora configurable
- Estado activo/inactivo

### 📅 Sistema de Turnos y Reservas
- Gestión de turnos con estados:
  - `disponible`: Turno libre para reservar
  - `reservado`: Turno asignado a un cliente
  - `pendiente_pago`: Reserva iniciada, esperando confirmación de pago
  - `bloqueado`: Turno bloqueado por administrador
  - `cancelado`: Turno cancelado
  - `finalizado`: Turno completado
- Cálculo automático de precios basado en:
  - Precio por hora de la cancha
  - Duración del turno
  - Servicios adicionales (luz nocturna)
- Índice único para prevenir doble reserva
- Reserva simple o con pago

### 💳 Sistema de Pagos
- Pagos para turnos individuales o inscripciones a torneos
- Estados de pago: `iniciado`, `completado`, `fallido`
- Timer de expiración de 15 minutos
- Procesamiento automático de pagos expirados
- Desglose detallado: monto turno/inscripción + servicios adicionales

### 🏆 Gestión de Torneos
- Creación y administración de torneos
- Inscripción de equipos
- Gestión de partidos
- Seguimiento de miembros por equipo

### 🛠️ Servicios Adicionales
- Configuración de servicios extras (luces, equipamiento)
- Precios dinámicos por servicio
- Activación/desactivación de servicios

---

## 🏗️ Arquitectura

### Patrón de Capas (Layered Architecture)

```
┌─────────────────────────────────────────────┐
│         Capa de Presentación (API)         │
│     FastAPI Routers + Validación          │
│  • 13 routers REST                         │
│  • Documentación automática (Swagger)      │
│  • Manejo de errores HTTP                  │
└─────────────────────────────────────────────┘
                    ↓ ↑
┌─────────────────────────────────────────────┐
│      Capa de Lógica de Negocio            │
│            Services                         │
│  • Validaciones de negocio                 │
│  • Orquestación de repositories            │
│  • Transacciones                           │
└─────────────────────────────────────────────┘
                    ↓ ↑
┌─────────────────────────────────────────────┐
│       Capa de Acceso a Datos (DAO)        │
│           Repositories                      │
│  • CRUD operations                         │
│  • Queries SQL                             │
│  • Mapeo objeto-relacional                 │
└─────────────────────────────────────────────┘
                    ↓ ↑
┌─────────────────────────────────────────────┐
│          Capa de Persistencia              │
│            SQLite Database                  │
│  • 13 tablas relacionales                  │
│  • Foreign keys + índices                  │
└─────────────────────────────────────────────┘
```

### Patrón DAO (Data Access Object)

Separación clara entre lógica de negocio y acceso a datos:

```python
# Repository (DAO) - Acceso a datos
class CanchaRepository:
    @staticmethod
    def crear(cancha: Cancha) -> int: ...
    
    @staticmethod
    def obtener_por_id(id: int) -> Optional[Cancha]: ...

# Service - Lógica de negocio
class CanchasService:
    def crear_cancha(data: dict) -> Cancha:
        # Validaciones
        # Transformaciones
        # Llamada al repository
```

---

## 📊 Modelo de Datos

### Diagrama Entidad-Relación

El sistema cuenta con **13 tablas principales**:

#### 🔐 Gestión de Acceso
- **Rol**: Roles del sistema (Admin, Cliente)
- **Usuario**: Usuarios con autenticación
- **Cliente**: Perfil de cliente vinculado a usuario

#### 🏟️ Gestión de Canchas
- **Cancha**: Canchas deportivas con precio_hora
- **ServicioAdicional**: Servicios extras (luz, equipos)

#### 📅 Gestión de Turnos
- **Turno**: Turnos/horarios de cancha
- **TurnoServicio**: Relación N:N entre Turno y ServicioAdicional

#### 💳 Gestión de Pagos
- **Pago**: Pagos de turnos e inscripciones

#### 🏆 Gestión de Torneos
- **Torneo**: Torneos organizados
- **Equipo**: Equipos participantes
- **EquipoMiembro**: Miembros de cada equipo
- **Inscripcion**: Inscripciones de equipos a torneos
- **Partido**: Partidos entre equipos

### Relaciones Clave

```
Usuario 1:1 Cliente
Usuario N:1 Rol

Turno N:1 Cancha
Turno N:1 Cliente
Turno N:M ServicioAdicional (a través de TurnoServicio)

Pago N:1 Cliente
Pago 1:1 Turno (opcional)
Pago 1:1 Inscripcion (opcional)

Equipo N:M Torneo (a través de Inscripcion)
Equipo 1:N EquipoMiembro
Partido N:1 Torneo
```

### Características del Schema

✅ **Integridad referencial** con Foreign Keys  
✅ **Índices únicos** para prevenir duplicados  
✅ **Índice compuesto único** en Turno (id_cancha, fecha_hora_inicio)  
✅ **Constraints** para validación a nivel de BD  
✅ **Timestamps** para auditoría  

---

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.13+
- Node.js 18+ (para Frontend)
- Git

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/Ignagg/TP-DAO---4K1---G22---2025.git
cd TP-DAO---4K1---G22---2025
```

### 2️⃣ Backend Setup

```bash
cd Backend

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat
# Linux/Mac:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Inicializar base de datos con datos de prueba
python scripts/init_database.py

# Iniciar servidor FastAPI
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

### 3️⃣ Frontend Setup

```bash
cd Frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

### 4️⃣ Acceder a la aplicación

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc

### 🔐 Credenciales de Prueba

**Administrador**:
- Usuario: `admin`
- Email: `admin@canchas.com`
- Password: `admin123`

---

## 📁 Estructura del Proyecto

```
TP-DAO---4K1---G22---2025/
│
├── Backend/                          # API REST con FastAPI
│   ├── api/                         # Capa de presentación
│   │   ├── main.py                  # Aplicación FastAPI principal
│   │   ├── dependencies/            # Dependencias de autenticación
│   │   │   └── auth.py              # Middleware JWT
│   │   └── routers/                 # Endpoints REST (13 routers)
│   │       ├── auth.py              # Login y autenticación
│   │       ├── usuarios.py          # CRUD usuarios
│   │       ├── clientes.py          # CRUD clientes
│   │       ├── roles.py             # CRUD roles
│   │       ├── canchas.py           # CRUD canchas
│   │       ├── turnos.py            # Gestión de turnos
│   │       ├── servicios_adicionales.py
│   │       ├── pagos.py             # Sistema de pagos
│   │       ├── torneos.py           # CRUD torneos
│   │       ├── equipos.py           # CRUD equipos
│   │       ├── equipo_miembros.py   # Miembros de equipos
│   │       ├── inscripciones.py     # Inscripciones a torneos
│   │       └── partidos.py          # CRUD partidos
│   │
│   ├── services/                    # Lógica de negocio (13 services)
│   │   ├── auth_service.py          # Autenticación JWT
│   │   ├── usuarios_service.py
│   │   ├── clientes_service.py
│   │   ├── roles_service.py
│   │   ├── canchas_service.py
│   │   ├── turnos_service.py
│   │   ├── servicios_adicionales_service.py
│   │   ├── pagos_service.py
│   │   ├── torneos_service.py
│   │   ├── equipos_service.py
│   │   ├── equipo_miembros_service.py
│   │   ├── inscripciones_service.py
│   │   └── partidos_service.py
│   │
│   ├── repositories/                # Capa DAO (13 repositories)
│   │   ├── usuario_repository.py
│   │   ├── cliente_repository.py
│   │   ├── rol_repository.py
│   │   ├── cancha_repository.py
│   │   ├── turno_repository.py
│   │   ├── turno_servicio_repository.py
│   │   ├── servicio_adicional_repository.py
│   │   ├── pago_repository.py
│   │   ├── torneo_repository.py
│   │   ├── equipo_repository.py
│   │   ├── equipo_miembro_repository.py
│   │   ├── inscripcion_repository.py
│   │   └── partido_repository.py
│   │
│   ├── models/                      # Modelos de dominio (13 entidades)
│   │   ├── usuario.py
│   │   ├── cliente.py
│   │   ├── rol.py
│   │   ├── cancha.py
│   │   ├── turno.py
│   │   ├── turno_servicio.py
│   │   ├── servicio_adicional.py
│   │   ├── pago.py
│   │   ├── torneo.py
│   │   ├── equipo.py
│   │   ├── equipo_miembro.py
│   │   ├── inscripcion.py
│   │   └── partido.py
│   │
│   ├── database/                    # Configuración de BD
│   │   └── connection.py            # Conexión SQLite
│   │
│   ├── scripts/                     # Scripts utilitarios
│   │   ├── init_database.py         # ⭐ Inicialización completa
│   │   ├── create_admin.py          # Crear usuario admin
│   │   └── migrate_to_new_pago.py   # Migración de sistema de pagos
│   │
│   ├── tests/                       # Tests unitarios
│   ├── database.db                  # Base de datos SQLite
│   ├── DER_TP_DAO_V2.sql           # Schema SQL completo
│   ├── requirements.txt             # Dependencias Python
│   └── README.md                    # Documentación Backend
│
├── Frontend/                        # Aplicación React
│   ├── src/
│   │   ├── components/              # Componentes React
│   │   ├── contexts/                # Context API (Auth)
│   │   ├── services/                # Servicios API
│   │   ├── App.tsx                  # Componente principal
│   │   └── main.tsx                 # Entry point
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── README.md                    # Documentación Frontend
│
├── .gitignore
└── README.md                        # 📖 Este archivo
```

---

## 🔌 API Endpoints

### 🔐 Autenticación
```
POST   /api/auth/login              # Login usuario
POST   /api/auth/register            # Registro usuario + cliente
```

### 👤 Usuarios y Clientes
```
GET    /api/usuarios                 # Listar usuarios
GET    /api/usuarios/{id}            # Obtener usuario
POST   /api/usuarios                 # Crear usuario
PUT    /api/usuarios/{id}            # Actualizar usuario
DELETE /api/usuarios/{id}            # Eliminar usuario

GET    /api/clientes                 # Listar clientes
GET    /api/clientes/{id}            # Obtener cliente
POST   /api/clientes                 # Crear cliente
PUT    /api/clientes/{id}            # Actualizar cliente
DELETE /api/clientes/{id}            # Eliminar cliente
```

### 🏟️ Canchas y Turnos
```
GET    /api/canchas                  # Listar canchas
GET    /api/canchas/{id}             # Obtener cancha
POST   /api/canchas                  # Crear cancha (admin)
PUT    /api/canchas/{id}             # Actualizar cancha (admin)
DELETE /api/canchas/{id}             # Eliminar cancha (admin)

GET    /api/turnos                   # Listar turnos
GET    /api/turnos/{id}              # Obtener turno
GET    /api/turnos/cancha/{id}       # Turnos por cancha
GET    /api/turnos/cliente/{id}      # Turnos por cliente
GET    /api/turnos/disponibles       # Buscar turnos disponibles
POST   /api/turnos                   # Crear turno
POST   /api/turnos/{id}/reservar-simple  # Reserva directa
PUT    /api/turnos/{id}              # Actualizar turno
DELETE /api/turnos/{id}              # Eliminar turno
```

### 💳 Pagos
```
POST   /api/pagos/turno              # Iniciar pago de turno
POST   /api/pagos/inscripcion        # Iniciar pago de inscripción
POST   /api/pagos/{id}/confirmar     # Confirmar pago
POST   /api/pagos/{id}/marcar-fallido # Marcar pago como fallido
GET    /api/pagos/cliente/{id}       # Pagos por cliente
GET    /api/pagos/turno/{id}         # Pago de un turno
GET    /api/pagos/inscripcion/{id}   # Pago de una inscripción
```

### 🏆 Torneos y Equipos
```
GET    /api/torneos                  # Listar torneos
POST   /api/torneos                  # Crear torneo
GET    /api/torneos/{id}             # Obtener torneo
PUT    /api/torneos/{id}             # Actualizar torneo
DELETE /api/torneos/{id}             # Eliminar torneo

GET    /api/equipos                  # Listar equipos
POST   /api/equipos                  # Crear equipo
GET    /api/equipos/{id}             # Obtener equipo
PUT    /api/equipos/{id}             # Actualizar equipo
DELETE /api/equipos/{id}             # Eliminar equipo

GET    /api/inscripciones            # Listar inscripciones
POST   /api/inscripciones            # Inscribir equipo a torneo
GET    /api/inscripciones/{id}       # Obtener inscripción
DELETE /api/inscripciones/{id}       # Eliminar inscripción

GET    /api/partidos                 # Listar partidos
POST   /api/partidos                 # Crear partido
GET    /api/partidos/{id}            # Obtener partido
PUT    /api/partidos/{id}            # Actualizar partido
DELETE /api/partidos/{id}            # Eliminar partido
```

### 🛠️ Servicios Adicionales
```
GET    /api/servicios-adicionales    # Listar servicios
POST   /api/servicios-adicionales    # Crear servicio (admin)
GET    /api/servicios-adicionales/{id} # Obtener servicio
PUT    /api/servicios-adicionales/{id} # Actualizar servicio (admin)
DELETE /api/servicios-adicionales/{id} # Eliminar servicio (admin)
```

---

## 📖 Documentación

### Backend
- [Backend README](Backend/README.md) - Documentación completa del backend
- [Swagger UI](http://localhost:8000/docs) - Documentación interactiva
- [ReDoc](http://localhost:8000/redoc) - Documentación alternativa
- [DER SQL](Backend/DER_TP_DAO_V2.sql) - Schema de base de datos

### Scripts Importantes
- [init_database.py](Backend/scripts/init_database.py) - Inicialización de BD con datos de prueba
- [create_admin.py](Backend/scripts/create_admin.py) - Crear usuario administrador

### Frontend
- [Frontend README](Frontend/README.md) - Documentación del frontend

---

## 🔧 Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web moderno y rápido
- **SQLite** - Base de datos embebida
- **Pydantic** - Validación de datos
- **python-jose** - JWT para autenticación
- **passlib** - Hashing de passwords (pbkdf2_sha256)
- **uvicorn** - Servidor ASGI

### Frontend
- **React 18** - Biblioteca UI
- **TypeScript** - Tipado estático
- **Vite** - Build tool
- **Axios** - Cliente HTTP
- **React Router** - Enrutamiento

---

## 👥 Equipo

**Grupo 22 - 4K1 - 2025**

---

## 📝 Licencia

Este proyecto es parte de un trabajo práctico académico.

---

## 🐛 Troubleshooting

### Base de datos corrupta
```bash
cd Backend
rm database.db  # Eliminar BD
python scripts/init_database.py --reset  # Recrear
```

### Token expirado
Los tokens JWT expiran a los 5 minutos. Volver a hacer login.

### Puerto 8000 ocupado
```bash
# Cambiar puerto
uvicorn api.main:app --reload --port 8001
```

### Problemas con virtual environment
```bash
# Recrear venv
rm -rf .venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 📮 Contacto

Para consultas sobre el proyecto, contactar al equipo de desarrollo.
