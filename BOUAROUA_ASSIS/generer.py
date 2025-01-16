import sys
from grammaire import lire
from itertools import product


def generer_mots(grammaire, axiome: str, n: int):
    def expansion(symbole: str, longueur: int, visites: set):
        if longueur > n:  # Ignorer les mots trop longs
            return set()
        if symbole not in grammaire.regles:  # Si le symbole est un terminal
            return {symbole}

        # Ajouter le symbole à la liste des visités
        visites.add(symbole)

        mots = set()
        for production in grammaire.regles.get(symbole, []):
            if production == "E":  # Gestion de l'epsilon (E)
                mots.add("E")
                continue

            # Expansion récursive pour chaque symbole dans la production
            expansions = [expansion(s, longueur + 1, visites.copy()) for s in production]
            for combinaison in product(*expansions):
                mot = ''.join(combinaison)
                if len(mot) <= n:
                    mots.add(mot)

        # Retirer le symbole après traitement
        visites.remove(symbole)

        return mots

    # Générer les mots à partir de l'axiome
    mots = expansion(axiome, 0, set())

    # Inclure explicitement l'epsilon si applicable
    if "" in grammaire.regles.get(axiome, []):
        mots.add("E")

    return mots


def main():
    if len(sys.argv) != 3:
        print("Usage : python generer.py <fichier_grammaire> <longueur_max>")
        sys.exit(1)

    fichier_grammaire = sys.argv[1]
    longueur_max = int(sys.argv[2])

    # Lire la grammaire depuis le fichier
    grammaire = lire(fichier_grammaire)

    # L'axiome est toujours le premier non-terminal dans le fichier
    axiome = list(grammaire.regles.keys())[0]

    # Générer les mots
    mots = generer_mots(grammaire, axiome, longueur_max)

    # Trier les mots en ordre lexicographique et les afficher
    for mot in sorted(mots):
        print(mot)


if __name__ == "__main__":
    main()
