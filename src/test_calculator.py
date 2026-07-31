import pytest
from src.calculator import calculer_devis

def test_calculer_devis_nominal():
    res = calculer_devis(
        jours_junior=10,
        jours_confirme=5,
        jours_senior=2,
        frais_deplacement=500.0,
        marge_cible=0.25
    )
    
    assert res["cout_humain_total"] == 7100.0
    assert res["frais_generaux"] == 355.0
    assert res["cout_revient_total"] == 7955.0
    assert round(res["prix_vente_conseille"], 2) == 10606.67
    assert round(res["marge_brute_euros"], 2) == 2651.67

def test_marge_invalide():
    with pytest.raises(ValueError):
        calculer_devis(1, 1, 1, 100, 1.2)