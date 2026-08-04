import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

from src.models import QuoteInput
from src.logger import logger


def generer_pdf_devis(input_data: QuoteInput, resultats: dict) -> bytes:
    """Génère un fichier PDF en mémoire et retourne son contenu binaire."""
    logger.info("Génération du document PDF du devis en cours...")
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()
    story = []

    # En-tête
    title_style = styles["Title"]
    title_style.textColor = colors.HexColor("#1E3A8A")
    story.append(Paragraph("DEVIS - QUOTE OPTIMIZER", title_style))
    story.append(Spacer(1, 12))

    # Détail des prestations
    data_table = [
        ["Poste", "Quantité (Jours / Unités)", "Montant (€)"],
        [
            "Développeur Junior (300€/j)",
            str(input_data.jours_junior),
            f"{input_data.jours_junior * 300:.2f} €",
        ],
        [
            "Développeur Confirmé (500€/j)",
            str(input_data.jours_confirme),
            f"{input_data.jours_confirme * 500:.2f} €",
        ],
        [
            "Développeur Senior (800€/j)",
            str(input_data.jours_senior),
            f"{input_data.jours_senior * 800:.2f} €",
        ],
        ["Frais Annexes / Déplacement", "-", f"{resultats['frais_deplacement']:.2f} €"],
        ["Frais Généraux (5%)", "-", f"{resultats['frais_generaux']:.2f} €"],
    ]

    t = Table(data_table, colWidths=[240, 140, 140])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563EB")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ]
        )
    )
    story.append(t)
    story.append(Spacer(1, 20))

    # Synthèse Financière
    summary_data = [
        ["Coût de revient total", f"{resultats['cout_revient_total']:.2f} €"],
        ["Marge cible appliquée", f"{input_data.marge_cible * 100:.1f} %"],
        ["Prix de vente conseillé", f"{resultats['prix_vente_conseille']:.2f} €"],
    ]

    t_summary = Table(summary_data, colWidths=[300, 220])
    t_summary.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 2), (-1, 2), colors.HexColor("#D1FAE5")),
                ("FONTNAME", (0, 2), (-1, 2), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ]
        )
    )
    story.append(t_summary)

    doc.build(story)
    pdf_data = buffer.getvalue()
    buffer.close()

    logger.info("Génération du PDF terminée avec succès.")
    return pdf_data
