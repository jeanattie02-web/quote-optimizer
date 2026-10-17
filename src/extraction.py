"""Extraction du texte des demandes de devis au format PDF."""

import pdfplumber


def extraire_texte(chemin: str) -> str:
    """Renvoie tout le texte d'un PDF, page après page."""
    pages = []
    with pdfplumber.open(chemin) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return "/n".join(pages)
