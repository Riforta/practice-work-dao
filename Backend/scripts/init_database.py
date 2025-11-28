"""
Script de inicialización de base de datos.

Este script:
1. Crea todas las tablas si no existen
2. Inserta datos básicos (roles, canchas, servicios, etc.)
3. Opcionalmente crea un usuario admin por defecto

Uso:
    python scripts/init_database.py
    python scripts/init_database.py --reset  # Elimina y recrea todo
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime, timedelta
from passlib.hash import pbkdf2_sha256  # ← Cambiado de bcrypt a pbkdf2_sha256

# Agregar el directorio raíz al path
sys.path.append(str(Path(__file__).parent.parent))

from database.connection import get_connection


def crear_tablas():
    """Crea todas las tablas necesarias"""
    conn = get_connection()
    cursor = conn.cursor()
    
    print("Creando tablas...")
    
    try:
        # Tabla Rol
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "Rol" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "nombre_rol" TEXT UNIQUE NOT NULL,
                "descripcion" TEXT
            )
        """)
        
        # Tabla Usuario
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "Usuario" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "nombre_usuario" TEXT NOT NULL UNIQUE,
                "email" TEXT NOT NULL UNIQUE,
                "password_hash" TEXT NOT NULL,
                "id_rol" INTEGER,
                FOREIGN KEY("id_rol") REFERENCES "Rol"("id") ON DELETE SET NULL
            )
        """)
        
        # Tabla Cliente
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "Cliente" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "nombre" TEXT NOT NULL,
                "apellido" TEXT,
                "dni" TEXT UNIQUE,
                "telefono" TEXT NOT NULL,
                "email" TEXT,
                "id_usuario" INTEGER UNIQUE,
                FOREIGN KEY("id_usuario") REFERENCES "Usuario"("id")
            )
        """)
        
        # Tabla Cancha
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "Cancha" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "nombre" TEXT NOT NULL,
                "tipo_deporte" TEXT,
                "descripcion" TEXT,
                "activa" INTEGER DEFAULT 1,
                "precio_hora" NUMERIC
            )
        """)
        
        # Tabla ServicioAdicional
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "ServicioAdicional" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "nombre" TEXT NOT NULL,
                "precio_actual" REAL NOT NULL,
                "activo" INTEGER DEFAULT 1
            )
        """)
        
        # Tabla Turno
        cursor.execute("""
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
            )
        """)
        
        # Tabla TurnoXServicio
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "TurnoXServicio" (
                "id_turno" INTEGER,
                "id_servicio" INTEGER,
                "cantidad" INTEGER NOT NULL DEFAULT 1,
                "precio_unitario_congelado" REAL NOT NULL,
                PRIMARY KEY ("id_turno", "id_servicio"),
                FOREIGN KEY ("id_turno") REFERENCES "Turno"("id") ON DELETE CASCADE,
                FOREIGN KEY ("id_servicio") REFERENCES "ServicioAdicional"("id") ON DELETE CASCADE
            )
        """)
        
        # Tabla Torneo
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "Torneo" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "nombre" TEXT NOT NULL,
                "tipo_deporte" TEXT NOT NULL,
                "created_at" TEXT DEFAULT CURRENT_TIMESTAMP,
                "fecha_inicio" TEXT,
                "fecha_fin" TEXT,
                "costo_inscripcion" REAL DEFAULT 0,
                "cupos" INTEGER,
                "reglas" TEXT,
                "estado" TEXT
            )
        """)
        
        # Tabla Equipo
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "Equipo" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "nombre_equipo" TEXT UNIQUE NOT NULL,
                "id_capitan" INTEGER,
                FOREIGN KEY ("id_capitan") REFERENCES "Cliente"("id") ON DELETE SET NULL
            )
        """)
        
        # Tabla EquipoMiembro
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "EquipoMiembro" (
                "id_equipo" INTEGER,
                "id_cliente" INTEGER,
                PRIMARY KEY ("id_equipo", "id_cliente"),
                FOREIGN KEY ("id_equipo") REFERENCES "Equipo"("id") ON DELETE CASCADE,
                FOREIGN KEY ("id_cliente") REFERENCES "Cliente"("id") ON DELETE CASCADE
            )
        """)
        
        # Tabla EquipoXTorneo (relación N:M entre Equipo y Torneo)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "EquipoXTorneo" (
                "id_equipo" INTEGER,
                "id_torneo" INTEGER,
                "fecha_inscripcion" TEXT DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY ("id_equipo", "id_torneo"),
                FOREIGN KEY ("id_equipo") REFERENCES "Equipo"("id") ON DELETE CASCADE,
                FOREIGN KEY ("id_torneo") REFERENCES "Torneo"("id") ON DELETE CASCADE
            )
        """)
        
        # Tabla Pago
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "Pago" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "id_turno" INTEGER UNIQUE,
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
                FOREIGN KEY ("id_cliente") REFERENCES "Cliente"("id") ON DELETE CASCADE,
                FOREIGN KEY ("id_usuario_registro") REFERENCES "Usuario"("id") ON DELETE SET NULL
            )
        """)
        
        print("✓ Tablas creadas exitosamente")
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        print(f"✗ Error al crear tablas: {e}")
        raise
    finally:
        conn.close()


