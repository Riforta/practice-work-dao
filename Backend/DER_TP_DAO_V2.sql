-- DER_TP_DAO_V2.sql
-- Versión corregida para SQLite: todas las foreign keys se declaran
-- dentro de las sentencias CREATE TABLE (SQLite no soporta ALTER ... ADD FOREIGN KEY).

PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

-- Seguridad
CREATE TABLE IF NOT EXISTS "Rol" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "nombre_rol" TEXT UNIQUE NOT NULL,
  "descripcion" TEXT
);

CREATE TABLE IF NOT EXISTS "Usuario" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "nombre_usuario" TEXT UNIQUE NOT NULL,
  "email" TEXT UNIQUE NOT NULL,
  "password_hash" TEXT NOT NULL,
  "id_rol" INTEGER,
  "activo" INTEGER DEFAULT 1,
  FOREIGN KEY ("id_rol") REFERENCES "Rol"("id") ON DELETE SET NULL
);

-- Datos del Cliente y Cancha
CREATE TABLE `Cliente` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `nombre` TEXT NOT NULL,
  `apellido` TEXT,
  `dni` TEXT UNIQUE, -- Validacion avanzada
  `telefono` TEXT NOT NULL,
  `email` TEXT
);

CREATE TABLE `Cancha` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `nombre` TEXT NOT NULL,
  `tipo_deporte` TEXT,
  `descripcion` TEXT,
  `activa` INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS "Tarifa" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "id_cancha" INTEGER NOT NULL,
  "descripcion" TEXT,
  "precio_hora" REAL NOT NULL,
  FOREIGN KEY ("id_cancha") REFERENCES "Cancha"("id") ON DELETE CASCADE
);

-- Transacción Principal (Turno/Reserva)
CREATE TABLE IF NOT EXISTS "Turno" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "id_cancha" INTEGER NOT NULL,
  "fecha_hora_inicio" TEXT NOT NULL,
  "fecha_hora_fin" TEXT NOT NULL,
  "estado" TEXT NOT NULL DEFAULT 'disponible',
  "precio_final" REAL NOT NULL,
  "id_cliente" INTEGER,
  "id_usuario_registro" INTEGER,
  "reserva_created_at" TEXT DEFAULT CURRENT_TIMESTAMP,
  "id_usuario_bloqueo" INTEGER,
  "motivo_bloqueo" TEXT,
  FOREIGN KEY ("id_cancha") REFERENCES "Cancha"("id") ON DELETE CASCADE,
  FOREIGN KEY ("id_cliente") REFERENCES "Cliente"("id") ON DELETE SET NULL,
  FOREIGN KEY ("id_usuario_registro") REFERENCES "Usuario"("id") ON DELETE SET NULL,
  FOREIGN KEY ("id_usuario_bloqueo") REFERENCES "Usuario"("id") ON DELETE SET NULL
);

-- Módulos de Pago y Servicios
CREATE TABLE `ServicioAdicional` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `nombre` TEXT NOT NULL,
  `precio_actual` REAL NOT NULL,
  `activo` INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS "TurnoXServicio" (
  "id_turno" INTEGER,
  "id_servicio" INTEGER,
  "cantidad" INTEGER NOT NULL DEFAULT 1,
  "precio_unitario_congelado" REAL NOT NULL,
  PRIMARY KEY ("id_turno", "id_servicio"),
  FOREIGN KEY ("id_turno") REFERENCES "Turno"("id") ON DELETE CASCADE,
  FOREIGN KEY ("id_servicio") REFERENCES "ServicioAdicional"("id") ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "Pedido" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "id_cliente" INTEGER NOT NULL,
  "monto_total" REAL NOT NULL,
  "estado" TEXT NOT NULL DEFAULT 'pendiente_pago',
  "fecha_creacion" TEXT DEFAULT CURRENT_TIMESTAMP,
  "fecha_expiracion" TEXT,
  FOREIGN KEY ("id_cliente") REFERENCES "Cliente"("id") ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "PedidoItem" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "id_pedido" INTEGER NOT NULL,
  "id_turno" INTEGER UNIQUE,
  "id_inscripcion" INTEGER UNIQUE,
  "descripcion" TEXT NOT NULL,
  "monto" REAL NOT NULL,
  FOREIGN KEY ("id_pedido") REFERENCES "Pedido"("id") ON DELETE CASCADE,
  FOREIGN KEY ("id_turno") REFERENCES "Turno"("id") ON DELETE SET NULL,
  FOREIGN KEY ("id_inscripcion") REFERENCES "Inscripcion"("id") ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS "Pago" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "id_pedido" INTEGER NOT NULL,
  "monto" REAL NOT NULL,
  "estado" TEXT NOT NULL DEFAULT 'iniciado',
  "metodo_pago" TEXT,
  "id_gateway_externo" TEXT,
  "fecha_pago" TEXT DEFAULT CURRENT_TIMESTAMP,
  "id_usuario_manual" INTEGER NOT NULL,
  FOREIGN KEY ("id_pedido") REFERENCES "Pedido"("id") ON DELETE CASCADE,
  FOREIGN KEY ("id_usuario_manual") REFERENCES "Usuario"("id") ON DELETE SET NULL
);

