from typing import List

from sqlalchemy.orm import Session

from src.db_models import DevisDB
from src.logger import logger
from src.models import QuoteInput


def sauvegarder_devis(db: Session, quote_input: QuoteInput, res: dict) -> DevisDB:
    """Enregistre un nouveau devis en base de données."""
    logger.info("Enregistrement du devis en base de données...")
    db_devis = DevisDB(
        jours_junior=quote_input.jours_junior,
        jours_confirme=quote_input.jours_confirme,
        jours_senior=quote_input.jours_senior,
        frais_deplacement=quote_input.frais_deplacement,
        marge_cible=quote_input.marge_cible,
        cout_revient_total=res["cout_revient_total"],
        prix_vente_conseille=res["prix_vente_conseille"],
        marge_brute_euros=res["marge_brute_euros"],
    )
    db.add(db_devis)
    db.commit()
    db.refresh(db_devis)
    logger.info(f"Devis #{db_devis.id} enregistré avec succès.")
    return db_devis


def obtenir_tous_les_devis(db: Session) -> List[DevisDB]:
    """Récupère l'ensemble des devis enregistrés par ordre décroissant."""
    return db.query(DevisDB).order_by(DevisDB.id.desc()).all()
