import pytest

from scripts.evaluer import comparer


@pytest.mark.parametrize(
    "attendu, obtenu, resultat",
    [
        (20, 20, "juste"),
        (1500, 1500.0, "juste"),
        (None, None, "juste"),
        (None, 3, "hallucination"),
        (20, None, "oubli"),
        (20, 25, "erreur"),
    ],
)
def test_comparer(attendu, obtenu, resultat):
    assert comparer(attendu, obtenu) == resultat
