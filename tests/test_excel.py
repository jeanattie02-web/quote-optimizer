from src.calculator import calculer_devis
from src.excel_generator import generer_excel_devis
from src.models import QuoteInput


def test_generer_excel_devis_non_vide():
    payload = QuoteInput(
        jours_junior=2,
        jours_confirme=3,
        jours_senior=1,
        frais_deplacement=200.0,
        marge_cible=0.25,
    )
    res = calculer_devis(payload)
    excel_bytes = generer_excel_devis(payload, res)

    assert isinstance(excel_bytes, bytes)
    assert len(excel_bytes) > 0
    # Signature magique d'un fichier ZIP / XLSX valide (PK..)
    assert excel_bytes.startswith(b"PK")
