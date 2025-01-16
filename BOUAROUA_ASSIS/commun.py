from itertools import product


def generer_non_terminal(existants: set):

    lettres = [chr(i) for i in range(65, 91) if chr(i) != 'E']  # De 'A' à 'Z', sauf 'E'

    for lettre in lettres:
        if lettre not in existants:
            return lettre

    for lettre in lettres:
        for i in range(1, 11):  # De 1 à 10
            non_terminal = f"{lettre}{i}"
            if non_terminal not in existants:
                return non_terminal


def retirer_axiome(grammaire, axiome: str):
    # Récupérer les non-terminaux existants
    existants = set(grammaire.regles.keys())

    # Générer un nouveau non-terminal unique
    nouveau_non_terminal = generer_non_terminal(existants)

    # Copier toutes les règles de l'axiome dans le nouveau non-terminal,
    # en remplaçant les occurrences récursives par le nouveau non-terminal
    nouvelles_regles = []
    for droite in grammaire.regles[axiome]:
        if axiome in droite:
            nouvelles_regles.append(droite.replace(axiome, nouveau_non_terminal))
        else:
            nouvelles_regles.append(droite)

    # Ajouter le nouveau non-terminal à la grammaire
    grammaire.regles[nouveau_non_terminal] = nouvelles_regles

    # Remplacer les règles de l'axiome par une seule référence au nouveau non-terminal
    grammaire.regles[axiome] = [nouveau_non_terminal]


def generer_variantes_epsilon(droite: str, epsilon_produits: set):
    # Identifier les positions des non-terminaux epsilon-productifs dans la règle
    positions = [i for i, char in enumerate(droite) if char in epsilon_produits]

    # Si aucun epsilon-produit, retourne simplement la règle
    if not positions:
        return {droite}

    # Générer toutes les combinaisons de True (garder) ou False (supprimer) pour chaque position
    variantes = set()
    for combinaison in product([True, False], repeat=len(positions)):
        nouvelle_regle = list(droite)
        for i, garder in enumerate(combinaison):
            if not garder:
                # Remplace par vide (supprime le caractère à cette position)
                nouvelle_regle[positions[i]] = ""
        variante = "".join(nouvelle_regle)  # Reconstitue la règle
        if variante:  # Élimine les variantes totalement vides (hors axiome)
            variantes.add(variante)
    return variantes


def supprimer_epsilon(grammaire, axiome: str):
    # Trouver tous les non-terminaux qui produisent ε (sauf l'axiome)
    epsilon_produits = {gauche for gauche, droites in grammaire.regles.items() if "" in droites and gauche != axiome}

    nouvelles_regles = {}
    for gauche, droites in grammaire.regles.items():
        nouvelles_droites = set()  # Utilise un set pour éviter les doublons
        for droite in droites:
            # Si la règle est ε
            if droite == "":
                # Conserve ε uniquement si c'est l'axiome
                if gauche == axiome:
                    nouvelles_droites.add("")
                continue

            # Générer toutes les combinaisons possibles en remplaçant les epsilon-produits
            nouvelles_droites.update(generer_variantes_epsilon(droite, epsilon_produits))

        # Ajouter les nouvelles règles pour le non-terminal actuel
        nouvelles_regles[gauche] = list(nouvelles_droites)

    # Si l'axiome produisait ε, s'assurer que "" (epsilon) est conservé
    if "" not in nouvelles_regles.get(axiome, []):
        nouvelles_regles[axiome].append("")

    # Mettre à jour les règles de la grammaire
    grammaire.regles = nouvelles_regles
