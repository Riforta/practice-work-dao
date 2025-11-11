# 🏟️ Sistema de Alquiler de Canchas Deportivas

Sistema de gestión para alquiler de canchas deportivas, incluyendo gestión de usuarios, reservas, torneos y pagos.

## ✅ Estado Actual

- ✅ **Base de datos SQLite creada** con todas las tablas definidas
- ✅ **16 modelos de entidad** implementados como dataclasses
- ✅ **Repository Pattern** implementado (ejemplo: ClienteRepository)
- ✅ **Sistema de conexión** a base de datos configurado
- ✅ **Scripts de prueba** y ejemplos funcionales

## 🚀 Inicio Rápido

```bash
# Navegar al backend
cd Backend

# Crear la base de datos
python database/connection.py

# Verificar la instalación
python test_setup.py

# Ver ejemplo de uso
python main.py
```

📖 **Para más detalles**, consulta [`Backend/GETTING_STARTED.md`](Backend/GETTING_STARTED.md)

## 📂 Estructura del Proyecto

```
Backend/
├── database/              # ✅ Gestión de conexión a SQLite
│   └── connection.py
├── models/               # ✅ 16 modelos de entidad implementados
│   ├── cliente.py
│   ├── cancha.py
│   ├── turno.py
│   └── ... (13 más)
├── repository/           # 🔄 En desarrollo
│   └── cliente_repository.py
├── services/             # ⏳ Pendiente
├── routes/               # ⏳ Pendiente (FastAPI/Flask)
├── database.db          # ✅ Base de datos SQLite
└── DER_TP_DAO_V2.sql   # ✅ Esquema de base de datos
```

## 🏗️ Arquitectura Propuesta

### Estructura Monolítica con Organización por Capas (Layered Architecture)

#### 1. **Presentación** (📁 `/Backend/routes`)
*   APIs REST - Todos los endpoints para comunicación con las entidades
*   Implementación con **FastAPI** o **Flask**
*   Delegación a la lógica de negocio con validaciones mínimas
*   **Estado**: ⏳ Pendiente

#### 2. **Lógica de Negocio** (📁 `/Backend/services`)
*   Trabaja exclusivamente con Python: recibe Python, devuelve Python
*   Creación de instancias de entidades
*   Manejo de excepciones
*   Implementación de transacciones
*   Llamadas a los CRUD para inserción en BD
*   **Estado**: ⏳ Pendiente

#### 3. **Acceso a Datos** (📁 `/Backend/repository`)
*   Implementación del patrón DAO (Data Access Object)
*   CRUD para todas las entidades del dominio
*   **Sin lógica de negocio**, solo operaciones de persistencia
*   **Estado**: 🔄 En desarrollo (ClienteRepository implementado como ejemplo)

#### 4. **Persistencia/Datos** (📁 `/Backend/models` y `/Backend/database`)
*   Modelos de entidades (dataclasses)
*   Configuración y gestión de la base de datos SQLite
*   **Estado**: ✅ Completado (16 entidades implementadas)

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

- **Base de datos**: SQLite3
- **Lenguaje**: Python 3
- **Patrón**: DAO (Data Access Object) + Layered Architecture
- **API** (propuesto): FastAPI o Flask
- **Frontend**: React + TypeScript + Vite

## 📝 Próximos Pasos

1. ⏳ Implementar repositories para todas las entidades
2. ⏳ Crear servicios de lógica de negocio
3. ⏳ Desarrollar API REST con FastAPI/Flask
4. ⏳ Implementar autenticación y autorización
5. ⏳ Conectar con el frontend React

## 👥 Equipo

**Grupo 22 - 4K1 - TP DAO 2025**

---

📖 **Documentación completa**: Ver [`Backend/README.md`](Backend/README.md) y [`Backend/GETTING_STARTED.md`](Backend/GETTING_STARTED.md)
