"""Extraction des demandes de devis : texte des PDF, schéma des champs et modèle."""

import os
from typing import Optional

import httpx
import pdfplumber
from pydantic import BaseModel, Field

import re

# --- Réglages du modèle de langage (modifiables par variables d'environnement) ---
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
MODELE = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

CONSIGNES = (
    "Tu lis des demandes de devis et tu en extrais quatre informations. "
    "Réponds uniquement en JSON, selon le schéma fourni. "
    "Si une information n'apparaît pas explicitement dans le document, "
    "réponds null : n'invente jamais de valeur. "
    "Les jours sont des nombres de jours de travail, pas des jours de la semaine. "
    "Les frais de déplacement ne sont pas le budget global. "
)


# --- Schéma des champs à extraire ---
class DemandeDevis(BaseModel):
    """Champs extraits d'une demande de devis."""

    jours_junior: Optional[int] = Field(
        default=None,
        ge=0,
        description="Nombre de jours de travail d'un développeur junior",
    )
    jours_confirme: Optional[int] = Field(
        default=None,
        ge=0,
        description="Nombre de jours de travail d'un consultant confirmé",
    )
    jours_senior: Optional[int] = Field(
        default=None, ge=0, description="Nombre de jours de travail d'un expert senior"
    )
    frais_deplacement: Optional[float] = Field(
        default=None,
        ge=0,
        description="Budget de déplacement en euros, hors budget global",
    )


# --- Du PDF au texte ---
def extraire_texte(chemin: str) -> str:
    """Renvoie tout le texte d'un PDF, page après page."""
    pages = []
    with pdfplumber.open(chemin) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return "\n".join(pages)


# --- Du texte aux champs vérifiés ---
def extraire_champs(texte: str) -> DemandeDevis:
    """Demande au modèle les champs d'une demande de devis, puis les vérifie."""
    requete = {
        "model": MODELE,
        "stream": False,
        "format": DemandeDevis.model_json_schema(),
        "options": {"temperature": 0},
        "messages": [
            {"role": "system", "content": CONSIGNES},
            {"role": "user", "content": texte},
        ],
    }
    reponse = httpx.post(OLLAMA_URL, json=requete, timeout=120)
    reponse.raise_for_status()
    contenu = reponse.json()["message"]["content"]
    return DemandeDevis.model_validate_json(contenu)


PROFILS = {
    "junior": "jours_junior",
    "confirm": "jours_confirme",
    "senior": "jours_senior",
}

MOTIF_JOURS = re.compile(r"(\d+)\s*jours?")


# --- Lecture manuelle du tableau ---
def lire_jours_tableaux(chemin: str) -> dict:
    """Lit les jours par profil dans les tableaux du PDF"""
    jours = {}
    with pdfplumber.open(chemin) as pdf:
        for page in pdf.pages:
            for tableau in page.extract_tables():
                for ligne in tableau:
                    texte_ligne = " ".join(cellule or "" for cellule in ligne).lower()
                    nombre = MOTIF_JOURS.search(texte_ligne)
                    if nombre is None:
                        continue
                    for mot, champ in PROFILS.items():
                        if mot in texte_ligne:
                            jours[champ] = int(nombre.group(1))
    return jours


# ---fusion des deux sources---
def analyser_demande(chemin: str) -> DemandeDevis:
    """Analyse une demande PDF : tableaux lus sans IA, texte libre confié au modèle."""
    demande = extraire_champs(extraire_texte(chemin))
    jours_tableaux = lire_jours_tableaux(chemin)
    return demande.model_copy(update=jours_tableaux)
