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
        
        # Tabla Inscripcion
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "Inscripcion" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "id_equipo" INTEGER NOT NULL,
                "id_torneo" INTEGER NOT NULL,
                "fecha_inscripcion" TEXT DEFAULT CURRENT_TIMESTAMP,
                "estado" TEXT NOT NULL DEFAULT 'pendiente_pago',
                UNIQUE ("id_equipo", "id_torneo"),
                FOREIGN KEY ("id_equipo") REFERENCES "Equipo"("id") ON DELETE CASCADE,
                FOREIGN KEY ("id_torneo") REFERENCES "Torneo"("id") ON DELETE CASCADE
            )
        """)
        
        # Tabla Partido
        cursor.execute("""
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
            )
        """)
        
        # Tabla Pago
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "Pago" (
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
        
        # 2. USUARIO ADMIN POR DEFECTO
        print("  → Creando usuario administrador...")
        # ✅ Usar pbkdf2_sha256 igual que en auth_service.py
        password_hash = pbkdf2_sha256.hash("admin123")
        
        cursor.execute("""
            INSERT OR IGNORE INTO Usuario (nombre_usuario, email, password_hash, id_rol)
            VALUES (?, ?, ?, ?)
        """, ('admin', 'admin@canchas.com', password_hash, 1))
        
        print("    ✓ Usuario admin creado (usuario: admin, password: admin123)")
        
        # 3. CANCHAS
        print("  → Insertando canchas...")
        canchas = [
            ('Cancha Fútbol 5 - Principal', 'Futbol', 'Cancha de césped sintético con iluminación', 1, 8000.0),
            ('Cancha Fútbol 7 - Grande', 'Futbol', 'Cancha amplia con tribunas', 1, 12000.0),
            ('Cancha Padel 1', 'Padel', 'Cancha de polvo de ladrillo', 1, 5000.0),
            ('Cancha Padel 2', 'Padel', 'Cancha con paredes de vidrio', 1, 6000.0),
            ('Cancha Básquet', 'Básquet', 'Cancha techada con piso sintético', 1, 10000.0)
        ]
        
        for cancha in canchas:
            cursor.execute("""
                INSERT OR IGNORE INTO Cancha (nombre, tipo_deporte, descripcion, activa, precio_hora)
                VALUES (?, ?, ?, ?, ?)
            """, cancha)
        
        print(f"    ✓ {len(canchas)} canchas insertadas")
        
        # 4. SERVICIOS ADICIONALES
        print("  → Insertando servicios adicionales...")
        servicios = [
            ('Pelota de fútbol', 500.0, 1),
            ('Iluminación nocturna', 1500.0, 1),
            ('Vestuario VIP', 1000.0, 1),
            ('Arbitraje profesional', 3000.0, 1),
            ('Set de pecheras', 800.0, 1),
            ('Raquetas de paddle', 1200.0, 1),
            ('Bebidas y snacks', 2000.0, 1)
        ]
        
        for servicio in servicios:
            cursor.execute("""
                INSERT OR IGNORE INTO ServicioAdicional (nombre, precio_actual, activo)
                VALUES (?, ?, ?)
            """, servicio)
        
        print(f"    ✓ {len(servicios)} servicios adicionales insertados")
        
        # 5. TURNOS DE EJEMPLO (próximos 3 días)
        print("  → Generando turnos disponibles...")
        
        # Obtener IDs de canchas
        cursor.execute("SELECT id FROM Cancha")
        cancha_ids = [row[0] for row in cursor.fetchall()]
        
        turnos_creados = 0
        for dia in range(3):  # Próximos 3 días
            fecha = datetime.now() + timedelta(days=dia)
            
            for cancha_id in cancha_ids:
                # Obtener precio de la cancha
                cursor.execute("SELECT precio_hora FROM Cancha WHERE id = ?", (cancha_id,))
                precio = cursor.fetchone()[0]
                
                # Generar turnos de 08:00 a 22:00 (cada 1 hora)
                for hora in range(8, 22):
                    inicio = fecha.replace(hour=hora, minute=0, second=0, microsecond=0)
                    fin = inicio + timedelta(hours=1)
                    
                    cursor.execute("""
                        INSERT OR IGNORE INTO Turno 
                        (id_cancha, fecha_hora_inicio, fecha_hora_fin, estado, precio_final)
                        VALUES (?, ?, ?, ?, ?)
                    """, (cancha_id, inicio.isoformat(), fin.isoformat(), 'disponible', precio))
                    
                    turnos_creados += 1
        
        print(f"    ✓ {turnos_creados} turnos generados")
        
        # 6. TORNEO DE EJEMPLO
        print("  → Creando torneo de ejemplo...")
        fecha_inicio = (datetime.now() + timedelta(days=7)).date().isoformat()
        fecha_fin = (datetime.now() + timedelta(days=14)).date().isoformat()
        
        cursor.execute("""
            INSERT OR IGNORE INTO Torneo 
            (nombre, tipo_deporte, fecha_inicio, fecha_fin, costo_inscripcion, cupos, reglas, estado)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            'Torneo Apertura 2025',
            'Fútbol 5',
            fecha_inicio,
            fecha_fin,
            5000.0,
            16,
            'Torneo eliminación directa. Máximo 8 jugadores por equipo.',
            'inscripcion_abierta'
        ))
        
        print("    ✓ 1 torneo de ejemplo creado")
        
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
            'Turno', 'Torneo', 'Equipo', 'Inscripcion', 'Partido', 'Pago'
        ]
        
        for tabla in tablas:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cursor.fetchone()[0]
            print(f"  {tabla:20} {count:>4} registros")
        
        print("\n" + "="*60)
        print("CREDENCIALES DE ADMINISTRADOR")
        print("="*60)
        print("  Usuario:   admin")
        print("  Password:  admin123")
        print("  Email:     admin@canchas.com")
        
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
        print("  3. Crear clientes y probar reservas")
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
