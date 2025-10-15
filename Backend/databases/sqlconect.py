"""Configuración de SQLAlchemy.

Resuelve la ruta de la base de datos SQLite de forma absoluta para evitar
problemas por el directorio de trabajo actual.
"""

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Ruta absoluta a Backend/databases/dbFutbolReserva.db
BASE_DIR = Path(__file__).resolve().parent.parent  # .../Backend
DB_PATH = BASE_DIR / "databases" / "dbFutbolReserva.db"
DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}" 

# Para SQLite en apps con hilos (ej. FastAPI/Flask), conviene check_same_thread=False
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,  # API 2.0 de SQLAlchemy
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()

__all__ = ["engine", "SessionLocal", "Base"]