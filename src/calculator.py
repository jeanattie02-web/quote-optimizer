# src/calculator.py

FRAIS_GENERAUX_PCT = 0.05  # 5% de frais de structure

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
    # Grille tarifaire journaliers (Coûts internes)
    COST_JUNIOR = 300.0
    COST_CONFIRME = 500.0
    COST_SENIOR = 800.0

    # 1. Calculs mathématiques
    cout_humain = (
        (jours_junior * COST_JUNIOR)
        + (jours_confirme * COST_CONFIRME)
        + (jours_senior * COST_SENIOR)
    )
    #Ajout frais généraux
    frais_generaux = cout_humain * FRAIS_GENERAUX_PCT
    cout_revient_total = cout_humain + frais_deplacement+ frais_generaux     
    
    # Sécurité 
    # Vérification des valeurs négatives
    if jours_junior < 0 or jours_confirme < 0 or jours_senior < 0:
        raise ValueError("Le nombre de jours ne peut pas être négatif.")
        
    if frais_deplacement < 0:
        raise ValueError("Les frais de déplacement ne peuvent pas être négatifs.")
    if marge_cible >= 1.0 or marge_cible<0:
        raise ValueError("La marge cible doit être strictement inférieure à 100% (1.0) et supérieure ou égaole à 0")

    prix_vente_conseille = cout_revient_total / (1 - marge_cible)
    marge_brute_euros = prix_vente_conseille - cout_revient_total

    # 2. On retourne un dictionnaire propre
    return {
        "cout_humain_total": cout_humain,
        "frais_generaux":frais_generaux,
        "frais_deplacement":frais_deplacement,
        "cout_revient_total": cout_revient_total,
        "prix_vente_conseille": prix_vente_conseille,
        "marge_brute_euros": marge_brute_euros
    }

