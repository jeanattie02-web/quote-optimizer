import streamlit as st
from src.calculator import calculer_devis

st.title(" Quote Optimizer")
st.write("Optimisez vos chiffrages de projets web et d'analyse de données.")

# --- Formulaire de saisie ---
st.header("1. Saisie des données du projet")

col1, col2 = st.columns(2)

with col1:
    jours_junior = st.number_input("Jours Développeur Junior (300€/j)", min_value=0, value=10)
    jours_confirme = st.number_input("Jours Développeur Confirmé (500€/j)", min_value=0, value=5)
    jours_senior = st.number_input("Jours Développeur Senior (800€/j)", min_value=0, value=2)

with col2:
    frais_deplacement = st.number_input("Frais de déplacement / Annexes (€)", min_value=0.0, value=500.0)
    marge_cible_pct = st.slider("Marge cible (%)", min_value=5, max_value=80, value=25)

# --- Calcul et affichage ---
if st.button("Calculer le devis"):
    marge_cible_decimal = marge_cible_pct / 100.0
    
    res = calculer_devis(
        jours_junior=jours_junior,
        jours_confirme=jours_confirme,
        jours_senior=jours_senior,
        frais_deplacement=frais_deplacement,
        marge_cible=marge_cible_decimal
    )

    st.markdown("---")
    st.header("2. Résultats du chiffrage")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Coût de revient total", f"{res['cout_revient_total']:.2f} €")
    m2.metric("Prix de vente conseillé", f"{res['prix_vente_conseille']:.2f} €")
    m3.metric("Marge brute générée", f"{res['marge_brute_euros']:.2f} €")