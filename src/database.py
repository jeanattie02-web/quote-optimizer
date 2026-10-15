"""Connexion à la base SQLite et création des tables."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Chemin de la base, modifiable par la variable d'environnement DATABASE_PATH
DB_PATH = os.getenv("DATABASE_PATH", "./data/quote_optimizer.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Générateur de session de base de données."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Crée toutes les tables définies dans les modèles ORM."""
    import src.db_models  # noqa: F401
    Base.metadata.create_all(bind=engine)
