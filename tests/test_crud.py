from src.calculator import calculer_devis
from src.crud import obtenir_tous_les_devis, sauvegarder_devis
from src.database import SessionLocal, init_db
from src.models import QuoteInput


def test_sauvegarder_et_lire_devis():
    init_db()
    db = SessionLocal()

    try:
        data = QuoteInput(
            jours_junior=2,
            jours_confirme=3,
            jours_senior=1,
            frais_deplacement=100.0,
            marge_cible=0.25,
        )
        res = calculer_devis(data)

        # Insère en base
        devis_cree = sauvegarder_devis(db, data, res)
        assert devis_cree.id is not None
        assert devis_cree.prix_vente_conseille == res["prix_vente_conseille"]

        # Récupère l'historique
        historique = obtenir_tous_les_devis(db)
        assert len(historique) > 0
        assert historique[0].id == devis_cree.id

    finally:
        db.close()
