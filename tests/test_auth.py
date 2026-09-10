import pytest
from fastapi import HTTPException
from src.auth import verifier_cle_api


def test_cle_valide(monkeypatch):
    monkeypatch.setenv("API_KEY_SECRET", "ma-cle-secrete")
    resultat = verifier_cle_api(cle_recue="ma-cle-secrete")
    assert resultat == "ma-cle-secrete"


def test_cle_invalide(monkeypatch):
    with pytest.raises(HTTPException) as exc_info:
        verifier_cle_api(cle_recue="cle_invalide")
    assert exc_info.value.status_code == 401
    assert "Clé API invalide" in exc_info.value.detail
