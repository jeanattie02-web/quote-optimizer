FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source et de la configuration
COPY src/ ./src/
COPY app.py .
COPY pytest.ini .

# Exposition des ports (FastAPI: 8000, Streamlit: 8501)
EXPOSE 8000 8501

#Commande par défaut
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]