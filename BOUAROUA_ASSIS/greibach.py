from commun import generer_non_terminal, retirer_axiome, supprimer_epsilon


# Supprimer les règles unité 𝑋 → 𝑌
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


# Supprimer les non-terminaux en tête des règles
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


# Supprimer les symboles terminaux qui ne sont pas en tête des règles.
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
    return (grammaire)
