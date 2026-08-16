from starlette.testclient import TestClient as TestClient  # noqa
from src.api import app
from src.database import init_db

client = TestClient(app)

# Initialisation des tables SQLite pour les tests
init_db()

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_creer_et_lister_devis_via_api():
    payload = {
        "jours_junior": 4,
        "jours_confirme": 2,
        "jours_senior": 1,
        "frais_deplacement": 150.0,
        "marge_cible": 0.20,
    }

    # Test de création POST /quotes
    post_response = client.post("/quotes", json=payload)
    assert post_response.status_code == 201
    data = post_response.json()
    assert data["id"] is not None
    assert data["prix_vente_conseille"] > 0

    # Test de lecture GET /quotes
    get_response = client.get("/quotes")
    assert get_response.status_code == 200
    devis_liste = get_response.json()
    assert len(devis_liste) > 0
    assert any(d["id"] == data["id"] for d in devis_liste)
