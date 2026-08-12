from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer

from src.database import Base


class DevisDB(Base):
    __tablename__ = "devis"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date_creation = Column(DateTime, default=datetime.utcnow)
    jours_junior = Column(Integer, nullable=False)
    jours_confirme = Column(Integer, nullable=False)
    jours_senior = Column(Integer, nullable=False)
    frais_deplacement = Column(Float, nullable=False)
    marge_cible = Column(Float, nullable=False)
    cout_revient_total = Column(Float, nullable=False)
    prix_vente_conseille = Column(Float, nullable=False)
    marge_brute_euros = Column(Float, nullable=False)
