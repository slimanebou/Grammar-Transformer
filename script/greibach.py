
# generer des variables non-terminal
def generer_non_terminal(existants):
    
    lettres = [chr(i) for i in range(65, 91) if chr(i) != 'E']  # De 'A' à 'Z', sauf 'E'

    for lettre in lettres:
        if lettre not in existants:
            return lettre

    for lettre in lettres:
        for i in range(1, 11):  # De 1 à 10
            non_terminal = f"{lettre}{i}"
            if non_terminal not in existants:
                return non_terminal


# 1. retirer l’axiome des membres droits des règles ;
def retirer_axiome(grammaire, axiome):
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


# 2. supprimer les règles 𝑋 → 𝜀 sauf si 𝑋 est l’axiome ;
from itertools import product
def generer_variantes_epsilon(droite, epsilon_produits):
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


def supprimer_epsilon(grammaire, axiome):
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

# 3. supprimer les règles unité 𝑋 → 𝑌 
def supprimer_unites(grammaire):
    nouvelles_regles = {}

    for gauche in grammaire.regles:
        # Collecte des productions finales pour ce non-terminal
        nouvelles_droites = set()
        # Règles à traiter pour supprimer les unités
        a_traiter = set([gauche])  # On commence par le non-terminal lui-même

        while a_traiter:
            courant = a_traiter.pop()  # Traiter un non-terminal
            for droite in grammaire.regles.get(courant, []):
                if len(droite) == 1 and droite.isupper():  # Si c'est une règle unitaire
                    if droite not in nouvelles_droites:
                        a_traiter.add(droite)  # Ajouter pour traitement
                else:
                    nouvelles_droites.add(droite)  # Ajouter les productions finales

        # Une fois terminé, mettre à jour les règles pour ce non-terminal
        nouvelles_regles[gauche] = list(nouvelles_droites)

    # Mettre à jour la grammaire
    grammaire.regles = nouvelles_regles


# 4. supprimer les non-terminaux en tête des règles 
def supprimer_non_terminaux_tete(grammaire):
    nouvelles_regles = {}

    for gauche, droites in grammaire.regles.items():
        nouvelles_droites = []
        for droite in droites:
            # Vérifier si la règle est vide
            if not droite:  # Règle vide (epsilon)
                nouvelles_droites.append("")  # Conserver epsilon
                continue

            # Si la règle commence par un non-terminal
            if droite[0].isupper():
                non_terminal = droite[0]
                # Remplacer par les productions du non-terminal
                for remplacement in grammaire.regles.get(non_terminal, []):
                    nouvelles_droites.append(remplacement + droite[1:])
            else:
                # Conserver les règles qui commencent par un terminal
                nouvelles_droites.append(droite)
        # Ajouter les nouvelles règles pour le non-terminal actuel
        nouvelles_regles[gauche] = list(set(nouvelles_droites))  # Éliminer les doublons

    # Mettre à jour les règles de la grammaire
    grammaire.regles = nouvelles_regles

# 5. supprimer les symboles terminaux qui ne sont pas en tête des règles.
def supprimer_terminaux_mixtes(grammaire):
    """
    Remplace les terminaux qui ne sont pas en tête des règles par des non-terminaux.
    Les règles de longueur 1 contenant un terminal restent inchangées.
    """
    existants = set(grammaire.regles.keys())  # Ensemble des non-terminaux existants
    nouvelles_regles = {}
    remplacements = {}  # Associe chaque terminal à un nouveau non-terminal unique

    for gauche, droites in grammaire.regles.items():
        nouvelles_droites = []
        for droite in droites:
            # Si la règle est un terminal seul ou vide, on la conserve
            if len(droite) == 1 and droite.islower():
                nouvelles_droites.append(droite)
                continue

            nouvelle_droite = []
            for i, char in enumerate(droite):
                # On ne remplace que les terminaux après le premier symbole
                if i > 0 and char.islower():
                    if char not in remplacements:
                        # Générer un nouveau non-terminal pour ce terminal
                        nouveau_non_terminal = generer_non_terminal(existants)
                        existants.add(nouveau_non_terminal)
                        remplacements[char] = nouveau_non_terminal
                        # Ajouter une règle associant le nouveau non-terminal au terminal
                        nouvelles_regles.setdefault(nouveau_non_terminal, []).append(char)
                    nouvelle_droite.append(remplacements[char])
                else:
                    # Conserver le symbole tel quel (premier caractère ou non-terminal)
                    nouvelle_droite.append(char)

            # Ajouter la règle modifiée
            nouvelles_droites.append("".join(nouvelle_droite))

        # Ajouter les nouvelles règles pour le non-terminal actuel
        nouvelles_regles[gauche] = list(set(nouvelles_droites))  # Éliminer les doublons

    # Mettre à jour les règles de la grammaire
    grammaire.regles.update(nouvelles_regles)


def greibach(grammaire):
    axiome = list(grammaire.regles.keys())[0]  # Le premier non-terminal dans les clés
    retirer_axiome(grammaire, axiome)
    supprimer_epsilon(grammaire, axiome)
    supprimer_unites(grammaire)
    supprimer_non_terminaux_tete(grammaire)
    supprimer_terminaux_mixtes(grammaire)
    return grammaire