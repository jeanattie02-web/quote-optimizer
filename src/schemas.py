from datetime import datetime
from pydantic import BaseModel, ConfigDict


class QuoteResponse(BaseModel):
    id: int
    date_creation: datetime
    jours_junior: int
    jours_confirme: int
    jours_senior: int
    frais_deplacement: float
    marge_cible: float
    cout_revient_total: float
    prix_vente_conseille: float
    marge_brute_euros: float

    model_config = ConfigDict(from_attributes=True)
