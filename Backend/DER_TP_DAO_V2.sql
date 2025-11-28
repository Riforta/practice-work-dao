CREATE TABLE `Usuario` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `nombre_usuario` varchar(255) UNIQUE NOT NULL,
  `email` varchar(255) UNIQUE NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `id_rol` integer
);

CREATE TABLE `Rol` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `nombre_rol` varchar(255) UNIQUE NOT NULL,
  `descripcion` varchar(255)
);

CREATE TABLE `Cliente` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `apellido` varchar(255),
  `dni` varchar(255) UNIQUE,
  `telefono` varchar(255) NOT NULL,
  `id_usuario` integer UNIQUE
);

CREATE TABLE `Cancha` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `tipo_deporte` varchar(255),
  `descripcion` text,
  `activa` boolean DEFAULT true,
  `precio_hora` float
);

CREATE TABLE `Turno` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `id_cancha` integer NOT NULL,
  `fecha_hora_inicio` datetime NOT NULL,
  `fecha_hora_fin` datetime NOT NULL,
  `estado` varchar(255) NOT NULL DEFAULT 'disponible',
  `precio_final` float NOT NULL,
  `id_cliente` integer,
  `id_usuario_registro` integer,
  `reserva_created_at` timestamp,
  `id_usuario_bloqueo` integer,
  `motivo_bloqueo` varchar(255)
);

CREATE TABLE `ServicioAdicional` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `precio_actual` float NOT NULL,
  `activo` boolean DEFAULT true
);

CREATE TABLE `TurnoXServicio` (
  `id_turno` integer,
  `id_servicio` integer,
  `cantidad` integer NOT NULL DEFAULT 1,
  `precio_unitario_congelado` float NOT NULL,
  PRIMARY KEY (`id_turno`, `id_servicio`)
);

CREATE TABLE `Torneo` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `tipo_deporte` varchar(255) NOT NULL,
  `created_at` timestamp DEFAULT (now()),
  `fecha_inicio` date,
  `fecha_fin` date,
  `costo_inscripcion` float DEFAULT 0,
  `cupos` integer,
  `reglas` text,
  `estado` varchar(255)
);

CREATE TABLE `Equipo` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `nombre_equipo` varchar(255) UNIQUE NOT NULL,
  `id_capitan` integer
);

CREATE TABLE `EquipoMiembro` (
  `id_equipo` integer,
  `id_cliente` integer,
  PRIMARY KEY (`id_equipo`, `id_cliente`)
);

CREATE TABLE `EquipoXTorneo` (
  `id_equipo` integer,
  `id_torneo` integer,
  `fecha_inscripcion` timestamp DEFAULT (now()),
  PRIMARY KEY (`id_equipo`, `id_torneo`)
);

CREATE TABLE `Pago` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `id_turno` integer UNIQUE,
  `monto_turno` float,
  `monto_servicios` float DEFAULT 0,
  `monto_total` float NOT NULL,
  `id_cliente` integer NOT NULL,
  `id_usuario_registro` integer,
  `estado` varchar(255) NOT NULL DEFAULT 'iniciado',
  `metodo_pago` varchar(255),
  `id_gateway_externo` varchar(255),
  `fecha_creacion` timestamp DEFAULT (now()),
  `fecha_expiracion` timestamp,
  `fecha_completado` timestamp
);

CREATE UNIQUE INDEX `Turno_index_0` ON `Turno` (`id_cancha`, `fecha_hora_inicio`);

ALTER TABLE `Usuario` ADD FOREIGN KEY (`id_rol`) REFERENCES `Rol` (`id`);

ALTER TABLE `Cliente` ADD FOREIGN KEY (`id_usuario`) REFERENCES `Usuario` (`id`);

ALTER TABLE `Turno` ADD FOREIGN KEY (`id_cancha`) REFERENCES `Cancha` (`id`);

ALTER TABLE `Turno` ADD FOREIGN KEY (`id_cliente`) REFERENCES `Cliente` (`id`);

ALTER TABLE `Turno` ADD FOREIGN KEY (`id_usuario_registro`) REFERENCES `Usuario` (`id`);

ALTER TABLE `Turno` ADD FOREIGN KEY (`id_usuario_bloqueo`) REFERENCES `Usuario` (`id`);

ALTER TABLE `TurnoXServicio` ADD FOREIGN KEY (`id_turno`) REFERENCES `Turno` (`id`);

ALTER TABLE `TurnoXServicio` ADD FOREIGN KEY (`id_servicio`) REFERENCES `ServicioAdicional` (`id`);

ALTER TABLE `Equipo` ADD FOREIGN KEY (`id_capitan`) REFERENCES `Cliente` (`id`);

ALTER TABLE `EquipoMiembro` ADD FOREIGN KEY (`id_equipo`) REFERENCES `Equipo` (`id`);

ALTER TABLE `EquipoMiembro` ADD FOREIGN KEY (`id_cliente`) REFERENCES `Cliente` (`id`);

ALTER TABLE `EquipoXTorneo` ADD FOREIGN KEY (`id_equipo`) REFERENCES `Equipo` (`id`);

ALTER TABLE `EquipoXTorneo` ADD FOREIGN KEY (`id_torneo`) REFERENCES `Torneo` (`id`);

ALTER TABLE `Pago` ADD FOREIGN KEY (`id_turno`) REFERENCES `Turno` (`id`);

ALTER TABLE `Pago` ADD FOREIGN KEY (`id_cliente`) REFERENCES `Cliente` (`id`);

ALTER TABLE `Pago` ADD FOREIGN KEY (`id_usuario_registro`) REFERENCES `Usuario` (`id`);
