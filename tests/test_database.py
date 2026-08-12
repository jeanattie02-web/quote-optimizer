import os

from src.database import Base, init_db
from src.db_models import DevisDB


def test_init_db_et_creation_table():
    # Initialise les tables
    init_db()

    # Vérifie que la table 'devis' existe bien dans les métadonnées SQLAlchemy
    assert "devis" in Base.metadata.tables

    # Vérifie que la structure des colonnes de DevisDB est conforme
    columns = DevisDB.__table__.columns.keys()
    assert "id" in columns
    assert "cout_revient_total" in columns
    assert "prix_vente_conseille" in columns
    assert "marge_brute_euros" in columns


def test_base_de_donnees_fichier_cree():
    init_db()
    # Vérifie que le fichier SQLite est bien généré sur le disque
    assert os.path.exists("quote_optimizer.db")
