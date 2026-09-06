import os
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def verifier_cle_api(cle_recue: str = Security(api_key_header)):
    """Vérifie que l'en-tête X-API-Key correspond à la clé secrète attendue."""
    cle_attendue = os.getenv("API_KEY_SECRET")

    if cle_recue != cle_attendue:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clé API invalide ou manquante.",
        )
    return cle_recue
