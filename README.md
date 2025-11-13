# 🏟️ Sistema de Alquiler de Canchas Deportivas

Sistema de gestión para alquiler de canchas deportivas, incluyendo gestión de usuarios, reservas, torneos y pagos.

## ✅ Estado Actual

- ✅ **Base de datos SQLite inicializada** con 17 tablas y datos seed
- ✅ **16 modelos de entidad** implementados como dataclasses
- ✅ **14 Repositories completos** con patrón DAO (CRUD completo)
- ✅ **13 Services** de lógica de negocio implementados
- ✅ **13 Routers FastAPI** con endpoints REST
- ✅ **Sistema de conexión** a base de datos configurado con foreign keys
- ✅ **Script de inicialización** automático con verificación de integridad

## 🚀 Inicio Rápido

```bash
# Navegar al backend
cd Backend

# Inicializar la base de datos (recomendado)
cd database
python init_database.py

# O usar el método alternativo
cd ..
python database/connection.py

# Iniciar el servidor FastAPI
uvicorn api.main:app --reload
```

🌐 **API disponible en**: `http://localhost:8000`  
📖 **Documentación Swagger**: `http://localhost:8000/docs`  
📋 **Documentación ReDoc**: `http://localhost:8000/redoc`

### 🔐 Credenciales por Defecto

- **Usuario**: `admin`
- **Email**: `admin@tpdao.com`
- **Password**: `admin123`

📖 **Para más detalles**, consulta [`Backend/database/README_INIT.md`](Backend/database/README_INIT.md) y [`Backend/GETTING_STARTED.md`](Backend/GETTING_STARTED.md)

## 📂 Estructura del Proyecto

```
Backend/
├── api/                  # ✅ API REST con FastAPI
│   ├── main.py          # ✅ Configuración principal FastAPI
│   └── routers/         # ✅ 13 routers implementados
│       ├── clientes.py
│       ├── canchas.py
│       ├── usuarios.py
│       └── ... (10 más)
├── database/            # ✅ Gestión de base de datos
│   ├── connection.py    # ✅ Conexión SQLite
│   ├── init_database.py # ✅ Script de inicialización
│   └── README_INIT.md   # ✅ Documentación DB
├── models/              # ✅ 16 modelos implementados
│   ├── cliente.py
│   ├── cancha.py
│   ├── turno.py
│   └── ... (13 más)
├── repository/          # ✅ 14 repositories completos
│   ├── cliente_repository.py
│   ├── cancha_repository.py
│   ├── usuario_repository.py
│   └── ... (11 más)
├── services/            # ✅ 13 services implementados
│   ├── clientes_services.py
│   ├── canchas_services.py
│   └── ... (11 más)
├── database.db          # ✅ Base de datos SQLite
└── database_inicializar.sql  # ✅ Schema con datos seed
```

## 🏗️ Arquitectura Implementada

### Estructura Monolítica con Organización por Capas (Layered Architecture)

#### 1. **Presentación** (📁 `/Backend/api/routers`)
*   APIs REST con **FastAPI** ✅
*   13 routers implementados (clientes, canchas, usuarios, equipos, torneos, etc.)
*   Validación de entrada y serialización JSON
*   Documentación automática con Swagger/ReDoc
*   **Estado**: ✅ Completado

#### 2. **Lógica de Negocio** (📁 `/Backend/services`)
*   13 servicios implementados
*   Manejo de transacciones y validaciones
*   Creación de instancias de entidades
*   Orquestación entre múltiples repositories
*   Manejo centralizado de excepciones
*   **Estado**: ✅ Completado

#### 3. **Acceso a Datos** (📁 `/Backend/repository`)
*   Patrón DAO (Data Access Object) completo
*   14 repositories con CRUD implementado:
    - ClienteRepository, CanchaRepository, UsuarioRepository
    - TorneoRepository, EquipoRepository, RolRepository
    - TarifaRepository, PartidoRepository, InscripcionRepository
    - PedidoRepository, PedidoItemRepository, PagoRepository
    - EquipoMiembroRepository, ServicioAdicionalRepository
*   Sin lógica de negocio, solo operaciones de persistencia
*   **Estado**: ✅ Completado

#### 4. **Persistencia/Datos** (📁 `/Backend/models` y `/Backend/database`)
*   16 modelos de entidades como dataclasses
*   Base de datos SQLite con 17 tablas
*   Foreign keys habilitadas y verificadas
*   Script de inicialización con datos seed
*   Sistema de índices para optimización
*   **Estado**: ✅ Completado