-- Módulo de Torneos
CREATE TABLE `Torneo` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `nombre` TEXT NOT NULL,
  `tipo_deporte` TEXT NOT NULL,
  `created_at` TEXT DEFAULT CURRENT_TIMESTAMP,
  `fecha_inicio` TEXT,
  `fecha_fin` TEXT,
  `costo_inscripcion` REAL DEFAULT 0,
  `cupos` INTEGER,
  `reglas` TEXT,
  `estado` TEXT
);

CREATE TABLE IF NOT EXISTS "Equipo" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "nombre_equipo" TEXT UNIQUE NOT NULL,
  "id_capitan" INTEGER,
  FOREIGN KEY ("id_capitan") REFERENCES "Cliente"("id") ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS "EquipoMiembro" (
  "id_equipo" INTEGER,
  "id_cliente" INTEGER,
  PRIMARY KEY ("id_equipo", "id_cliente"),
  FOREIGN KEY ("id_equipo") REFERENCES "Equipo"("id") ON DELETE CASCADE,
  FOREIGN KEY ("id_cliente") REFERENCES "Cliente"("id") ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "Inscripcion" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "id_equipo" INTEGER NOT NULL,
  "id_torneo" INTEGER NOT NULL,
  "fecha_inscripcion" TEXT DEFAULT CURRENT_TIMESTAMP,
  "estado" TEXT NOT NULL DEFAULT 'pendiente_pago',
  UNIQUE ("id_equipo", "id_torneo"),
  FOREIGN KEY ("id_equipo") REFERENCES "Equipo"("id") ON DELETE CASCADE,
  FOREIGN KEY ("id_torneo") REFERENCES "Torneo"("id") ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "Partido" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "id_torneo" INTEGER NOT NULL,
  "id_turno" INTEGER UNIQUE,
  "id_equipo_local" INTEGER,
  "id_equipo_visitante" INTEGER,
  "id_equipo_ganador" INTEGER,
  "ronda" TEXT,
  "marcador_local" INTEGER,
  "marcador_visitante" INTEGER,
  "estado" TEXT,
  FOREIGN KEY ("id_torneo") REFERENCES "Torneo"("id") ON DELETE CASCADE,
  FOREIGN KEY ("id_turno") REFERENCES "Turno"("id") ON DELETE SET NULL,
  FOREIGN KEY ("id_equipo_local") REFERENCES "Equipo"("id") ON DELETE SET NULL,
  FOREIGN KEY ("id_equipo_visitante") REFERENCES "Equipo"("id") ON DELETE SET NULL,
  FOREIGN KEY ("id_equipo_ganador") REFERENCES "Equipo"("id") ON DELETE SET NULL
);


-- Índices y notas
COMMIT;

CREATE INDEX IF NOT EXISTS idx_cliente_dni ON "Cliente"(dni);
CREATE INDEX IF NOT EXISTS idx_usuario_email ON "Usuario"(email);
CREATE INDEX IF NOT EXISTS idx_turno_cancha ON "Turno"("id_cancha");
CREATE INDEX IF NOT EXISTS idx_tarifa_cancha ON "Tarifa"("id_cancha");

-- Fin del DER corregido para SQLite