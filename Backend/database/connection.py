import sqlite3
import os
from pathlib import Path

# Ruta del archivo de base de datos
DB_PATH = Path(__file__).parent.parent / "database.db"


def get_connection():
    """
    Obtiene una conexión a la base de datos SQLite.
    Activa las claves foráneas.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row  # Para acceder a las columnas por nombre
    return conn


def init_database():
    """
    Inicializa la base de datos ejecutando el script SQL.
    """
    sql_script_path = Path(__file__).parent.parent / "DER_TP_DAO_V2.sql"
    
    if not sql_script_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo SQL en {sql_script_path}")
    
    conn = get_connection()
    try:
        with open(sql_script_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        conn.executescript(sql_script)
        conn.commit()
        print(f"✓ Base de datos inicializada correctamente en {DB_PATH}")
    except Exception as e:
        print(f"✗ Error al inicializar la base de datos: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    # Eliminar la base de datos existente si existe
    if DB_PATH.exists():
        os.remove(DB_PATH)
        print(f"Base de datos anterior eliminada: {DB_PATH}")
    
    # Crear nueva base de datos
    init_database()
