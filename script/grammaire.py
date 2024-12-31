#!/usr/bin/env python3
import sys
import os
from chomsky import chomsky
from greibach import greibach

class Grammaire:
    def __init__(self):
        self.regles = {}  # Dictionnaire pour stocker les règles : {non_terminal: [productions]}

    def ajouter_regle(self, gauche, droite):

        gauche = gauche.strip()
        droite = [d.strip() if d.strip() != "E" else "" for d in droite.split('|')]
        if gauche not in self.regles:
            self.regles[gauche] = []
        self.regles[gauche].extend(droite)

    def __str__(self):
        
        return '\n'.join(
            f"{gauche} : {' | '.join(d if d != '' else 'E' for d in droites)}"
            for gauche, droites in self.regles.items()
        )

def lire(fichier):
    grammaire = Grammaire()
    with open(fichier, 'r') as f:
        for ligne in f:
            if ':' in ligne:
                gauche, droite = ligne.split(':', 1)
                grammaire.ajouter_regle(gauche, droite)
    return grammaire

def ecrire(grammaire, fichier):
    with open(fichier, 'w') as f:
        f.write(str(grammaire))


def main():
    if len(sys.argv) != 2:
        print("Usage : grammaire <nom_fichier.general>")
        sys.exit(1)

    fichier_entree = sys.argv[1]

    # Vérifie si le fichier existe
    if not os.path.exists(fichier_entree):
        print(f"Erreur : Le fichier '{fichier_entree}' n'existe pas.")
        sys.exit(1)


    # Lire la grammaire depuis le fichier
    grammaire1 = lire(fichier_entree)
    grammaire2 = lire(fichier_entree)

    # Transformation en forme normale de Chomsky
    grammaire_chomsky = chomsky(grammaire1)
    ecrire(grammaire_chomsky, fichier_entree.replace(".general", ".chomsky"))

    # Transformation en forme normale de Greibach
    grammaire_greibach = greibach(grammaire2)
    ecrire(grammaire_greibach, fichier_entree.replace(".general", ".greibach"))

if __name__ == "__main__":
    main()
