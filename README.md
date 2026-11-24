# 📊 Quote Optimizer

[![Python CI](https://github.com/jeanattie02-web/quote-optimizer/actions/workflows/ci.yml/badge.svg)](https://github.com/jeanattie02-web/quote-optimizer/actions/workflows/ci.yml)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://quote-optimizer-8uxqzdp7hvzee8awrnyrxg.streamlit.app/)

**Quote Optimizer** est une application de chiffrage de devis pour des projets de développement web et d'analyse de données. On saisit le nombre de jours par profil (junior, confirmé, senior) et les frais annexes ; l'application calcule le coût de revient, le prix de vente conseillé et la marge.

Elle peut aussi **lire une demande de devis en PDF** et préremplir le formulaire grâce à un modèle de langage qui tourne en local avec Ollama : le document ne quitte pas la machine.

🔗 **Application en ligne :** [quote-optimizer-8uxqzdp7hvzee8awrnyrxg.streamlit.app](https://quote-optimizer-8uxqzdp7hvzee8awrnyrxg.streamlit.app/) (sans la lecture des PDF, qui nécessite Ollama en local)

---

## 🚀 Fonctionnalités

* **Calcul du devis :** coût de revient = jours × tarif journalier (300 €, 500 € ou 800 € selon le profil) + 5 % de frais généraux + frais annexes ; prix de vente = coût de revient / (1 − marge cible).
* **Lecture d'une demande de devis PDF :** préremplit les jours et les frais, et signale les champs non trouvés. L'utilisateur vérifie et corrige avant de calculer.
* **Validation des saisies** avec Pydantic (pas de valeurs négatives, marge bornée).
* **Historique des devis** enregistré dans une base SQLite, avec suppression.
* **Indicateurs :** chiffre d'affaires potentiel, marge moyenne, répartition des jours par profil.
* **Export** du devis en PDF et en Excel.
* **API REST (FastAPI)** pour créer, lister et supprimer des devis, avec une clé API pour l'écriture. Si l'API ne répond pas, l'interface passe en mode autonome et écrit directement dans la base.

---

## 🗂️ Organisation du code

```
app.py                     Interface Streamlit
src/
├── calculator.py          Calcul du devis
├── models.py, schemas.py  Modèles Pydantic
├── extraction.py          Lecture des demandes de devis PDF
├── api.py, auth.py        API FastAPI et vérification de la clé API
├── client.py              Client HTTP de l'API, utilisé par l'interface
├── database.py, db_models.py, crud.py   Base SQLite (SQLAlchemy)
├── pdf_generator.py, excel_generator.py Exports PDF et Excel
├── analytics.py           Indicateurs
└── logger.py              Journal (app.log)
scripts/evaluer.py         Évaluation de la lecture des PDF
tests/                     Tests unitaires (pytest)
```

## 🛠️ Stack technique

Python 3.11 · Streamlit · FastAPI · SQLAlchemy / SQLite · Pydantic · pandas · ReportLab · openpyxl · pdfplumber · Ollama (Llama 3.2, 3B) · pytest · Black / Flake8 · GitHub Actions · Docker

L'intégration continue vérifie à chaque Pull Request le style (Flake8, Black), les tests et la construction de l'image Docker.

---

## 💻 Installation et lancement en local

```bash
git clone https://github.com/jeanattie02-web/quote-optimizer.git
cd quote-optimizer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Interface seule (mode autonome) :**

```bash
streamlit run app.py
```

**Avec l'API**, dans deux terminaux, avec la même clé :

```bash
export API_KEY_SECRET=une-cle-de-test
uvicorn src.api:app --reload      # documentation sur http://127.0.0.1:8000/docs
```

```bash
export API_KEY_SECRET=une-cle-de-test
streamlit run app.py
```

**Avec Docker :** `docker compose up --build`, avec `API_KEY_SECRET` défini dans un fichier `.env`. Interface sur le port 8501, API sur le port 8000.

**Lecture des PDF :** installer [Ollama](https://ollama.com), puis télécharger le modèle.

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:3b
```

Le modèle et l'adresse d'Ollama se changent avec les variables `OLLAMA_MODEL` et `OLLAMA_URL`. Une carte graphique est fortement conseillée : sur processeur seul, la lecture d'un document est très lente.

**Tests et évaluation :**

```bash
pytest
python -m scripts.evaluer
```

---

## 📄 Lecture des demandes de devis PDF

### Fonctionnement

Une demande de devis mélange souvent un tableau de charges et du texte libre. L'application fait donc deux lectures complémentaires :

1. **Le texte libre** est confié à un modèle de langage (Llama 3.2, 3 milliards de paramètres) qui tourne en local avec Ollama. Le modèle doit répondre dans un format JSON imposé, décrit par un schéma Pydantic, avec une température de 0 et la consigne de répondre `null` quand une information n'apparaît pas. Sa réponse est ensuite validée par Pydantic.
2. **Les tableaux** sont lus sans IA, avec pdfplumber et une expression régulière. Les jours trouvés dans un tableau remplacent ceux proposés par le modèle.

```
PDF ─┬─ texte ────► modèle local (JSON imposé) ─► validation Pydantic ─┐
     └─ tableaux ─► expression régulière, sans IA ─────────────────────┴─► fusion ─► formulaire prérempli ─► vérification humaine
```

Le modèle propose, l'utilisateur valide : les champs non trouvés sont signalés, car « 0 jour » et « information absente » ne veulent pas dire la même chose.

### Évaluation

Le script `scripts/evaluer.py` compare chaque champ extrait à la valeur attendue (`tests/data/demandes/attendus.json`) et le classe en **juste**, **hallucination** (valeur inventée), **oubli** (valeur manquée) ou **erreur** (mauvaise valeur).

Deux demandes fictives servent de test :
* `demande_lyon.pdf` : un tableau de charges (20, 10 et 3 jours) et 1 500 € de déplacement, avec des nombres pièges (nombre de salariés, d'entrepôts, durée en semaines, budget global) ;
* `demande_bordeaux.pdf` : aucune charge chiffrée, mais des nombres pièges (commerciaux, points de vente, réunions).

**Résultat : 8 champs justes sur 8**, sans hallucination ni oubli.

⚠️ Deux documents, c'est très peu : ce résultat montre que la chaîne fonctionne sur ces cas, pas qu'elle est fiable en général.

### Difficultés rencontrées

* **Un modèle très lent au départ** (0,7 token/s) : la carte graphique n'était pas utilisée. Après un diagnostic étage par étage (Windows, WSL, Ollama), environ 42 tokens/s sur GPU.
* **Des hallucinations :** à la question des jours, le modèle répondait par des jours de la semaine. Corrigé en imposant le schéma JSON, avec une description pour chaque champ.
* **Des tableaux ignorés :** j'ai testé une hypothèse à la fois (accents, contexte, ordre des mots). Le petit modèle ne trouvait les jours que dans une formulation du type « 20 jours de développeur junior ». Un modèle plus gros (qwen2.5:7b) n'a pas fait mieux. J'ai donc choisi de lire les tableaux sans IA et de réserver le modèle au texte libre.
* **Une consigne qui créait des erreurs :** la première évaluation donnait 6/8, avec deux hallucinations sur Bordeaux (2 et 4 jours, tirés de « deux réunions de cadrage » et de « 4 points de vente »). La cause était une consigne que j'avais ajoutée sur les tableaux : elle poussait le modèle à chercher des charges partout. Après l'avoir retirée : 8/8. Depuis, je mesure l'effet de chaque modification.
* **Un fichier de tests ignoré sans erreur :** nommé `tests_evaluer.py` au lieu de `test_evaluer.py`, il n'était pas trouvé par pytest.
* **Un bug invisible :** `"/n"` au lieu de `"\n"` pour séparer les pages. Les tests passaient quand même, car les PDF de test ne font qu'une page : un test qui passe ne couvre que les cas testés.
* **Streamlit relance tout le script à chaque interaction :** le résultat de l'analyse disparaissait dès qu'on touchait au curseur de marge. Il est maintenant gardé dans `st.session_state`.

### Limites

* Testé sur seulement deux documents fictifs.
* La lecture des tableaux repose sur des mots-clés (« junior », « confirmé », « senior ») et sur le format « N jours » : une autre formulation serait manquée.
* Les PDF scannés (images) ne sont pas pris en charge : il n'y a pas de reconnaissance de caractères.
* La partie modèle n'est pas testée par l'intégration continue, où Ollama n'est pas installé : elle est évaluée en local avec `scripts/evaluer.py`.
* Sur la version en ligne et dans Docker, Ollama n'est pas joignable : l'application l'indique et la saisie reste manuelle.

### Pistes

* Enrichir le jeu de test avec des demandes plus variées.
* Un mode dégradé qui lit au moins les tableaux quand le modèle n'est pas disponible.
* Un agent capable, pour une demande incomplète, de chercher des devis similaires dans l'historique et de préparer un e-mail au client, toujours avec une validation humaine.

---

## 🤖 Usage de l'IA dans ce projet

J'ai développé ce projet avec l'aide d'un assistant IA (Claude), utilisé surtout comme tuteur : explications, relecture du code, aide au débogage, et parfois correction directe. Pour la lecture des PDF, j'ai avancé étape par étape, en lisant les erreurs, en formulant des hypothèses et en les testant une à une. L'objectif était de comprendre chaque ligne, pas seulement d'obtenir un code qui fonctionne.