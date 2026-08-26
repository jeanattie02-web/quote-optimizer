from src.analytics import calculer_kpis_globaux
import pytest


def test_calculer_kpis_liste_vide():
    kpis = calculer_kpis_globaux([])
    assert kpis["total_devis"] == 0
    assert kpis["ca_total"] == 0.0
    assert kpis["total_jours_hommes"] == 0


def test_calculer_kpis_avec_donnees():
    donnees = [
        {
            "prix_vente_conseille": 1000.0,
            "marge_brute_euros": 200.0,
            "marge_cible": 0.20,
            "jours_junior": 2,
            "jours_confirme": 1,
            "jours_senior": 0,
        },
        {
            "prix_vente_conseille": 3000.0,
            "marge_brute_euros": 900.0,
            "marge_cible": 0.30,
            "jours_junior": 0,
            "jours_confirme": 2,
            "jours_senior": 2,
        },
    ]
    kpis = calculer_kpis_globaux(donnees)

    assert kpis["total_devis"] == 2
    assert kpis["ca_total"] == pytest.approx(4000.0)
    assert kpis["marge_totale_euros"] == pytest.approx(1100.0)
    assert kpis["marge_moyenne_pct"] == pytest.approx(25.0)
    assert kpis["total_jours_hommes"] == 7
    assert kpis["repartition_profils"]["Junior"] == 2
    assert kpis["repartition_profils"]["Confirmé"] == 3
    assert kpis["repartition_profils"]["Senior"] == 2
