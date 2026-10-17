from src.extraction import extraire_texte

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
