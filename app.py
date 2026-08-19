import pandas as pd
from pydantic import ValidationError
import streamlit as st

from src.calculator import calculer_devis
from src.crud import obtenir_tous_les_devis, sauvegarder_devis
from src.database import SessionLocal, init_db
from src.logger import logger
from src.models import QuoteInput
from src.pdf_generator import generer_pdf_devis

from src.client import QuoteAPIClient

# Initialisation de la BDD
init_db()

api_client = QuoteAPIClient()
api_active = api_client.verifier_sante()

st.set_page_config(page_title="Quote Optimizer", page_icon="📊", layout="wide")

calculer_devis_cached = st.cache_data(calculer_devis)

st.title("Quote Optimizer")
st.write("Optimisez vos chiffrages de projets web et d'analyse de données.")


# Indicateur de statut de l'API dans la barre latérale
if api_active:
    st.sidebar.success("🟢 API FastAPI Connectée")
else:
    st.sidebar.warning("🟠 Mode Autonome (API Déconnectée)")

tab_calcul, tab_historique = st.tabs(["💡 Nouveau Devis", "📜 Historique des Devis"])
# Déclaration des onglets
tab_calcul, tab_historique = st.tabs(["💡 Nouveau Devis", "📜 Historique des Devis"])

# --- ONGLET 1 : CALCULATEUR ---
with tab_calcul:
    st.subheader("Calculateur de Devis")

    col1, col2 = st.columns(2)

    with col1:
        jours_junior = st.number_input(
            "Jours Développeur Junior (300€/j)", min_value=0, value=0
        )
        jours_confirme = st.number_input(
            "Jours Développeur Confirmé (500€/j)", min_value=0, value=0
        )
        jours_senior = st.number_input(
            "Jours Développeur Senior (800€/j)", min_value=0, value=0
        )

    with col2:
        frais_deplacement = st.number_input(
            "Frais de déplacement / Annexes (€)", min_value=0.0, value=0.0
        )
        marge_cible_pct = st.slider(
            "Marge cible (%)", min_value=5, max_value=80, value=25
        )

    marge_cible_decimal = marge_cible_pct / 100.0

    # Validation Pydantic
    erreur_saisie = None
    quote_input = None

    try:
        quote_input = QuoteInput(
            jours_junior=jours_junior,
            jours_confirme=jours_confirme,
            jours_senior=jours_senior,
            frais_deplacement=frais_deplacement,
            marge_cible=marge_cible_decimal,
        )
    except ValidationError as e:
        erreur_saisie = e.errors()[0]["msg"]
        logger.warning(f"Saisie invalide détectée : {erreur_saisie}")

    if erreur_saisie:
        st.error(f"Erreur de saisie : {erreur_saisie}")

    bouton_calcul = st.button(
        "Calculer le devis", type="primary", disabled=(erreur_saisie is not None)
    )

    if bouton_calcul and not erreur_saisie and quote_input:
        try:
            if api_active:
                devis_data = api_client.creer_devis(quote_input)
                res = calculer_devis(quote_input)
            else:
                res = calculer_devis_cached(quote_input)

            # --- Sauvegarde en base de données ---
            db = SessionLocal()
            try:
                sauvegarder_devis(db, quote_input, res)
            finally:
                db.close()

            st.success("Devis calculé et enregistré en base de données !")
            st.markdown("---")
            st.header("2. Résultats du chiffrage")

            m1, m2, m3 = st.columns(3)
            m1.metric("Coût de revient total", f"{res['cout_revient_total']:.2f} €")
            m2.metric(
                "Prix de vente conseillé",
                f"{res['prix_vente_conseille']:.2f} €",
            )
            m3.metric("Marge brute générée", f"{res['marge_brute_euros']:.2f} €")

            st.subheader("💡 Détail de la structure des coûts")
            d1, d2, d3 = st.columns(3)
            d1.write(f"• **Main-d'œuvre brute :** {res['cout_humain_total']:.2f} €")
            d2.write(f"• **Frais généraux (5%) :** {res['frais_generaux']:.2f} €")
            d3.write(f"• **Frais annexes :** {res['frais_deplacement']:.2f} €")

            st.subheader("📈 Ventilation du Prix de Vente")
            df_chart = (
                pd.DataFrame(
                    {
                        "Poste": [
                            "Main-d'œuvre",
                            "Frais Généraux",
                            "Frais Annexes",
                            "Marge Brute",
                        ],
                        "Montant (€)": [
                            res["cout_humain_total"],
                            res["frais_generaux"],
                            res["frais_deplacement"],
                            res["marge_brute_euros"],
                        ],
                    }
                )
                .set_index("Poste")
                .round(2)
            )
            st.bar_chart(df_chart)

            st.subheader("📥 Exporter la synthèse")
            pdf_bytes = generer_pdf_devis(quote_input, res)
            st.download_button(
                label="📄 Télécharger le devis (.PDF)",
                data=pdf_bytes,
                file_name="devis_quote_optimizer.pdf",
                mime="application/pdf",
            )
        except Exception as e:
            logger.error(f"Erreur inattendue lors du calcul : {e}", exc_info=True)
            st.error(f"Erreur de calcul : {e}")

# --- ONGLET 2 : HISTORIQUE ---
with tab_historique:
    st.subheader("Historique des devis enregistrés en BDD")

    if api_active:
        liste_raw = api_client.recuperer_historique()
        if liste_raw:
            data = [
                {
                    "ID": d["id"],
                    "Date": d["date_creation"][:16].replace("T", " "),
                    "Jr Junior": d["jours_junior"],
                    "Jr Confirmé": d["jours_confirme"],
                    "Jr Senior": d["jours_senior"],
                    "Frais Dep (€)": d["frais_deplacement"],
                    "Marge (%)": f"{d['marge_cible'] * 100:.1f}%",
                    "Coût Total (€)": d["cout_revient_total"],
                    "Prix Vente (€)": d["prix_vente_conseille"],
                }
                for d in liste_raw
            ]
            st.dataframe(pd.DataFrame(data), use_container_width=True)
        else:
            st.info("Aucun devis enregistré en base.")
    else:
        db = SessionLocal()
        try:
            devis_liste = obtenir_tous_les_devis(db)
            if devis_liste:
                data = [
                    {
                        "ID": d.id,
                        "Date": d.date_creation.strftime("%Y-%m-%d %H:%M"),
                        "Jr Junior": d.jours_junior,
                        "Jr Confirmé": d.jours_confirme,
                        "Jr Senior": d.jours_senior,
                        "Frais Dep (€)": d.frais_deplacement,
                        "Marge (%)": f"{d.marge_cible * 100:.1f}%",
                        "Coût Total (€)": d.cout_revient_total,
                        "Prix Vente (€)": d.prix_vente_conseille,
                    }
                    for d in devis_liste
                ]
                st.dataframe(pd.DataFrame(data), use_container_width=True)
            else:
                st.info("Aucun devis enregistrer en base.")
        finally:
            db.close()
