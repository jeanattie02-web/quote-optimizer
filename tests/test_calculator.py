import pytest
from src.calculator import calculer_devis
from pydantic import ValidationError
from src.models import QuoteInput
from src.pdf_generator import generer_pdf_devis


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


def test_export_PDF_devis():
    data = QuoteInput(
        jours_junior=5,
        jours_confirme=2,
        jours_senior=1,
        frais_deplacement=200.0,
        marge_cible=0.20,
    )
    res = calculer_devis(data)
    pdf_bytes = generer_pdf_devis(data, res)

    # Vérifie que le retour est bien du binaire non vide
    # et qu'il commence par le header PDF (%PDF)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0
    assert pdf_bytes.startswith(b"%PDF")
