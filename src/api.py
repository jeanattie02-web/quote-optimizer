from typing import List, Optional
from src.calculator import calculer_devis
from src.crud import obtenir_tous_les_devis, sauvegarder_devis, supprimer_devis
from src.database import get_db, init_db
from src.logger import logger
from src.models import QuoteInput

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from src.schemas import QuoteResponse

# Initialise les tables en base au démarrage de l'API
init_db()

app = FastAPI(
    title="Quote Optimizer API",
    description="API REST de chiffrage et de gestion de devis techniques",
    version="1.0.0",
)


@app.get("/health", tags=["Monitoring"])
def health_check():
    """Point de contrôle de santé du service."""
    return {"status": "ok", "service": "Quote Optimizer API"}


@app.post(
    "/quotes",
    response_model=QuoteResponse,
    status_code=201,
    tags=["Quotes"],
)
def creer_devis(payload: QuoteInput, db: Session = Depends(get_db)):
    """Calcule et sauvegarde un nouveau devis en base de données."""
    try:
        res = calculer_devis(payload)
        devis_db = sauvegarder_devis(db, payload, res)
        return devis_db
    except Exception as e:
        logger.error(f"Erreur API lors de la création du devis : {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get(
    "/quotes",
    response_model=List[QuoteResponse],
    tags=["Quotes"],
)
def lister_devis(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à sauter"),
    limit: int = Query(100, ge=1, le=100, description="Nombre maximal d'éléments"),
    min_prix: Optional[float] = Query(
        None, ge=0, description="Filtrer par prix de vente minimum"
    ),
    db: Session = Depends(get_db),
):
    """Récupère l'historique des devis avec support du filtrage et de la pagination."""
    return obtenir_tous_les_devis(db, skip=skip, limit=limit, min_prix=min_prix)


# Delete
@app.delete(
    "/quotes/{quote_id}",
    status_code=204,
    tags=["Quotes"],
)
# Supression
def effacer_devis(quote_id: int, db: Session = Depends(get_db)):
    """Supprime un devis spécifique de la base de données."""
    succes = supprimer_devis(db, quote_id=quote_id)
    # Error 404: the current devis is not found
    if not succes:
        raise HTTPException(status_code=404, detail=f"Devis #{quote_id} introuvable.")
    return None
