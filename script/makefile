# Par défaut, exécuter toutes les étapes pour tous les fichiers
all: run_grammaire run_generer

# Exécute le programme principal pour chaque fichier
run_grammaire:
	@echo "Execution de grammaire.py pour tous les fichiers"
	python grammaire.py exemple1.general || exit 1;
	python grammaire.py exemple2.general || exit 1;
	python grammaire.py exemple3.general || exit 1;
	python grammaire.py exemple4.general || exit 1;
	python grammaire.py exemple5.general || exit 1;

# Génération des mots
run_generer:
	@echo "Generation des mots à partir des fichiers"
	python generer.py exemple1.greibach 3 || exit 1;
	python generer.py exemple1.chomsky 3 || exit 1;
	python generer.py exemple2.greibach 3 || exit 1;
	python generer.py exemple2.chomsky 3 || exit 1;
	python generer.py exemple3.greibach 3 || exit 1;
	python generer.py exemple3.chomsky 3 || exit 1;
	python generer.py exemple4.greibach 3 || exit 1;
	python generer.py exemple4.chomsky 3 || exit 1;
	python generer.py exemple5.greibach 3 || exit 1;
	python generer.py exemple5.chomsky 3 || exit 1;
	