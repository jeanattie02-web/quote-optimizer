from typing import List, Optional

from sqlalchemy.orm import Session

from src.db_models import DevisDB
from src.logger import logger
from src.models import QuoteInput


def sauvegarder_devis(
    db: Session, quote_input: QuoteInput, res: dict
) -> DevisDB:  # (CREATE)
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


def obtenir_tous_les_devis(  # (READ)
    db: Session,
    skip: int = 0,
    limit: int = 100,
    min_prix: Optional[float] = None,
) -> List[DevisDB]:
    """Récupère les devis enregistrés avec options de pagination et filtre."""
    query = db.query(DevisDB)
    # SELECT * FROM devis
    if min_prix is not None:
        query = query.filter(DevisDB.prix_vente_conseille >= min_prix)
        # SELECT * FROM devis WHERE "prix_vente_conseille">="min_prix"
    return query.order_by(DevisDB.date_creation.desc()).offset(skip).limit(limit).all()
    # SELECT query ORDER BY "date_creation" DESC Limit 100


def supprimer_devis(db: Session, quote_id: int) -> bool:  # (DELETE)
    """Supprime un devis par son identifiant unique."""
    devis = db.query(DevisDB).filter(DevisDB.id == quote_id).first()
    # SELECT * FROM devis WHERE id = quote_id LIMIT 1;.
    if not devis:
        return False
    db.delete(devis)
    db.commit()
    logger.info(f"Devis #{quote_id} supprimé avec succès.")
    return True
