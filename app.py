import streamlit as st
import pandas as pd
from src.calculator import calculer_devis
from src.models import QuoteInput
from pydantic import ValidationError

st.set_page_config(page_title="Quote Optimizer", page_icon="📊", layout="wide")

# On applique le cache Streamlit sur la fonction importée directement dans l'app
calculer_devis_cached = st.cache_data(calculer_devis)


st.title("Quote Optimizer")
st.write("Optimisez vos chiffrages de projets web et d'analyse de données.")

# --- Formulaire de saisie ---
st.header("1. Saisie des données du projet")

col1, col2 = st.columns(2)

with col1:
    jours_junior = st.number_input("Jours Développeur Junior (300€/j)", value=0)
    jours_confirme = st.number_input("Jours Développeur Confirmé (500€/j)", value=0)
    jours_senior = st.number_input("Jours Développeur Senior (800€/j)", value=0)

with col2:
    frais_deplacement = st.number_input("Frais de déplacement / Annexes (€)", value=0)
    marge_cible_pct = st.slider("Marge cible (%)", min_value=5, max_value=80, value=25)

# ---marge en décimal---
marge_cible_decimal = marge_cible_pct / 100.0

# ---Pydantic---
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
    # Récupération du premier message d'erreur Pydantic
    erreur_saisie = e.errors()[0]["msg"]
if erreur_saisie:
    st.error(f"Erreur de saisie : {erreur_saisie}")

# ---Bouton de calcul---
bouton_calcul = st.button(
    "Calculer le devis", type="primary", disabled=bool(erreur_saisie)
)

# --Resultat du Calcul"
resultats_container = st.container()

# --- Calcul et affichage ---
if bouton_calcul and not erreur_saisie:
    resultats_container.empty()
    with resultats_container:
        try:
            res = calculer_devis_cached(quote_input)

            st.markdown("---")
            st.header("2. Résultats du chiffrage")

            # KPIs principaux
            m1, m2, m3 = st.columns(3)
            m1.metric("Coût de revient total", f"{res['cout_revient_total']:.2f} €")
            m2.metric("Prix de vente conseillé", f"{res['prix_vente_conseille']:.2f} €")
            m3.metric("Marge brute générée", f"{res['marge_brute_euros']:.2f} €")

            st.subheader("💡 Détail de la structure des coûts")

            d1, d2, d3 = st.columns(3)
            d1.write(f"• **Main-d'œuvre brute :** {res['cout_humain_total']:.2f} €")
            d2.write(f"• **Frais généraux (5%) :** {res['frais_generaux']:.2f} €")
            d3.write(f"• **Frais annexes :** {res['frais_deplacement']:.2f} €")

            # --- Visualisation graphique ---
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

            # --- Exportation CSV ---
            st.subheader("📥 Exporter la synthèse")

            df_export = pd.DataFrame(
                [
                    {
                        "Jours Junior": jours_junior,
                        "Jours Confirme": jours_confirme,
                        "Jours Senior": jours_senior,
                        "Cout Main Oeuvre (€)": round(res["cout_humain_total"], 2),
                        "Frais Generaux (€)": round(res["frais_generaux"], 2),
                        "Frais Annexes (€)": round(res["frais_deplacement"], 2),
                        "Cout Revient Total (€)": round(res["cout_revient_total"], 2),
                        "Prix Vente Conseille (€)": round(
                            res["prix_vente_conseille"], 2
                        ),
                        "Marge Brute (€)": round(res["marge_brute_euros"], 2),
                    }
                ]
            )

            csv_data = df_export.to_csv(index=False, sep=";").encode("utf-8-sig")

            st.download_button(
                label="📄 Télécharger le devis (.CSV)",
                data=csv_data,
                file_name="devis_quote_optimizer.csv",
                mime="text/csv",
            )
        except ValueError as e:
            st.error(f"Erreur de saisie : {e}")
