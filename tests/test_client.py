from unittest.mock import MagicMock, patch
import httpx
from src.client import QuoteAPIClient
from src.models import QuoteInput


@patch("httpx.get")
def test_verifier_sante_api_ok(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    client = QuoteAPIClient()
    assert client.verifier_sante() is True


@patch("httpx.get")
def test_verifier_sante_api_ko(mock_get):
    mock_get.side_effect = httpx.RequestError("API Offline")

    client = QuoteAPIClient()
    assert client.verifier_sante() is False


@patch("httpx.post")
def test_creer_devis_via_client(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": 42, "prix_vente_conseille": 2500.0}
    mock_post.return_value = mock_response

    client = QuoteAPIClient()
    payload = QuoteInput(
        jours_junior=1,
        jours_confirme=1,
        jours_senior=1,
        frais_deplacement=0.0,
        marge_cible=0.2,
    )
    result = client.creer_devis(payload)
    assert result["id"] == 42
    assert result["prix_vente_conseille"] == 2500.0
