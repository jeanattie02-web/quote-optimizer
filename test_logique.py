# test_logique.py

from src.calculator import calculer_devis

resultat = calculer_devis(
    jours_junior=10,
    jours_confirme=5,
    jours_senior=2,
    frais_deplacement=500.0,
    marge_cible=0.25
)

print("--- RÉSULTATS DU CHIFFRAGE ---")
print(f"Coût de revient total : {resultat['cout_revient_total']:.2f} €")
print(f"Prix de vente conseillé : {resultat['prix_vente_conseille']:.2f} €")
print(f"Marge brute générée   : {resultat['marge_brute_euros']:.2f} €")