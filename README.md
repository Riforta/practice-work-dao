# Sistema de Gestión de Canchas Deportivas - DeporteX

## 📋 Descripción del Proyecto

**DeporteX** es un sistema completo de gestión para complejos deportivos que permite administrar canchas, reservas, torneos, equipos y pagos. El proyecto está desarrollado con una arquitectura cliente-servidor moderna y escalable.

## 🏗️ Arquitectura

### Backend
- **Framework**: FastAPI (Python)
- **Base de datos**: SQLite
- **Autenticación**: JWT con pbkdf2_sha256
- **Patrón de diseño**: Arquitectura en capas (Modelos, Repositorios, Servicios, Routers)

### Frontend
- **Framework**: React 18 + TypeScript
- **Build tool**: Vite
- **Estilos**: Tailwind CSS v4
- **Routing**: React Router v6
- **Iconos**: Heroicons

## 🚀 Estado Actual del Proyecto

### ✅ Funcionalidades Implementadas

#### Módulo de Autenticación
- [x] Login con usuario/contraseña
- [x] Registro de nuevos usuarios
- [x] Sistema de roles (Administrador, Cliente, Empleado)
- [x] Protección de rutas por roles
- [x] Interfaz mejorada con diseño moderno y gradientes

#### Módulo de Clientes
- [x] Registro de clientes con validaciones completas
- [x] Modificación de datos (todos los campos obligatorios)
- [x] Consulta y búsqueda de clientes
- [x] Eliminación de clientes
- [x] Botones con colores consistentes (emerald/red)

#### Módulo de Canchas
- [x] Gestión completa de canchas (CRUD)
- [x] Tipos de deporte: Fútbol, Básquet, Pádel
- [x] Precios por hora configurables
- [x] 8 canchas de ejemplo en base de datos

#### Módulo de Turnos/Reservas
- [x] Generación automática de turnos disponibles
- [x] Sistema de reservas con validaciones
- [x] Bloqueo de turnos por administradores
- [x] Filtros avanzados (fecha, horario, cancha, estado)
- [x] Estados: disponible, reservado, bloqueado, completado, cancelado, no_disponible
- [x] ~4,200 turnos generados (últimos 30 días + próximos 7 días)

#### Módulo de Servicios Adicionales
- [x] Gestión de servicios extras (CRUD)
- [x] 12 servicios de ejemplo (pelotas, iluminación, vestuarios, etc.)
- [x] Asignación de servicios a turnos
- [x] Cálculo automático de totales

#### Módulo de Pagos
- [x] Registro de pagos con turno y servicios
- [x] Estados: iniciado, completado, fallido
- [x] Métodos de pago: efectivo, tarjeta, transferencia, mercadopago
- [x] Auto-carga del monto al seleccionar turno
- [x] ~2,000 pagos históricos generados

#### Módulo de Torneos
- [x] Gestión de torneos (CRUD)
- [x] Estados: planificado, inscripciones_abiertas, en_curso, finalizado, cancelado
- [x] Inscripción de equipos
- [x] Bloqueo de turnos para torneos
- [x] 4 torneos de ejemplo (1 en curso, 3 con inscripciones abiertas)

#### Módulo de Equipos
- [x] Creación y gestión de equipos
- [x] Asignación de capitanes y miembros
- [x] 9 equipos de ejemplo con miembros

#### Módulo de Reportes
- [x] **Resumen General del Sistema**
  - Total de canchas, clientes, reservas
  - Ingresos totales y promedio por reserva
  - Clientes activos
  
- [x] **Utilización Mensual de Canchas**
  - Reservas por mes y cancha
  - Ingresos mensuales incluyendo servicios
  - Gráficos por mes

- [x] **Canchas Más Utilizadas**
  - Ranking de canchas por cantidad de reservas
  - Ingresos totales por cancha
  - Precio promedio

- [x] **Reservas por Cliente**
  - Historial completo de reservas
  - Total gastado (turno + servicios)
  - Cantidad de reservas por cliente

- [x] **Reservas por Cancha y Período**
  - Filtrado por fechas
  - Detalle de reservas por cancha
  - Ingresos por período

- [x] **Exportación a PDF**
  - Todos los reportes exportables
  - Conversión de colores oklab/oklch a RGB
  - Soporte multi-página

### 🎨 Mejoras de UI/UX Recientes

#### Componentes de Autenticación
- **Login**: Diseño moderno con gradientes emerald/teal, iconos SVG, botón de mostrar/ocultar contraseña
- **Register**: Layout en 2 columnas, campos con iconos específicos, validaciones visuales con asteriscos rojos

#### Navbar
- Background con gradiente slate
- Logo con efecto glow en hover
- Botones estilizados con ancho uniforme (140px)
- Badge de usuario con ícono
- Botón logout con hover en rojo

### 📊 Datos de Ejemplo

