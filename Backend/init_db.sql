-- Script SQLite para inicializar la base de datos del club
-- Basado en DER_TP_DAO_V2.sql adaptado para SQLite

-- Tabla Usuario
CREATE TABLE IF NOT EXISTS Usuario (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre_usuario VARCHAR(255) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  id_rol INTEGER,
  activo BOOLEAN DEFAULT 1
);

-- Tabla Rol
CREATE TABLE IF NOT EXISTS Rol (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre_rol VARCHAR(255) UNIQUE NOT NULL,
  descripcion VARCHAR(255)
);

-- Tabla Cliente
CREATE TABLE IF NOT EXISTS Cliente (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre VARCHAR(255) NOT NULL,
  apellido VARCHAR(255),
  dni VARCHAR(255) UNIQUE,
  telefono VARCHAR(255) NOT NULL,
  email VARCHAR(255),
  id_usuario INTEGER UNIQUE,
  FOREIGN KEY (id_usuario) REFERENCES Usuario(id) ON DELETE SET NULL
);

-- Tabla Cancha
CREATE TABLE IF NOT EXISTS Cancha (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre VARCHAR(255) NOT NULL,
  tipo_deporte VARCHAR(255),
  descripcion TEXT,
  activa BOOLEAN DEFAULT 1
);

-- Tabla Turno
CREATE TABLE IF NOT EXISTS Turno (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_cancha INTEGER NOT NULL,
  fecha_hora_inicio DATETIME NOT NULL,
  fecha_hora_fin DATETIME NOT NULL,
  estado VARCHAR(255) NOT NULL DEFAULT 'disponible',
  precio_final REAL NOT NULL,
  id_cliente INTEGER,
  id_usuario_registro INTEGER,
  reserva_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  id_usuario_bloqueo INTEGER,
  motivo_bloqueo VARCHAR(255),
  FOREIGN KEY (id_cancha) REFERENCES Cancha(id) ON DELETE CASCADE,
  FOREIGN KEY (id_cliente) REFERENCES Cliente(id) ON DELETE SET NULL,
  FOREIGN KEY (id_usuario_registro) REFERENCES Usuario(id) ON DELETE SET NULL,
  FOREIGN KEY (id_usuario_bloqueo) REFERENCES Usuario(id) ON DELETE SET NULL
);

-- Tabla Tarifa
CREATE TABLE IF NOT EXISTS Tarifa (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_cancha INTEGER NOT NULL,
  descripcion VARCHAR(255),
  precio_hora REAL NOT NULL,
  FOREIGN KEY (id_cancha) REFERENCES Cancha(id) ON DELETE CASCADE
);

-- Tabla ServicioAdicional
CREATE TABLE IF NOT EXISTS ServicioAdicional (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre VARCHAR(255) NOT NULL,
  precio_actual REAL NOT NULL,
  activo BOOLEAN DEFAULT 1
);

-- Tabla TurnoXServicio (relación muchos a muchos)
CREATE TABLE IF NOT EXISTS TurnoXServicio (
  id_turno INTEGER,
  id_servicio INTEGER,
  cantidad INTEGER NOT NULL DEFAULT 1,
  precio_unitario_congelado REAL NOT NULL,
  PRIMARY KEY (id_turno, id_servicio),
  FOREIGN KEY (id_turno) REFERENCES Turno(id) ON DELETE CASCADE,
  FOREIGN KEY (id_servicio) REFERENCES ServicioAdicional(id) ON DELETE CASCADE
);

-- Tabla Torneo
CREATE TABLE IF NOT EXISTS Torneo (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre VARCHAR(255) NOT NULL,
  tipo_deporte VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  fecha_inicio DATE,
  fecha_fin DATE,
  costo_inscripcion REAL DEFAULT 0,
  cupos INTEGER,
  reglas TEXT,
  estado VARCHAR(255)
);

-- Tabla Equipo
CREATE TABLE IF NOT EXISTS Equipo (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre_equipo VARCHAR(255) UNIQUE NOT NULL,
  id_capitan INTEGER,
  FOREIGN KEY (id_capitan) REFERENCES Cliente(id) ON DELETE SET NULL
);

-- Tabla EquipoMiembro (relación muchos a muchos)
CREATE TABLE IF NOT EXISTS EquipoMiembro (
  id_equipo INTEGER,
  id_cliente INTEGER,
  PRIMARY KEY (id_equipo, id_cliente),
  FOREIGN KEY (id_equipo) REFERENCES Equipo(id) ON DELETE CASCADE,
  FOREIGN KEY (id_cliente) REFERENCES Cliente(id) ON DELETE CASCADE
);

-- Tabla Inscripcion
CREATE TABLE IF NOT EXISTS Inscripcion (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_equipo INTEGER NOT NULL,
  id_torneo INTEGER NOT NULL,
  fecha_inscripcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  estado VARCHAR(255) NOT NULL DEFAULT 'pendiente_pago',
  FOREIGN KEY (id_equipo) REFERENCES Equipo(id) ON DELETE CASCADE,
  FOREIGN KEY (id_torneo) REFERENCES Torneo(id) ON DELETE CASCADE
);

-- Datos de prueba

-- Insertar roles
INSERT OR IGNORE INTO Rol (id, nombre_rol, descripcion) VALUES 
(1, 'admin', 'Administrador del sistema'),
(2, 'empleado', 'Empleado del club'),
(3, 'cliente', 'Cliente del club');

-- Insertar usuarios de prueba
INSERT OR IGNORE INTO Usuario (id, nombre_usuario, email, password_hash, id_rol, activo) VALUES
(1, 'admin', 'admin@club.com', 'hash_admin', 1, 1),
(2, 'empleado1', 'empleado@club.com', 'hash_empleado', 2, 1);

-- Insertar servicios adicionales
INSERT OR IGNORE INTO ServicioAdicional (id, nombre, precio_actual, activo) VALUES
(1, 'Luz', 500.0, 1),
(2, 'Pelota', 200.0, 1),
(3, 'Vestuario', 300.0, 1);

-- Insertar canchas de prueba
INSERT OR IGNORE INTO Cancha (id, nombre, tipo_deporte, descripcion, activa) VALUES
(1, 'Cancha Fútbol 1', 'futbol', 'Cancha de fútbol 5', 1),
(2, 'Cancha Fútbol 2', 'futbol', 'Cancha de fútbol 7', 1),
(3, 'Cancha Básquet 1', 'basquet', 'Cancha de básquet techada', 1),
(4, 'Cancha Pádel 1', 'padel', 'Cancha de pádel con iluminación', 1);

-- Insertar tarifas de prueba
INSERT OR IGNORE INTO Tarifa (id, id_cancha, descripcion, precio_hora) VALUES
(1, 1, 'Tarifa estándar Fútbol 5', 1500.0),
(2, 2, 'Tarifa estándar Fútbol 7', 2000.0),
(3, 3, 'Tarifa estándar Básquet', 1800.0),
(4, 4, 'Tarifa estándar Pádel', 2500.0);
