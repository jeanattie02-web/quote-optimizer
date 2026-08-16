from typing import List
from src.calculator import calculer_devis
from src.crud import obtenir_tous_les_devis, sauvegarder_devis
from src.database import get_db
from src.logger import logger
from src.models import QuoteInput

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from src.schemas import QuoteResponse

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
def lister_devis(db: Session = Depends(get_db)):
    """Récupère l'historique complet des devis enregistrés."""
    return obtenir_tous_les_devis(db)