## 📊 Entidades del Dominio

### Gestión de Usuarios y Roles
- `Rol` - Roles del sistema
- `Usuario` - Usuarios del sistema con autenticación

### Gestión de Clientes
- `Cliente` - Clientes que reservan canchas o participan en torneos

### Gestión de Canchas y Reservas
- `Cancha` - Canchas deportivas disponibles
- `Turno` - Turnos/reservas de canchas
- `Tarifa` - Tarifas por cancha
- `ServicioAdicional` - Servicios extras (iluminación, equipamiento, etc.)
- `TurnoXServicio` - Relación entre turnos y servicios adicionales

### Gestión de Torneos
- `Torneo` - Torneos organizados
- `Equipo` - Equipos participantes
- `EquipoMiembro` - Miembros de cada equipo
- `Inscripcion` - Inscripciones de equipos en torneos
- `Partido` - Partidos del torneo

### Gestión de Pagos
- `Pedido` - Pedidos/órdenes de pago
- `PedidoItem` - Items de cada pedido
- `Pago` - Pagos realizados

## 🛠️ Tecnologías

- **Base de datos**: SQLite3 con foreign keys habilitadas
- **Backend**: Python 3.8+
- **Framework API**: FastAPI con Uvicorn
- **Patrón**: DAO (Data Access Object) + Layered Architecture
- **Documentación**: Swagger UI / ReDoc (automático)
- **Frontend**: React + TypeScript + Vite (en desarrollo)

## 🎯 Funcionalidades Implementadas

### Backend Completo
- ✅ **CRUD completo** para todas las entidades
- ✅ **API REST** con 13 routers y ~65+ endpoints
- ✅ **Gestión de usuarios** con roles (Admin, Operador, Cliente)
- ✅ **Gestión de canchas** con tarifas y servicios adicionales
- ✅ **Sistema de reservas** (turnos) con disponibilidad
- ✅ **Gestión de torneos** con equipos, inscripciones y partidos
- ✅ **Sistema de pedidos** con items y pagos
- ✅ **Validación de integridad** con foreign keys
- ✅ **Documentación automática** de la API

### Datos Iniciales (Seed Data)
- ✅ 3 Roles predefinidos
- ✅ Usuario administrador
- ✅ 3 Canchas de ejemplo
- ✅ 3 Tarifas configuradas
- ✅ 3 Servicios adicionales
- ✅ Cliente y Torneo de prueba

## 📝 Próximos Pasos

1. 🔄 **Conectar frontend React** con el backend FastAPI
2. ⏳ Implementar **autenticación JWT** y sistema de login
3. ⏳ Desarrollar **interfaz de usuario** para todas las funcionalidades
4. ⏳ Agregar **validaciones avanzadas** en la capa de servicios
5. ⏳ Implementar **sistema de notificaciones**
6. ⏳ Agregar **reportes y estadísticas**
7. ⏳ Configurar **CORS** para producción
8. ⏳ Implementar **testing unitario e integración**

## 📚 Documentación Adicional

- **Inicialización de BD**: [`Backend/database/README_INIT.md`](Backend/database/README_INIT.md)
- **Guía de inicio**: [`Backend/GETTING_STARTED.md`](Backend/GETTING_STARTED.md)
- **Documentación completa**: [`Backend/README.md`](Backend/README.md)
- **API Docs (en ejecución)**: `http://localhost:8000/docs`

## 👥 Equipo

**Grupo 22 - 4K1 - TP DAO 2025**

---

## � Estado del Proyecto

| Componente | Estado | Progreso |
|------------|--------|----------|
| Modelos (16) | ✅ Completado | 100% |
| Repositories (14) | ✅ Completado | 100% |
| Services (13) | ✅ Completado | 100% |
| API Routers (13) | ✅ Completado | 100% |
| Base de Datos | ✅ Inicializada | 100% |
| Documentación API | ✅ Automática | 100% |
| Frontend React | 🔄 En desarrollo | 30% |
| Autenticación | ⏳ Pendiente | 0% |
| Testing | ⏳ Pendiente | 0% |

---

�📖 **Documentación completa**: Ver [`Backend/README.md`](Backend/README.md) y [`Backend/database/README_INIT.md`](Backend/database/README_INIT.md)
