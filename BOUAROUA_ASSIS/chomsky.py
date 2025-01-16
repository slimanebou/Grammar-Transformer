from commun import generer_non_terminal, retirer_axiome, supprimer_epsilon


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


# Remplace les règles contenant plus de deux non-terminaux par des règles binaires.
def remplacer_non_terminaux_longueur2(grammaire):
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


# Supprimer les règles unité 𝑋 → 𝑌.
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

    return (grammaire)
