from typing import Any, Dict, List
import pandas as pd


def calculer_kpis_globaux(devis_liste: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calcule les indicateurs clés de performance financiers consolidés."""
    if not devis_liste:
        return {
            "total_devis": 0,
            "ca_total": 0.0,
            "marge_moyenne_pct": 0.0,
            "marge_totale_euros": 0.0,
            "total_jours_hommes": 0,
            "repartition_profils": {
                "Junior": 0,
                "Confirmé": 0,
                "Senior": 0,
            },
        }
    # Transformation Dico en BBD
    df = pd.DataFrame(devis_liste)

    # KPI

    ca_total = float(df["prix_vente_conseille"].sum())
    marge_totale_euros = float(df["marge_brute_euros"].sum())
    marge_moyenne_pct = float(df["marge_cible"].mean() * 100)
    total_junior = int(df["jours_junior"].sum())
    total_confirme = int(df["jours_confirme"].sum())
    total_senior = int(df["jours_senior"].sum())
    total_jours = total_junior + total_confirme + total_senior

    return {
        "total_devis": len(df),
        "ca_total": round(ca_total, 2),
        "marge_moyenne_pct": round(marge_moyenne_pct, 2),
        "marge_totale_euros": round(marge_totale_euros, 2),
        "total_jours_hommes": total_jours,
        "repartition_profils": {
            "Junior": total_junior,
            "Confirmé": total_confirme,
            "Senior": total_senior,
        },
    }
