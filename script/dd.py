import sys
from grammaire import lire
from itertools import product


def generer_mots(grammaire, axiome, n):
    def expansion(symbole, longueur, visités):
        if longueur > n:
            return set()  # Ignorer les mots trop longs
        if symbole.islower():  # Si le symbole est un terminal
            return {symbole}

        # Si c'est un non-terminal, vérifier pour éviter les cycles
        if symbole in visités:
            return set()  # Éviter les cycles récursifs

        # Ajouter le symbole au chemin des visités
        visités.add(symbole)

        # Expansion des règles
        mots = set()
        for production in grammaire.regles.get(symbole, []):
            if production == "":  # Gérer epsilon (E)
                mots.add("E")  # Ajouter E (epsilon) comme un mot valide
                continue

            # Expansion pour chaque symbole dans la production
            expansions = [expansion(s, longueur + 1, set(visités)) for s in production]
            # Générer tous les produits cartésiens des expansions
            for combinaison in product(*expansions):
                mot = ''.join(combinaison)
                if len(mot) <= n:
                    mots.add(mot)

        # Retirer le symbole du chemin des visités après le traitement
        visités.remove(symbole)

        return mots

    # Générer les mots à partir de l'axiome
    return expansion(axiome, 0, set())


def ecrire_mots(mots, fichier_sortie):
    with open(fichier_sortie, 'w') as f:
        for mot in sorted(mots):  # Trier les mots et les écrire ligne par ligne
            f.write(mot + '\n')


def main():
    if len(sys.argv) != 3:
        print("Usage : python generer.py <fichier_grammaire> <longueur_max>")
        sys.exit(1)

    fichier_grammaire = sys.argv[1]
    longueur_max = int(sys.argv[2])

    # Lire la grammaire depuis le fichier
    grammaire = lire(fichier_grammaire)

    # Vérifier que la grammaire contient des règles
    if not grammaire.regles:
        print(f"Erreur : La grammaire dans le fichier '{fichier_grammaire}' est vide ou invalide.")
        sys.exit(1)

    # L'axiome est toujours le premier non-terminal dans le fichier
    axiome = list(grammaire.regles.keys())[0]

    # Générer les mots
    mots = generer_mots(grammaire, axiome, longueur_max)

    # Créer le nom du fichier de sortie
    fichier_sortie = fichier_grammaire.split(".")[0] + ".word"

    # Écrire les mots générés dans le fichier `.word`
    ecrire_mots(mots, fichier_sortie)


if __name__ == "__main__":
    main()
