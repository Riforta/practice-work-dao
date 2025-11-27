# Migración al Nuevo Modelo de Pago - Resumen

## Cambios Realizados

### 1. **Modelo de Datos Actualizado**

#### Tabla Pago (NUEVA ESTRUCTURA)
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
)
```

**Cambios clave:**
- ❌ Eliminado `id_pedido` (intermediario)
- ✅ Agregado `id_turno` y `id_inscripcion` (vinculación directa)
- ✅ Agregado `monto_turno`, `monto_servicios` (desglose)
- ✅ Agregado `id_cliente` (dueño del pago)
- ✅ Agregado `fecha_creacion`, `fecha_expiracion`, `fecha_completado` (control temporal)

#### Tablas Eliminadas
- ❌ **Pedido** - Ya no se usa carrito
- ❌ **PedidoItem** - Ya no hay items de pedido

### 2. **Índice Único en Turno**
```sql
CREATE UNIQUE INDEX idx_turno_cancha_fecha 
ON "Turno"("id_cancha", "fecha_hora_inicio")
```
Previene doble reserva de la misma cancha en el mismo horario.

---

## Nuevo Flujo de Negocio

### A. Reserva de Turno

```
1. Cliente selecciona turno + servicios opcionales
   ↓
2. POST /api/pagos/turno
   - Crea Pago con estado='iniciado'
   - Cambia Turno.estado a 'pendiente_pago'
   - Guarda servicios en TurnoXServicio
   - Fecha_expiracion = now() + 15 min
   ↓
3a. Pago confirmado (dentro de 15 min)
    POST /api/pagos/{id}/confirmar
    - Pago.estado = 'completado'
    - Turno.estado = 'reservado'
    
3b. Timer expira (después de 15 min)
    Job automático: procesar_pagos_expirados()
    - Pago.estado = 'fallido'
    - Turno.estado = 'disponible'
```

### B. Inscripción a Torneo

```
1. Equipo se inscribe a torneo
   ↓
2. POST /api/pagos/inscripcion
   - Crea Pago con estado='iniciado'
   - Inscripcion.estado = 'pendiente_pago'
   - Fecha_expiracion = now() + 15 min
   ↓
3a. Pago confirmado
    - Pago.estado = 'completado'
    - Inscripcion.estado = 'confirmada'
    
3b. Timer expira
    - Pago.estado = 'fallido'
    - Inscripcion.estado = 'cancelada'
```

---

## Endpoints API Actualizados

### Crear Pago para Turno
```http
POST /api/pagos/turno
Authorization: Bearer {token}

{
  "id_turno": 123,
  "id_cliente": 1,
  "monto_turno": 5000.0,
  "monto_servicios": 1500.0,
  "servicios": [
    {
      "id_servicio": 1,
      "cantidad": 2,
      "precio_unitario": 750.0
    }
  ],
  "metodo_pago": "tarjeta"
}
```

### Crear Pago para Inscripción
```http
POST /api/pagos/inscripcion
Authorization: Bearer {token}

{
  "id_inscripcion": 456,
  "id_cliente": 1,
  "monto_total": 3000.0,
  "metodo_pago": "efectivo"
}
```

### Confirmar Pago
```http
POST /api/pagos/{pago_id}/confirmar
Authorization: Bearer {token}

{
  "metodo_pago": "tarjeta",
  "id_gateway_externo": "TXN123456"
}
```

### Marcar Pago como Fallido
```http
POST /api/pagos/{pago_id}/marcar-fallido
Authorization: Bearer {token}
```

### Procesar Pagos Expirados (Job automático)
```http
POST /api/pagos/procesar-expirados
Authorization: Bearer {token_admin}
```

### Consultar Pagos
```http
GET /api/pagos/{pago_id}
GET /api/pagos/cliente/{id_cliente}
GET /api/pagos/turno/{id_turno}
GET /api/pagos/inscripcion/{id_inscripcion}
```

---

## Archivos Modificados

### Actualizados
- ✅ `models/pago.py` - Nueva estructura
- ✅ `repositories/pago_repository.py` - Queries actualizadas
- ✅ `services/pagos_service.py` - Lógica de negocio reescrita
- ✅ `api/routers/pagos.py` - Endpoints rediseñados

### Eliminados
- ❌ `models/pedido.py`
- ❌ `models/pedido_item.py`
- ❌ `repositories/pedido_repository.py`
- ❌ `repositories/pedido_item_repository.py`
- ❌ `services/pedidos_service.py`
- ❌ `api/routers/pedidos.py`

### Nuevos
- ✅ `scripts/migrate_to_new_pago.py` - Script de migración

---

## Cómo Usar el Script de Migración

### Verificar estado actual
```bash
python scripts/migrate_to_new_pago.py --check
```

### Ejecutar migración
```bash
python scripts/migrate_to_new_pago.py --execute
```

⚠️ **ADVERTENCIA**: La migración elimina las tablas Pedido, PedidoItem y Pago antiguas.

---

## Estados del Pago

| Estado | Descripción |
|--------|-------------|
| `iniciado` | Pago creado, esperando confirmación (15 min) |
| `completado` | Pago confirmado exitosamente |
| `fallido` | Pago no completado en tiempo o error |

---

## Estados del Turno

| Estado | Descripción |
|--------|-------------|
| `disponible` | Turno libre para reservar |
| `pendiente_pago` | Reservado temporalmente (15 min) |
| `reservado` | Pago confirmado, reserva firme |
| `bloqueado` | Bloqueado por administrador |

---

## Comparación: DER vs Base de Datos Actual

### ✅ Alineado con DER v2
- Pago vinculado directamente a Turno/Inscripción
- Índice único en Turno(id_cancha, fecha_hora_inicio)
- Campo `email` en Cliente (adicional al DER)
- Tipos de datos adaptados a SQLite

### ⚠️ Diferencias con DER original
- DER tenía estructura con Pedido/PedidoItem → **ELIMINADO**
- DER usaba tipos MySQL (varchar, float) → Adaptado a SQLite (TEXT, REAL)
- Agregado `ON DELETE` policies para mejor integridad referencial

---

## Job Automático Recomendado

Para manejar expiración de pagos, agregar un cron job o tarea programada:

```python
# Ejecutar cada 1 minuto
from services.pagos_service import procesar_pagos_expirados

cantidad = procesar_pagos_expirados()
print(f"{cantidad} pagos expirados procesados")
```

O implementar un endpoint protegido que se llame desde un scheduler externo.

---

## Testing

Después de la migración, ejecutar:

```bash
# Verificar que la API inicia correctamente
python -m uvicorn api.main:app --reload

# Ejecutar tests (si existen)
pytest tests/
```

---

## Rollback (Si es necesario)

Si necesitas volver atrás:

1. Restaurar backup de `database.db`
2. Revertir cambios en Git:
   ```bash
   git checkout HEAD^ -- Backend/models/pago.py
   git checkout HEAD^ -- Backend/repositories/pago_repository.py
   git checkout HEAD^ -- Backend/services/pagos_service.py
   git checkout HEAD^ -- Backend/api/routers/pagos.py
   ```
3. Restaurar archivos eliminados de Pedido/PedidoItem desde Git

---

**Fecha de migración**: 2025-11-27  
**Versión DER**: V2 (MySQL export, adaptado a SQLite)
