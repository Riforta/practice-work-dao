# Comparación DER vs Base de Datos SQLite - Actualizada

## Estado Actual: ✅ ALINEADO CON DER_TP_DAO_V2.sql

### Tablas Implementadas

| Tabla | DER MySQL | BD SQLite | Estado |
|-------|-----------|-----------|--------|
| Usuario | ✅ | ✅ | ✅ Alineado |
| Rol | ✅ | ✅ | ✅ Alineado |
| Cliente | ✅ | ✅ | ✅ Alineado + email |
| Cancha | ✅ | ✅ | ✅ Alineado |
| Turno | ✅ | ✅ | ✅ Alineado |
| ServicioAdicional | ✅ | ✅ | ✅ Alineado |
| TurnoXServicio | ✅ | ✅ | ✅ Alineado |
| Torneo | ✅ | ✅ | ✅ Alineado |
| Equipo | ✅ | ✅ | ✅ Alineado |
| EquipoMiembro | ✅ | ✅ | ✅ Alineado |
| Inscripcion | ✅ | ✅ | ✅ Alineado |
| Partido | ✅ | ✅ | ✅ Alineado |
| **Pago** | ✅ | ✅ | ✅ **ACTUALIZADO** |
| ~~Pedido~~ | ❌ | ❌ | ✅ **ELIMINADO** |
| ~~PedidoItem~~ | ❌ | ❌ | ✅ **ELIMINADO** |

---

## Tabla Pago - Comparación Detallada

### DER_TP_DAO_V2.sql (MySQL)
```sql
CREATE TABLE `Pago` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `id_turno` integer UNIQUE,
  `id_inscripcion` integer UNIQUE,
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
```

### Base de Datos SQLite (Actual)
```sql
CREATE TABLE "Pago" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "id_turno" INTEGER UNIQUE,
  "id_inscripcion" INTEGER UNIQUE,
  "monto_turno" REAL,
  "monto_servicios" REAL DEFAULT 0,
  "monto_total" REAL NOT NULL,
  "id_cliente" INTEGER NOT NULL,
  "id_usuario_registro" INTEGER,
  "estado" TEXT NOT NULL DEFAULT 'iniciado',
  "metodo_pago" TEXT,
  "id_gateway_externo" TEXT,
  "fecha_creacion" TEXT DEFAULT CURRENT_TIMESTAMP,
  "fecha_expiracion" TEXT,
  "fecha_completado" TEXT,
  FOREIGN KEY ("id_turno") REFERENCES "Turno"("id") ON DELETE CASCADE,
  FOREIGN KEY ("id_inscripcion") REFERENCES "Inscripcion"("id") ON DELETE CASCADE,
  FOREIGN KEY ("id_cliente") REFERENCES "Cliente"("id") ON DELETE CASCADE,
  FOREIGN KEY ("id_usuario_registro") REFERENCES "Usuario"("id") ON DELETE SET NULL
);
```

### Diferencias (Todas Justificadas)
| Aspecto | DER MySQL | SQLite | Justificación |
|---------|-----------|--------|---------------|
| Tipos de datos | `float`, `varchar`, `timestamp` | `REAL`, `TEXT` | Tipos nativos SQLite |
| DEFAULT now() | `DEFAULT (now())` | `DEFAULT CURRENT_TIMESTAMP` | Sintaxis SQLite |
| Foreign Keys | Sin ON DELETE | Con ON DELETE policies | Mejor integridad referencial |

---

## Índices

### DER_TP_DAO_V2.sql
```sql
CREATE UNIQUE INDEX `Turno_index_0` ON `Turno` (`id_cancha`, `fecha_hora_inicio`);
CREATE UNIQUE INDEX `Inscripcion_index_1` ON `Inscripcion` (`id_equipo`, `id_torneo`);
```

### Base de Datos SQLite (Actual)
```sql
-- Índice único para prevenir doble reserva
CREATE UNIQUE INDEX idx_turno_cancha_fecha ON "Turno"("id_cancha", "fecha_hora_inicio");

-- Índice único implementado como constraint en tabla
UNIQUE ("id_equipo", "id_torneo")  -- En CREATE TABLE Inscripcion
```

**Estado**: ✅ Ambos índices implementados

---

## Mejoras Adicionales (No en DER)

### 1. Campo `email` en Cliente
```sql
-- SQLite tiene:
"email" TEXT

-- DER no lo tiene
```
**Justificación**: Útil para notificaciones sin necesidad de vincular Usuario.

### 2. Políticas ON DELETE Explícitas
```sql
-- Ejemplo: Pago
FOREIGN KEY ("id_turno") REFERENCES "Turno"("id") ON DELETE CASCADE
```
**Justificación**: Integridad referencial automática.

### 3. Índices Adicionales
```sql
CREATE INDEX idx_turno_cancha ON "Turno"("id_cancha");
CREATE INDEX idx_usuario_email ON "Usuario"("email");
```
**Justificación**: Optimización de queries frecuentes.

---

## Resumen de Migración Realizada

### ❌ Eliminado (Tabla antigua con Pedido/PedidoItem)
```
Pago (vieja)         Pedido             PedidoItem
  id                   id                 id
  id_pedido     →→     monto_total        id_pedido
  monto                estado             id_turno
  estado                                  id_inscripcion
  fecha_pago                              descripcion
                                          monto
```

### ✅ Nuevo (Tabla directa sin intermediarios)
```
Pago (nueva)
  id
  id_turno ──────────→ Turno
  id_inscripcion ───→ Inscripcion
  monto_turno
  monto_servicios
  monto_total
  id_cliente ────────→ Cliente
  id_usuario_registro → Usuario
  estado
  metodo_pago
  fecha_creacion
  fecha_expiracion
  fecha_completado
```

---

## Diferencias entre DER y BD Actual (Resumen)

| Categoría | Diferencia | Estado |
|-----------|------------|--------|
| **Estructura Pago** | ✅ Idéntica al DER v2 | ✅ CORRECTO |
| **Tablas Pedido/PedidoItem** | ❌ Eliminadas (no están en DER v2) | ✅ CORRECTO |
| **Índices** | ✅ Ambos implementados | ✅ CORRECTO |
| **Tipos de datos** | Adaptados a SQLite (TEXT, REAL vs varchar, float) | ✅ CORRECTO |
| **Campo email en Cliente** | 📝 Adicional (no en DER) | ✅ MEJORA |
| **ON DELETE policies** | 📝 Explícitas (no en DER) | ✅ MEJORA |

---

## Conclusión

✅ **La base de datos SQLite está COMPLETAMENTE ALINEADA con DER_TP_DAO_V2.sql**

Las únicas diferencias son:
1. Adaptaciones de sintaxis MySQL → SQLite (tipos, DEFAULT)
2. Mejoras adicionales (email, ON DELETE, índices extra)

No hay inconsistencias estructurales. El modelo implementa correctamente:
- ✅ Flujo de pago directo (sin carrito)
- ✅ Vinculación Pago → Turno/Inscripción
- ✅ Timer de 15 minutos con fecha_expiracion
- ✅ Estados de pago (iniciado, completado, fallido)
- ✅ Índices únicos para prevenir duplicados

---

**Fecha de verificación**: 2025-11-27  
**Versión DER**: V2  
**Estado**: ✅ PRODUCCIÓN READY
