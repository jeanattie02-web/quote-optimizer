"""Extraction des demandes de devis : texte des PDF et schéma des champs."""

from typing import Optional

import pdfplumber
from pydantic import BaseModel, Field


class DemandeDevis(BaseModel):
    """Champs extraits d'une demande de devis."""

    jours_junior: Optional[int] = Field(None, ge=0)
    jours_confirme: Optional[int] = Field(None, ge=0)
    jours_senior: Optional[int] = Field(None, ge=0)
    frais_deplacement: Optional[float] = Field(None, ge=0)


def extraire_texte(chemin: str) -> str:
    """Renvoie tout le texte d'un PDF, page après page."""
    pages = []
    with pdfplumber.open(chemin) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return "\n".join(pages)