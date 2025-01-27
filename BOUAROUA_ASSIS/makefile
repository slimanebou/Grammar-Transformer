# Variables
PYTHON = python3
GRAMMAIRE_SCRIPT = grammaire.py
GENERER_SCRIPT = generer.py
EXEMPLES = exemple1 exemple2 exemple3 exemple4 exemple5
OUTPUT_DIR = ./output
GENERER_MODES = greibach chomsky
LENGTH = 3  # Valeur par défaut pour la longueur

# Si une longueur est spécifiée en ligne de commande, elle sera utilisée
ifeq ($(origin length), command line)
    LENGTH = $(length)
endif

# Par défaut, affiche les options disponibles
all:
	@echo "Transformation des fichiers avec $(GRAMMAIRE_SCRIPT)"
	@for exemple in $(EXEMPLES); do \
		echo "Processing $$exemple.general"; \
		$(PYTHON) $(GRAMMAIRE_SCRIPT) $$exemple.general || exit 1; \
	done

# Génération des mots (équivalent à run_generer)
generate:
	@echo "Génération des mots avec $(GENERER_SCRIPT), longueur = $(LENGTH)"
	@for exemple in $(EXEMPLES); do \
		for mode in $(GENERER_MODES); do \
			echo "Generating words for $$exemple.$$mode with length $(LENGTH)"; \
			$(PYTHON) $(GENERER_SCRIPT) $(OUTPUT_DIR)/$$exemple.$$mode $(LENGTH) || exit 1; \
		done \
	done

# Nettoyage des fichiers générés
clean:
	@echo "Nettoyage des fichiers générés dans $(OUTPUT_DIR)"
	@rm -rf $(OUTPUT_DIR)

.PHONY: all transform generate clean
