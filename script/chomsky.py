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

# 1. retirer l’axiome des membres droits des règles 
def retirer_axiome(grammaire, axiome):
    existants = set(grammaire.regles.keys())
    nouveau_non_terminal = generer_non_terminal(existants)

    nouvelles_regles = []
    for droite in grammaire.regles[axiome]:
        if axiome in droite:
            nouvelles_regles.append(droite.replace(axiome, nouveau_non_terminal))
        else:
            nouvelles_regles.append(droite)

    grammaire.regles[nouveau_non_terminal] = nouvelles_regles
    grammaire.regles[axiome] = [nouveau_non_terminal]

def remplacer_terminaux_longueur2(grammaire):
    existants = set(grammaire.regles.keys())
    nouvelles_regles = {}
    remplacements = {}

    for gauche, droites in grammaire.regles.items():
        nouvelles_droites = []
        for droite in droites:
            # Si la règle est de longueur 1, on ne fait rien
            if len(droite) == 1 and droite.islower():
                nouvelles_droites.append(droite)
                continue

            # Sinon, on remplace les terminaux dans les règles de longueur >= 2
            nouvelle_droite = []
            for char in droite:
                if char.islower():  # Si c'est un terminal
                    if char not in remplacements:
                        # Créer un nouveau non-terminal pour ce terminal
                        nouveau_non_terminal = generer_non_terminal(existants)
                        existants.add(nouveau_non_terminal)
                        remplacements[char] = nouveau_non_terminal
                        nouvelles_regles[nouveau_non_terminal] = [char]  # N1 -> a
                    nouvelle_droite.append(remplacements[char])
                else:
                    nouvelle_droite.append(char)
            nouvelles_droites.append("".join(nouvelle_droite))

        nouvelles_regles[gauche] = nouvelles_droites

    # Ajouter les nouvelles règles pour les terminaux remplacés
    grammaire.regles.update(nouvelles_regles)

def remplacer_non_terminaux_longueur2(grammaire):
    """
    Remplace les règles contenant plus de deux non-terminaux par des règles binaires.
    :param grammaire: Instance de Grammaire.
    """
    existants = set(grammaire.regles.keys())
    nouvelles_regles = {}

    for gauche, droites in grammaire.regles.items():
        nouvelles_droites = []
        for droite in droites:
            # Tant que la règle contient plus de deux symboles
            while len(droite) > 2:
                # Créer un nouveau non-terminal pour les deux derniers symboles
                nouveau_non_terminal = generer_non_terminal(existants)
                existants.add(nouveau_non_terminal)

                # Garder le premier symbole et remplacer les deux suivants
                remplacement = droite[-2:]  # Les deux derniers symboles
                nouvelles_regles[nouveau_non_terminal] = [remplacement]

                # Construire la nouvelle règle
                droite = droite[:-2] + nouveau_non_terminal  # Conserver tout sauf les deux derniers symboles
            nouvelles_droites.append(droite)
        nouvelles_regles[gauche] = nouvelles_droites

    # Mettre à jour la grammaire avec les nouvelles règles binaires
    grammaire.regles.update(nouvelles_regles)

# 4. supprimer les règles 𝑋 → 𝜀 sauf si 𝑋 est l’axiome ;
from itertools import product

def generer_variantes_epsilon(droite, epsilon_produits):
    # Identifier les positions des non-terminaux epsilon-productifs dans la règle
    positions = [i for i, char in enumerate(droite) if char in epsilon_produits]

    # Si aucun epsilon-produit, retourne simplement la règle originale
    if not positions:
        return {droite}

    # Générer toutes les combinaisons de True (garder) ou False (supprimer) pour chaque position
    variantes = set()
    for combinaison in product([True, False], repeat=len(positions)):
        nouvelle_regle = list(droite)
        for i, garder in enumerate(combinaison):
            if not garder:
                # Supprime le caractère à cette position
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

# 5. supprimer les règles unité 𝑋 → 𝑌.
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

def chomsky(grammaire):
    axiome = list(grammaire.regles.keys())[0]  # Le premier non-terminal est l'axiome
    
    retirer_axiome(grammaire, axiome)
    remplacer_terminaux_longueur2(grammaire)
    remplacer_non_terminaux_longueur2(grammaire)
    supprimer_epsilon(grammaire, axiome)
    supprimer_unites(grammaire)

    return grammaire