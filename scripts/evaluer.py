"""Évalue l'extraction sur les demandes de test, en comparant aux valeurs attendues."""

import json

from src.extraction import analyser_demande

DOSSIER = "tests/data/demandes"


def comparer(attendu, obtenu) -> str:
    """Classe le résultat d'un champ : juste, hallucination, oubli ou erreur."""
    if attendu == obtenu:
        return "juste"
    if attendu is None:
        return "hallucination"
    if obtenu is None:
        return "oubli"
    return "erreur"


def main():
    with open(f"{DOSSIER}/attendus.json", encoding="utf-8") as fichier:
        attendus = json.load(fichier)

    bilan = {"juste": 0, "hallucination": 0, "oubli": 0, "erreur": 0}
    for nom, valeurs_attendues in attendus.items():
        obtenu = analyser_demande(f"{DOSSIER}/{nom}").model_dump()
        for champ, attendu in valeurs_attendues.items():
            resultat = comparer(attendu, obtenu[champ])
            bilan[resultat] += 1
            print(
                f"{nom:22} {champ:18} attendu={attendu!s:6} "
                f"obtenu={obtenu[champ]!s:6} → {resultat}"
            )

    total = sum(bilan.values())
    print(f"\nChamps justes : {bilan['juste']}/{total}")
    print(bilan)


if __name__ == "__main__":
    main()
