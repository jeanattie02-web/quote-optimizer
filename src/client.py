import os
from typing import Any, Dict, List, Optional
import httpx
from src.logger import logger
from src.models import QuoteInput

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


class QuoteAPIClient:
    """Client HTTP pour interagir avec l'API Quote Optimizer."""

    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url.rstrip("/")

    def verifier_sante(self) -> bool:
        """Vérifie si l'API est en ligne et accessible."""
        try:
            response = httpx.get(f"{self.base_url}/health", timeout=3.0)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Impossible de joindre l'API : {e}")
            return False

    def creer_devis(self, payload: QuoteInput) -> Dict[str, Any]:
        """Envoie une requête de calcul et sauvegarde de devis à l'API."""
        url = f"{self.base_url}/quotes"
        try:
            response = httpx.post(url, json=payload.model_dump(), timeout=5.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(
                f"Erreur HTTP API ({e.response.status_code}) : {e.response.text}"
            )
            raise ValueError(f"Erreur renvoyée par le serveur : {e.response.text}")
        except Exception as e:
            logger.error(f"Erreur réseau lors de l'appel API : {e}")
            raise RuntimeError(f"Échec de communication avec l'API : {e}")

    def recuperer_historique(
        self, skip: int = 0, limit: int = 100, min_prix: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Récupère la liste des devis enregistrés."""
        url = f"{self.base_url}/quotes"
        params: Dict[str, Any] = {"skip": skip, "limit": limit}
        if min_prix is not None:
            params["min_prix"] = min_prix

        try:
            response = httpx.get(url, params=params, timeout=5.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'historique : {e}")
            return []

    def supprimer_devis(self, quote_id: int) -> bool:
        """Envoie une requête de suppression d'un devis à l'API."""
        url = f"{self.base_url}/quotes/{quote_id}"
        try:
            response = httpx.delete(url, timeout=5.0)
            return response.status_code == 204
        except Exception as e:
            logger.error(f"Erreur lors de la suppression du devis #{quote_id} : {e}")
            return False
