import pytest
from src.calculator import calculer_devis
from pydantic import ValidationError
from src.models import QuoteInput


def test_calculer_devis_nominal():
    data = QuoteInput(
        jours_junior=10,
        jours_confirme=5,
        jours_senior=2,
        frais_deplacement=500.0,
        marge_cible=0.25,
    )
    res = calculer_devis(data)

    assert res["cout_humain_total"] == 7100.0
    assert res["frais_generaux"] == 355.0
    assert res["cout_revient_total"] == 7955.0
    assert round(res["prix_vente_conseille"], 2) == 10606.67
    assert round(res["marge_brute_euros"], 2) == 2651.67


def test_validation_pydantic_marge_invalide():
    with pytest.raises(ValidationError):
        QuoteInput(marge_cible=1.5)


def test_validation_pydantic_jours_negatifs():
    with pytest.raises(ValidationError):
        QuoteInput(jours_junior=-1)


def test_validation_pydantic_frais_negatifs():
    with pytest.raises(ValidationError):
        QuoteInput(frais_deplacement=-100)
