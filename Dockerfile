# ---- 1 : "builder" ----
# Cette étape sert UNIQUEMENT à installer les dépendances.
# Elle contient build-essential (compilateurs, etc.) mais ne sera PAS conservée dans l'image finale.
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# --target=/install : au lieu d'installer les paquets "dans" Python globalement,
# on les installe dans un dossier isolé /install qu'on pourra copier proprement à l'étape suivante.
RUN pip install --no-cache-dir -r requirements.txt --target=/install

# ---- 2 : image finale, légère ----
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# On récupère UNIQUEMENT les paquets déjà installés depuis le builder.
# Pas de build-essential, pas de cache pip : gain de poids important.
COPY --from=builder /install /usr/local/lib/python3.11/site-packages

COPY src/ ./src/
COPY app.py .
COPY pytest.ini .

# Création d'un utilisateur non-privilégié, et on lui donne la main sur /app
RUN useradd --create-home appuser && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000 8501

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]