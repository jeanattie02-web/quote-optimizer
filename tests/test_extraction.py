import pytest
from src.extraction import extraire_texte, MOTIF_JOURS, lire_jours_tableaux

LYON = "tests/data/demandes/demande_lyon.pdf"
BORDEAUX = "tests/data/demandes/demande_bordeaux.pdf"


def test_extraire_texte_renvoie_un_texte_non_vide():
    texte = extraire_texte(LYON)
    assert isinstance(texte, str)
    assert len(texte) > 0


def test_extraire_texte_trouve_les_informations_cles():
    texte = extraire_texte(LYON)
    assert "Développeur junior" in texte
    assert "20 jours" in texte
    assert "1 500" in texte


def test_extraire_texte_document_sans_charge():
    texte = extraire_texte(BORDEAUX)
    assert "Bordeaux" in texte
    assert "jours" not in texte


@pytest.mark.parametrize(
    "texte, attendu",
    [
        ("développeur junior 20 jours", 20),
        ("expert senior 1 jour", 1),
        ("consultant confirmé 3jours", 3),
        ("profil charge estimée", None),
    ],
)
def test_motif_jours(texte, attendu):
    resultat = MOTIF_JOURS.search(texte)
    if attendu is None:
        assert resultat is None
    else:
        assert resultat is not None
        assert int(resultat.group(1)) == attendu


def test_lire_jours_tableaux_trouve_les_jours():
    assert lire_jours_tableaux(LYON) == {
        "jours_junior": 20,
        "jours_confirme": 10,
        "jours_senior": 3,
    }


def test_lire_jours_tableaux_document_sans_tableau():
    assert lire_jours_tableaux(BORDEAUX) == {}