La base de datos incluye datos realistas para pruebas:
- **Usuarios**: 11 usuarios (1 admin, 2 empleados, 8 clientes)
- **Clientes**: 15 clientes registrados
- **Canchas**: 8 canchas (3 Fútbol, 3 Pádel, 2 Básquet)
- **Servicios**: 12 servicios adicionales
- **Turnos**: ~4,200 turnos (históricos y futuros)
- **Reservas**: ~2,000 reservas con pagos
- **Equipos**: 9 equipos formados con miembros
- **Torneos**: 4 torneos activos

**Credenciales de acceso:**
- **Admin**: `admin` / `admin123`
- **Empleados**: `empleado1` o `empleado2` / `emp123`
- **Clientes**: `jperez`, `mrodriguez`, etc. / `cliente123`

## 🔧 Instalación y Configuración

### Requisitos Previos
- Python 3.9+
- Node.js 18+
- npm o yarn

### Backend

```bash
cd Backend

# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Inicializar base de datos
python scripts/init_database.py --reset

# Iniciar servidor
python -m uvicorn api.main:app --reload
```

El backend estará disponible en: `http://localhost:8000`
Documentación API: `http://localhost:8000/docs`

### Frontend

```bash
cd Frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

El frontend estará disponible en: `http://localhost:5173`

## 📁 Estructura del Proyecto

```
TP-DAO---4K1---G22---2025/
├── Backend/
│   ├── api/
│   │   ├── dependencies/    # Autenticación y dependencias
│   │   ├── routers/         # Endpoints por módulo
│   │   └── main.py          # Aplicación FastAPI
│   ├── database/
│   │   └── connection.py    # Conexión SQLite
│   ├── models/              # Modelos de datos
│   ├── repositories/        # Capa de acceso a datos
│   ├── scripts/
│   ├── services/            # Lógica de negocio
│   │   └── init_database.py # Script de inicialización
│   └── requirements.txt
│
└── Frontend/
    ├── src/
    │   ├── components/      # Componentes React por módulo
    │   │   ├── auth/
    │   │   ├── canchas/
    │   │   ├── clientes/
    │   │   ├── navbar/
    │   │   ├── pagos/
    │   │   ├── reportes/
    │   │   ├── torneo/
    │   │   └── turnos/
    │   ├── contexts/        # Context API (Auth, Modal)
    │   ├── services/        # API clients
    │   └── main.tsx
    └── package.json
```

## 🔄 Flujos Principales

### Flujo de Reserva
1. Cliente selecciona fecha, hora y cancha
2. Opcionalmente agrega servicios adicionales
3. Sistema calcula monto total (turno + servicios)
4. Se crea el pago en estado "iniciado"
5. Al confirmar, turno pasa a "reservado" y pago a "completado"

### Flujo de Torneo
1. Admin crea torneo con fechas y reglas
2. Equipos se inscriben mientras inscripciones están abiertas
3. Admin bloquea turnos para el torneo
4. Al iniciar, torneo pasa a "en_curso"
5. Al finalizar, turnos se liberan

## 🐛 Correcciones Recientes

### Estados de Entidades
- ✅ Torneos: corregido de `inscripcion_abierta` a `inscripciones_abiertas`
- ✅ Pagos: corregido de `pendiente` a `iniciado`
- ✅ Reportes: incluyen turnos `completado` además de `reservado`

### Validaciones
- ✅ Clientes: apellido, DNI, teléfono ahora obligatorios
- ✅ Pagos: respetan el estado seleccionado por el usuario
- ✅ Turnos: filtros de fecha con máximo año 9999
- ✅ Torneo: deportes limitados a ['Fútbol', 'Básquet', 'Pádel']

### UI/UX
- ✅ Botones con tamaños consistentes
- ✅ Colores estandarizados (emerald para acciones principales)
- ✅ Iconos en todos los inputs
- ✅ Gradientes y efectos hover

## 📈 Próximas Mejoras Sugeridas

- [ ] Sistema de notificaciones
- [ ] Dashboard con gráficos en tiempo real
- [ ] Exportación a Excel
- [ ] Integración con pasarelas de pago reales
- [ ] Sistema de puntos/fidelización
- [ ] App móvil
- [ ] Calendario visual de reservas
- [ ] Chat de soporte en vivo

## 📝 Notas Técnicas

### Base de Datos
- Se usa SQLite para desarrollo (fácil de migrar a PostgreSQL/MySQL)
- Índices creados para optimizar consultas frecuentes
- Foreign keys habilitadas
- Timestamps en formato ISO 8601

### Seguridad
- Contraseñas hasheadas con pbkdf2_sha256
- Tokens JWT con expiración
- CORS configurado para desarrollo
- Validaciones en frontend y backend

### Performance
- Lazy loading en componentes React
- Consultas optimizadas con índices
- Caché de datos en frontend
- Paginación en listas largas

## 👥 Equipo de Desarrollo

**Grupo 22 - 4K1 - DAO 2025**

## 📄 Licencia

Este proyecto es parte de un trabajo práctico universitario para la materia Desarrollo de Aplicaciones con Objetos.

---

**Última actualización**: Noviembre 2025
