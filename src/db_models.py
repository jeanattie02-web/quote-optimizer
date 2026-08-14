from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Float, Integer

from src.database import Base


def get_utc_now():
    "Retourne la date et l'heure actuelles en UTC."
    return datetime.now(timezone.utc)


class DevisDB(Base):
    __tablename__ = "devis"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date_creation = Column(DateTime, default=get_utc_now)
    jours_junior = Column(Integer, nullable=False)
    jours_confirme = Column(Integer, nullable=False)
    jours_senior = Column(Integer, nullable=False)
    frais_deplacement = Column(Float, nullable=False)
    marge_cible = Column(Float, nullable=False)
    cout_revient_total = Column(Float, nullable=False)
    prix_vente_conseille = Column(Float, nullable=False)
    marge_brute_euros = Column(Float, nullable=False)
