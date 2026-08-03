# src/calculator.py
from src.models import QuoteInput
from src.logger import logger

FRAIS_GENERAUX_PCT = 0.05  # 5% de frais de structure


def calculer_devis(input_data: QuoteInput) -> dict:
    """
    Calcule le coût de revient, le prix de vente conseillé et la marge brute.
    """
    # Grille tarifaire journaliers (Coûts internes)
    COST_JUNIOR = 300.0
    COST_CONFIRME = 500.0
    COST_SENIOR = 800.0

    # 1. Calculs mathématiques
    cout_humain = (
        (input_data.jours_junior * COST_JUNIOR)
        + (input_data.jours_confirme * COST_CONFIRME)
        + (input_data.jours_senior * COST_SENIOR)
    )
    # Ajout frais généraux
    frais_generaux = cout_humain * FRAIS_GENERAUX_PCT
    cout_revient_total = cout_humain + input_data.frais_deplacement + frais_generaux
    prix_vente_conseille = cout_revient_total / (1 - input_data.marge_cible)
    marge_brute_euros = prix_vente_conseille - cout_revient_total

    # 2. On retourne un dictionnaire propre
    resultat = {
        "cout_humain_total": round(cout_humain, 2),
        "frais_generaux": round(frais_generaux, 2),
        "frais_deplacement": round(input_data.frais_deplacement, 2),
        "cout_revient_total": round(cout_revient_total, 2),
        "prix_vente_conseille": round(prix_vente_conseille, 2),
        "marge_brute_euros": round(marge_brute_euros, 2),
    }
    prix = resultat["prix_vente_conseille"]
    marge = resultat["marge_brute_euros"]
    logger.info(f"Calcul terminé | Prix conseillé: {prix} € | Marge: {marge} €")

    return resultat
