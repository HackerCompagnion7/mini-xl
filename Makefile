# MINI-XL v2.0 — Makefile
# Utilitaire CLI : tabulaire → Excel

.PHONY: help install run test lint clean check compile

# ------------------------------------------------------------------ #
#  Aide
# ------------------------------------------------------------------ #

help: ## Affiche cette aide
	@echo ""
	@echo "  MINI-XL v2.0 — Commandes disponibles :"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "    \033[36m%-12s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ------------------------------------------------------------------ #
#  Installation
# ------------------------------------------------------------------ #

install: ## Installe les dépendances (openpyxl)
	pip install openpyxl

install-termux: ## Installe les dépendances sur Termux
	pip install openpyxl

# ------------------------------------------------------------------ #
#  Exécution
# ------------------------------------------------------------------ #

run: ## Lance MINI-XL (scan ~/storage/downloads)
	python3 main.py

run-dir: ## Lance MINI-XL sur un répertoire personnalisé
	@read -p "  Répertoire : " dir; \
	python3 -c "from main import main; import sys; sys.argv=['mini-xl','$(dir)']; main()"

# ------------------------------------------------------------------ #
#  Validation
# ------------------------------------------------------------------ #

compile: ## Vérifie la compilation de tous les modules
	@echo "  Vérification compilation..."
	@python3 -m py_compile utils.py && echo "    ✔ utils.py"
	@python3 -m py_compile scanner.py && echo "    ✔ scanner.py"
	@python3 -m py_compile menu.py && echo "    ✔ menu.py"
	@python3 -m py_compile analyseur.py && echo "    ✔ analyseur.py"
	@python3 -m py_compile generateur.py && echo "    ✔ generateur.py"
	@python3 -m py_compile main.py && echo "    ✔ main.py"
	@echo "  Compilation OK ✔"

lint: ## Vérifie le style et les erreurs (pyflakes)
	@echo "  Analyse statique..."
	@python3 -m pyflakes utils.py scanner.py menu.py analyseur.py generateur.py main.py 2>&1 || \
		echo "  (pyflakes non installé — pip install pyflakes)"
	@echo "  Lint terminé."

test: ## Lance la suite de tests
	@echo "  Lancement des tests..."
	@python3 test_mini_xl.py

# ------------------------------------------------------------------ #
#  Vérification complète
# ------------------------------------------------------------------ #

check: compile lint test ## Vérification complète (compile + lint + test)

# ------------------------------------------------------------------ #
#  Nettoyage
# ------------------------------------------------------------------ #

clean: ## Supprime les fichiers temporaires et cache
	@echo "  Nettoyage..."
	@rm -rf __pycache__ *.pyc
	@rm -f mini-xl.log
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "  Nettoyage OK ✔"

# ------------------------------------------------------------------ #
#  Info
# ------------------------------------------------------------------ #

info: ## Affiche les informations du projet
	@echo ""
	@echo "  MINI-XL v2.0"
	@echo "  ─────────────"
	@echo "  Python : $$(python3 --version)"
	@echo "  openpyxl : $$(python3 -c 'import openpyxl; print(openpyxl.__version__)' 2>/dev/null || echo 'non installé')"
	@echo "  Modules :"
	@for f in utils.py scanner.py menu.py analyseur.py generateur.py main.py; do \
		echo "    $$f ($$(wc -l < $$f) lignes)"; \
	done
	@echo ""

# ------------------------------------------------------------------ #
#  Raccourci installation complète
# ------------------------------------------------------------------ #

setup: install compile ## Installation complète (deps + vérification)
	@echo ""
	@echo "  ✔ MINI-XL prêt ! Lancez : make run"
	@echo ""
