from pydantic import BaseModel, Field


class QuoteInput(BaseModel):
    jours_junior: int = Field(default=0, ge=0, description="Nombre de jours Junior")
    jours_confirme: int = Field(default=0, ge=0, description="Nombre de jours Confirmé")
    jours_senior: int = Field(default=0, ge=0, description="Nombre de jours Senior")
    frais_deplacement: float = Field(
        default=0.0, ge=0.0, description="Frais annexes en Euros"
    )

    marge_cible: float = Field(
        default=0.25,
        ge=0.0,
        lt=1.0,
        description="Marge cible entre 0.0 (0%) et 0.99 (99%)",
    )
