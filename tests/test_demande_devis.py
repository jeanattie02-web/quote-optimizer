import json

import pytest
from pydantic import ValidationError

from src.extraction import DemandeDevis


def test_demande_devis_champs_absents_par_defaut():
    demande = DemandeDevis()
    assert demande.jours_junior is None


def test_demande_devis_refuse_les_valeurs_negatives():
    with pytest.raises(ValidationError):
        DemandeDevis(jours_junior=-3)


def test_attendus_respectent_le_format():
    with open("tests/data/demandes/attendus.json", encoding="utf-8") as fichier:
        attendus = json.load(fichier)
    for valeurs in attendus.values():
        DemandeDevis(**valeurs)