def crear_indices():
    """Crea los índices necesarios"""
    conn = get_connection()
    cursor = conn.cursor()
    
    print("\nCreando índices...")
    
    try:
        # Índice único en Turno para prevenir doble reserva
        cursor.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_turno_cancha_fecha 
            ON "Turno"("id_cancha", "fecha_hora_inicio")
        """)
        
        # Índice en email de Usuario para búsquedas rápidas
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_usuario_email 
            ON "Usuario"("email")
        """)
        
        # Índice en cancha para filtros
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_turno_cancha 
            ON "Turno"("id_cancha")
        """)
        
        print("✓ Índices creados exitosamente")
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        print(f"✗ Error al crear índices: {e}")
        raise
    finally:
        conn.close()


def insertar_datos_basicos():
    """Inserta datos básicos necesarios para el sistema"""
    conn = get_connection()
    cursor = conn.cursor()
    
    print("\nInsertando datos básicos...")
    
    try:
        # 1. ROLES
        print("  → Insertando roles...")
        roles = [
            (1, 'administrador', 'Administrador del sistema con acceso completo'),
            (2, 'cliente', 'Cliente que puede reservar canchas y participar en torneos'),
            (3, 'empleado', 'Empleado del complejo deportivo')
        ]
        
        for rol in roles:
            cursor.execute("""
                INSERT OR IGNORE INTO Rol (id, nombre_rol, descripcion) 
                VALUES (?, ?, ?)
            """, rol)
        
        print("    ✓ 3 roles insertados")
        
        # 2. USUARIOS
        print("  → Creando usuarios...")
        # ✅ Usar pbkdf2_sha256 igual que en auth_service.py
        password_hash = pbkdf2_sha256.hash("admin123")
        
        usuarios = [
            ('admin', 'admin@canchas.com', password_hash, 1),
            ('empleado1', 'empleado1@canchas.com', pbkdf2_sha256.hash("emp123"), 3),
            ('empleado2', 'empleado2@canchas.com', pbkdf2_sha256.hash("emp123"), 3),
            ('jperez', 'jperez@email.com', pbkdf2_sha256.hash("cliente123"), 2),
            ('mrodriguez', 'mrodriguez@email.com', pbkdf2_sha256.hash("cliente123"), 2),
            ('lgomez', 'lgomez@email.com', pbkdf2_sha256.hash("cliente123"), 2),
            ('asanchez', 'asanchez@email.com', pbkdf2_sha256.hash("cliente123"), 2),
            ('cmartinez', 'cmartinez@email.com', pbkdf2_sha256.hash("cliente123"), 2),
            ('pfernandez', 'pfernandez@email.com', pbkdf2_sha256.hash("cliente123"), 2),
            ('rlopez', 'rlopez@email.com', pbkdf2_sha256.hash("cliente123"), 2),
            ('jgarcia', 'jgarcia@email.com', pbkdf2_sha256.hash("cliente123"), 2),
        ]
        
        for usuario in usuarios:
            cursor.execute("""
                INSERT OR IGNORE INTO Usuario (nombre_usuario, email, password_hash, id_rol)
                VALUES (?, ?, ?, ?)
            """, usuario)
        
        print(f"    ✓ {len(usuarios)} usuarios creados (password para admin: admin123, empleados: emp123, clientes: cliente123)")
        
        # 3. CLIENTES
        print("  → Insertando clientes...")
        cursor.execute("SELECT id FROM Usuario WHERE id_rol = 2")
        usuario_ids = [row[0] for row in cursor.fetchall()]
        
        clientes = [
            ('Juan', 'Pérez', '12345678', '3515551234', 'jperez@email.com', usuario_ids[0] if len(usuario_ids) > 0 else None),
            ('María', 'Rodríguez', '23456789', '3515552345', 'mrodriguez@email.com', usuario_ids[1] if len(usuario_ids) > 1 else None),
            ('Luis', 'Gómez', '34567890', '3515553456', 'lgomez@email.com', usuario_ids[2] if len(usuario_ids) > 2 else None),
            ('Ana', 'Sánchez', '45678901', '3515554567', 'asanchez@email.com', usuario_ids[3] if len(usuario_ids) > 3 else None),
            ('Carlos', 'Martínez', '56789012', '3515555678', 'cmartinez@email.com', usuario_ids[4] if len(usuario_ids) > 4 else None),
            ('Paula', 'Fernández', '67890123', '3515556789', 'pfernandez@email.com', usuario_ids[5] if len(usuario_ids) > 5 else None),
            ('Roberto', 'López', '78901234', '3515557890', 'rlopez@email.com', usuario_ids[6] if len(usuario_ids) > 6 else None),
            ('Julia', 'García', '89012345', '3515558901', 'jgarcia@email.com', usuario_ids[7] if len(usuario_ids) > 7 else None),
            # Clientes sin usuario asociado
            ('Diego', 'Torres', '90123456', '3515559012', 'dtorres@email.com', None),
            ('Sofía', 'Ruiz', '01234567', '3515550123', 'sruiz@email.com', None),
            ('Martín', 'Silva', '11223344', '3515551122', 'msilva@email.com', None),
            ('Laura', 'Díaz', '22334455', '3515552233', 'ldiaz@email.com', None),
            ('Gabriel', 'Castro', '33445566', '3515553344', 'gcastro@email.com', None),
            ('Valentina', 'Morales', '44556677', '3515554455', 'vmorales@email.com', None),
            ('Facundo', 'Romero', '55667788', '3515555566', 'fromero@email.com', None),
        ]
        
        for cliente in clientes:
            cursor.execute("""
                INSERT OR IGNORE INTO Cliente (nombre, apellido, dni, telefono, email, id_usuario)
                VALUES (?, ?, ?, ?, ?, ?)
            """, cliente)
        
        print(f"    ✓ {len(clientes)} clientes insertados")
        
        # 4. CANCHAS
        print("  → Insertando canchas...")
        canchas = [
            ('Cancha Fútbol 5 - Principal', 'Fútbol', 'Cancha de césped sintético con iluminación', 1, 8000.0),
            ('Cancha Fútbol 7 - Grande', 'Fútbol', 'Cancha amplia con tribunas', 1, 12000.0),
            ('Cancha Fútbol 11 - Estadio', 'Fútbol', 'Cancha reglamentaria con césped natural', 1, 20000.0),
            ('Cancha Padel 1', 'Pádel', 'Cancha de polvo de ladrillo', 1, 5000.0),
            ('Cancha Padel 2', 'Pádel', 'Cancha con paredes de vidrio', 1, 6000.0),
            ('Cancha Padel 3 - VIP', 'Pádel', 'Cancha premium con vestuarios', 1, 7500.0),
            ('Cancha Básquet - Techada', 'Básquet', 'Cancha techada con piso sintético', 1, 10000.0),
            ('Cancha Básquet - Exterior', 'Básquet', 'Cancha al aire libre', 1, 7000.0),
        ]
        
        for cancha in canchas:
            cursor.execute("""
                INSERT OR IGNORE INTO Cancha (nombre, tipo_deporte, descripcion, activa, precio_hora)
                VALUES (?, ?, ?, ?, ?)
            """, cancha)
        
        print(f"    ✓ {len(canchas)} canchas insertadas")
        
        # 5. SERVICIOS ADICIONALES
        print("  → Insertando servicios adicionales...")
        servicios = [
            ('Pelota de fútbol profesional', 800.0, 1),
            ('Pelota de básquet', 700.0, 1),
            ('Pelota de paddle', 600.0, 1),
            ('Iluminación nocturna', 1500.0, 1),
            ('Vestuario VIP', 1000.0, 1),
            ('Arbitraje profesional', 3000.0, 1),
            ('Set de pecheras (10 unidades)', 800.0, 1),
            ('Raquetas de paddle (2 unidades)', 1200.0, 1),
            ('Bebidas y snacks', 2000.0, 1),
            ('Conos de entrenamiento', 500.0, 1),
            ('Toallas', 300.0, 1),
            ('Botiquín de primeros auxilios', 1500.0, 1),
        ]
        
        for servicio in servicios:
            cursor.execute("""
                INSERT OR IGNORE INTO ServicioAdicional (nombre, precio_actual, activo)
                VALUES (?, ?, ?)
            """, servicio)
        
        print(f"    ✓ {len(servicios)} servicios adicionales insertados")
        
        # 6. TURNOS Y RESERVAS (últimos 30 días + próximos 7 días)
        print("  → Generando turnos y reservas...")
        
        # Obtener IDs necesarios
        cursor.execute("SELECT id FROM Cancha")
        cancha_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id FROM Cliente")
        cliente_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id FROM Usuario WHERE id_rol = 1 OR id_rol = 3")
        empleado_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id, precio_actual FROM ServicioAdicional WHERE activo = 1")
        servicios_disponibles = cursor.fetchall()
        
        import random
        
        turnos_creados = 0
        reservas_creadas = 0
        
        # Generar turnos históricos (últimos 30 días) con reservas
        for dia_offset in range(-30, 0):
            fecha = datetime.now() + timedelta(days=dia_offset)
            
            # Solo horarios laborales para datos históricos
            for cancha_id in cancha_ids:
                cursor.execute("SELECT precio_hora FROM Cancha WHERE id = ?", (cancha_id,))
                precio_base = cursor.fetchone()[0]
                
                for hora in range(8, 22):
                    inicio = fecha.replace(hour=hora, minute=0, second=0, microsecond=0)
                    fin = inicio + timedelta(hours=1)
                    
                    # 70% de probabilidad de estar reservado (histórico)
                    if random.random() < 0.7:
                        cliente_id = random.choice(cliente_ids)
                        empleado_id = random.choice(empleado_ids)
                        estado = 'completado' if random.random() < 0.95 else 'cancelado'
                        
                        cursor.execute("""
                            INSERT OR IGNORE INTO Turno 
                            (id_cancha, fecha_hora_inicio, fecha_hora_fin, estado, precio_final, 
                             id_cliente, id_usuario_registro, reserva_created_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (cancha_id, inicio.isoformat(), fin.isoformat(), estado, precio_base,
                              cliente_id, empleado_id, inicio.isoformat()))
                        
                        turno_id = cursor.lastrowid
                        
                        # Agregar servicios adicionales aleatorios (40% de probabilidad)
                        if turno_id and random.random() < 0.4:
                            num_servicios = random.randint(1, 3)
                            servicios_elegidos = random.sample(servicios_disponibles, min(num_servicios, len(servicios_disponibles)))
                            
                            for servicio_id, precio_servicio in servicios_elegidos:
                                cantidad = random.randint(1, 2)
                                cursor.execute("""
                                    INSERT OR IGNORE INTO TurnoXServicio 
                                    (id_turno, id_servicio, cantidad, precio_unitario_congelado)
                                    VALUES (?, ?, ?, ?)
                                """, (turno_id, servicio_id, cantidad, precio_servicio))
                        
                        # Crear pago correspondiente si está completado
                        if turno_id and estado == 'completado':
                            # Calcular monto de servicios
                            cursor.execute("""
                                SELECT COALESCE(SUM(cantidad * precio_unitario_congelado), 0)
                                FROM TurnoXServicio
                                WHERE id_turno = ?
                            """, (turno_id,))
                            monto_servicios = cursor.fetchone()[0]
                            
                            monto_total = precio_base + monto_servicios
                            metodo = random.choice(['efectivo', 'tarjeta', 'transferencia', 'mercadopago'])
                            
                            cursor.execute("""
                                INSERT OR IGNORE INTO Pago
                                (id_turno, monto_turno, monto_servicios, monto_total, id_cliente,
                                 id_usuario_registro, estado, metodo_pago, fecha_creacion, fecha_completado)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (turno_id, precio_base, monto_servicios, monto_total, cliente_id,
                                  empleado_id, 'completado', metodo, inicio.isoformat(), fin.isoformat()))
                        
                        reservas_creadas += 1
                    else:
                        # Turno disponible o bloqueado (5% bloqueados)
                        if random.random() < 0.05:
                            empleado_id = random.choice(empleado_ids)
                            motivo = random.choice(['Mantenimiento programado', 'Evento privado', 'Reparaciones'])
                            cursor.execute("""
                                INSERT OR IGNORE INTO Turno 
                                (id_cancha, fecha_hora_inicio, fecha_hora_fin, estado, precio_final,
                                 id_usuario_bloqueo, motivo_bloqueo)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                            """, (cancha_id, inicio.isoformat(), fin.isoformat(), 'bloqueado', precio_base,
                                  empleado_id, motivo))
                        else:
                            cursor.execute("""
                                INSERT OR IGNORE INTO Turno 
                                (id_cancha, fecha_hora_inicio, fecha_hora_fin, estado, precio_final)
                                VALUES (?, ?, ?, ?, ?)
                            """, (cancha_id, inicio.isoformat(), fin.isoformat(), 'disponible', precio_base))
                    
                    turnos_creados += 1
        
        # Generar turnos futuros (próximos 7 días)
        for dia_offset in range(0, 7):
            fecha = datetime.now() + timedelta(days=dia_offset)
            
            for cancha_id in cancha_ids:
                cursor.execute("SELECT precio_hora FROM Cancha WHERE id = ?", (cancha_id,))
                precio_base = cursor.fetchone()[0]
                
                for hora in range(8, 22):
                    inicio = fecha.replace(hour=hora, minute=0, second=0, microsecond=0)
                    fin = inicio + timedelta(hours=1)
                    
                    # 30% reservado en el futuro
                    if random.random() < 0.3:
                        cliente_id = random.choice(cliente_ids)
                        empleado_id = random.choice(empleado_ids)
                        
                        cursor.execute("""
                            INSERT OR IGNORE INTO Turno 
                            (id_cancha, fecha_hora_inicio, fecha_hora_fin, estado, precio_final,
                             id_cliente, id_usuario_registro, reserva_created_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (cancha_id, inicio.isoformat(), fin.isoformat(), 'reservado', precio_base,
                              cliente_id, empleado_id, datetime.now().isoformat()))
                        
                        turno_id = cursor.lastrowid
                        
                        # Servicios para reservas futuras (30% probabilidad)
                        if turno_id and random.random() < 0.3:
                            num_servicios = random.randint(1, 2)
                            servicios_elegidos = random.sample(servicios_disponibles, min(num_servicios, len(servicios_disponibles)))
                            
                            for servicio_id, precio_servicio in servicios_elegidos:
                                cursor.execute("""
                                    INSERT OR IGNORE INTO TurnoXServicio 
                                    (id_turno, id_servicio, cantidad, precio_unitario_congelado)
                                    VALUES (?, ?, ?, ?)
                                """, (turno_id, servicio_id, 1, precio_servicio))
                        
                        # Crear pago iniciado para reservas futuras
                        if turno_id:
                            cursor.execute("""
                                SELECT COALESCE(SUM(cantidad * precio_unitario_congelado), 0)
                                FROM TurnoXServicio
                                WHERE id_turno = ?
                            """, (turno_id,))
                            monto_servicios = cursor.fetchone()[0]
                            
                            monto_total = precio_base + monto_servicios
                            fecha_exp = (inicio + timedelta(hours=-2)).isoformat()  # Expira 2 horas antes
                            
                            cursor.execute("""
                                INSERT OR IGNORE INTO Pago
                                (id_turno, monto_turno, monto_servicios, monto_total, id_cliente,
                                 id_usuario_registro, estado, fecha_creacion, fecha_expiracion)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (turno_id, precio_base, monto_servicios, monto_total, cliente_id,
                                  empleado_id, 'iniciado', datetime.now().isoformat(), fecha_exp))
                        
                        reservas_creadas += 1
                    else:
                        cursor.execute("""
                            INSERT OR IGNORE INTO Turno 
                            (id_cancha, fecha_hora_inicio, fecha_hora_fin, estado, precio_final)
                            VALUES (?, ?, ?, ?, ?)
                        """, (cancha_id, inicio.isoformat(), fin.isoformat(), 'disponible', precio_base))
                    
                    turnos_creados += 1
        
        print(f"    ✓ {turnos_creados} turnos generados")
        print(f"    ✓ {reservas_creadas} reservas creadas con pagos")
        
        # 7. EQUIPOS Y TORNEOS
        print("  → Creando equipos y torneos...")
        
        # Crear equipos
        equipos = [
            ('Los Tigres FC', 1),  # Capitán: Juan Pérez
            ('Águilas United', 3),  # Capitán: Luis Gómez
            ('Leones de Oro', 5),  # Capitán: Carlos Martínez
            ('Halcones Rojos', 7),  # Capitán: Roberto López
            ('Cóndores FC', 9),  # Capitán: Diego Torres
            ('Pumas Basket', 2),  # Capitán: María Rodríguez (básquet)
            ('Dragones Basket', 4),  # Capitán: Ana Sánchez
            ('Raquetas Pro', 6),  # Capitán: Paula Fernández (paddle)
            ('Paddle Masters', 8),  # Capitán: Julia García
        ]
        
        for nombre_equipo, id_capitan in equipos:
            cursor.execute("""
                INSERT OR IGNORE INTO Equipo (nombre_equipo, id_capitan)
                VALUES (?, ?)
            """, (nombre_equipo, id_capitan))
        
        # Asignar miembros a equipos
        cursor.execute("SELECT id FROM Equipo")
        equipo_ids = [row[0] for row in cursor.fetchall()]
        
        # Distribuir clientes en equipos (3-5 miembros por equipo)
        cliente_idx = 0
        for equipo_id in equipo_ids[:5]:  # Solo equipos de fútbol
            num_miembros = random.randint(3, 5)
            for _ in range(num_miembros):
                if cliente_idx < len(cliente_ids):
                    cursor.execute("""
                        INSERT OR IGNORE INTO EquipoMiembro (id_equipo, id_cliente)
                        VALUES (?, ?)
                    """, (equipo_id, cliente_ids[cliente_idx]))
                    cliente_idx += 1
        
        print(f"    ✓ {len(equipos)} equipos creados con miembros")
        
        # Crear torneos
        fecha_inicio_1 = (datetime.now() - timedelta(days=15)).date().isoformat()
        fecha_fin_1 = (datetime.now() + timedelta(days=15)).date().isoformat()
        
        fecha_inicio_2 = (datetime.now() + timedelta(days=7)).date().isoformat()
        fecha_fin_2 = (datetime.now() + timedelta(days=21)).date().isoformat()
        
        fecha_inicio_3 = (datetime.now() + timedelta(days=30)).date().isoformat()
        fecha_fin_3 = (datetime.now() + timedelta(days=44)).date().isoformat()
        
        torneos = [
            ('Torneo Apertura 2025 - Fútbol 5', 'Fútbol', fecha_inicio_1, fecha_fin_1, 
             5000.0, 8, 'Torneo eliminación directa. Máximo 8 jugadores por equipo.', 'en_curso'),
            ('Copa Primavera - Básquet', 'Básquet', fecha_inicio_2, fecha_fin_2,
             8000.0, 6, 'Torneo round-robin. Equipos de 5 jugadores.', 'inscripciones_abiertas'),
            ('Torneo Verano - Paddle', 'Pádel', fecha_inicio_3, fecha_fin_3,
             3000.0, 12, 'Torneo parejas. Eliminación doble.', 'inscripciones_abiertas'),
            ('Liga Local - Fútbol 7', 'Fútbol', fecha_inicio_2, fecha_fin_2,
             7000.0, 10, 'Liga con partidos todos contra todos.', 'inscripciones_abiertas'),
        ]
        
        for torneo in torneos:
            cursor.execute("""
                INSERT OR IGNORE INTO Torneo 
                (nombre, tipo_deporte, fecha_inicio, fecha_fin, costo_inscripcion, 
                 cupos, reglas, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, torneo)
        
        # Inscribir equipos en torneos
        cursor.execute("SELECT id FROM Torneo")
        torneo_ids = [row[0] for row in cursor.fetchall()]
        
        # Torneo 1 (Fútbol): equipos 1-4 inscritos
        for i in range(4):
            cursor.execute("""
                INSERT OR IGNORE INTO EquipoXTorneo (id_equipo, id_torneo, fecha_inscripcion)
                VALUES (?, ?, ?)
            """, (equipo_ids[i], torneo_ids[0], (datetime.now() - timedelta(days=20)).isoformat()))
        
        # Torneo 2 (Básquet): equipos 6-7 inscritos
        for i in range(2):
            cursor.execute("""
                INSERT OR IGNORE INTO EquipoXTorneo (id_equipo, id_torneo, fecha_inscripcion)
                VALUES (?, ?, ?)
            """, (equipo_ids[5+i], torneo_ids[1], datetime.now().isoformat()))
        
        # Torneo 3 (Paddle): equipos 8-9 inscritos
        for i in range(2):
            cursor.execute("""
                INSERT OR IGNORE INTO EquipoXTorneo (id_equipo, id_torneo, fecha_inscripcion)
                VALUES (?, ?, ?)
            """, (equipo_ids[7+i], torneo_ids[2], datetime.now().isoformat()))
        
        print(f"    ✓ {len(torneos)} torneos creados con inscripciones")
        
        conn.commit()
        print("\n✓ Datos básicos insertados exitosamente")
        
    except Exception as e:
        conn.rollback()
        print(f"\n✗ Error al insertar datos: {e}")
        raise
    finally:
        conn.close()


def mostrar_resumen():
    """Muestra un resumen de los datos insertados"""
    conn = get_connection()
    cursor = conn.cursor()
    
    print("\n" + "="*60)
    print("RESUMEN DE LA BASE DE DATOS")
    print("="*60)
    
    try:
        # Contar registros en cada tabla
        tablas = [
            'Rol', 'Usuario', 'Cliente', 'Cancha', 'ServicioAdicional', 
            'Turno', 'Torneo', 'Equipo', 'EquipoMiembro', 'EquipoXTorneo', 'Pago'
        ]
        
        for tabla in tablas:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cursor.fetchone()[0]
            print(f"  {tabla:20} {count:>4} registros")
        
        print("\n" + "="*60)
        print("CREDENCIALES DE ACCESO")
        print("="*60)
        print("\n  ADMINISTRADOR:")
        print("    Usuario:   admin")
        print("    Password:  admin123")
        print("    Email:     admin@canchas.com")
        
        print("\n  EMPLEADOS:")
        print("    Usuario:   empleado1 / empleado2")
        print("    Password:  emp123")
        
        print("\n  CLIENTES (con usuario):")
        print("    Usuario:   jperez, mrodriguez, lgomez, etc.")
        print("    Password:  cliente123")
        
        print("\n" + "="*60)
        print("DATOS DE PRUEBA GENERADOS")
        print("="*60)
        print("  • 15 clientes registrados")
        print("  • 8 canchas (Fútbol, Básquet, Pádel)")
        print("  • 12 servicios adicionales")
        print("  • ~4,200 turnos (últimos 30 días + próximos 7 días)")
        print("  • ~2,000 reservas con pagos")
        print("  • 9 equipos formados")
        print("  • 4 torneos activos")
        
        print("\n" + "="*60)
        print("PRÓXIMOS PASOS")
        print("="*60)
        print("  1. Iniciar la API:")
        print("     python -m uvicorn api.main:app --reload")
        print("")
        print("  2. Login como admin:")
        print("     POST /api/auth/login")
        print("     {\"nombre_usuario\": \"admin\", \"password\": \"admin123\"}")
        print("")
        print("  3. Probar reportes con datos históricos reales")
        print("  4. Validar reservas, pagos y torneos")
        print("="*60 + "\n")
        
    finally:
        conn.close()


def resetear_base_datos():
    """Elimina todas las tablas y las recrea"""
    conn = get_connection()
    cursor = conn.cursor()
    
    print("\n⚠️  RESETEANDO BASE DE DATOS...")
    print("Se eliminarán TODOS los datos existentes.\n")
    
    try:
        # Desactivar foreign keys temporalmente para poder eliminar tablas
        cursor.execute("PRAGMA foreign_keys = OFF")
        
        # Obtener todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence'")
        tablas = [row[0] for row in cursor.fetchall()]
        
        # Eliminar todas las tablas
        for tabla in tablas:
            cursor.execute(f"DROP TABLE IF EXISTS {tabla}")
            print(f"  ✓ Tabla {tabla} eliminada")
        
        # Eliminar índices
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indices = [row[0] for row in cursor.fetchall()]
        
        for indice in indices:
            if not indice.startswith('sqlite_'):
                cursor.execute(f"DROP INDEX IF EXISTS {indice}")
        
        conn.commit()
        
        # Reactivar foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")
        
        print("\n✓ Base de datos reseteada\n")
        
    except Exception as e:
        conn.rollback()
        print(f"\n✗ Error al resetear base de datos: {e}")
        raise
    finally:
        conn.close()


def main():
    """Función principal"""
    import sys
    
    print("\n" + "="*60)
    print("SCRIPT DE INICIALIZACIÓN DE BASE DE DATOS")
    print("="*60 + "\n")
    
    # Verificar si se pide reset
    if len(sys.argv) > 1 and sys.argv[1] == '--reset':
        respuesta = input("⚠️  ¿Estás seguro de ELIMINAR todos los datos? (escribe 'SI'): ")
        if respuesta.strip().upper() == 'SI':
            resetear_base_datos()
        else:
            print("Reset cancelado")
            return
    
    # Crear estructura
    crear_tablas()
    crear_indices()
    
    # Insertar datos
    insertar_datos_basicos()
    
    # Mostrar resumen
    mostrar_resumen()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n✗ Error fatal: {e}")
        sys.exit(1)
