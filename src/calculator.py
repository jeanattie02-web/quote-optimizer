# src/calculator.py

def calculer_devis(
    jours_junior: int,
    jours_confirme: int,
    jours_senior: int,
    frais_deplacement: float = 0.0,
    marge_cible: float = 0.25

) -> dict:
    """
    Calcule le coût de revient, le prix de vente conseillé et la marge brute.
    """
    # Grille tarifaire (Coûts internes)
    COST_JUNIOR = 300.0
    COST_CONFIRME = 500.0
    COST_SENIOR = 800.0

    # 1. Calculs mathématiques
    cout_humain = (
        (jours_junior * COST_JUNIOR)
        + (jours_confirme * COST_CONFIRME)
        + (jours_senior * COST_SENIOR)
    )
    frais_annexes = frais_deplacement + (0.05 * cout_humain)
    cout_revient_total = cout_humain + frais_annexes

    # Sécurité 
    if marge_cible >= 1.0:
        raise ValueError("La marge cible doit être strictement inférieure à 100% (1.0).")

    prix_vente_conseille = cout_revient_total / (1 - marge_cible)
    marge_brute_euros = prix_vente_conseille - cout_revient_total

    # 2. On retourne un dictionnaire propre
    return {
        "cout_humain": cout_humain,
        "frais_annexes": frais_annexes,
        "cout_revient_total": cout_revient_total,
        "prix_vente_conseille": prix_vente_conseille,
        "marge_brute_euros": marge_brute_euros
    }