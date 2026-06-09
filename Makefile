# MINI-XL v2.0 — Makefile
# Installable Python Package

.PHONY: help install run test lint clean check compile build upload setup

# ------------------------------------------------------------------ #
#  Help
# ------------------------------------------------------------------ #

help: ## Show all available commands
	@echo ""
	@echo "  MINI-XL v2.0 — Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "    \033[36m%-12s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ------------------------------------------------------------------ #
#  Installation
# ------------------------------------------------------------------ #

install: ## Install mini-xl package (pip)
	pip install .

install-dev: ## Install in editable/development mode
	pip install -e .

install-termux: ## Install on Termux (Android)
	pip install .

install-github: ## Install directly from GitHub
	pip install git+https://github.com/HackerCompagnion7/mini-xl.git

# ------------------------------------------------------------------ #
#  Execution
# ------------------------------------------------------------------ #

run: ## Launch MINI-XL
	mini-xl

run-python: ## Launch via python -m
	python3 -m mini_xl

# ------------------------------------------------------------------ #
#  Validation
# ------------------------------------------------------------------ #

compile: ## Verify all modules compile
	@echo "  Checking compilation..."
	@python3 -m py_compile src/mini_xl/utils.py && echo "    PASS utils.py"
	@python3 -m py_compile src/mini_xl/scanner.py && echo "    PASS scanner.py"
	@python3 -m py_compile src/mini_xl/menu.py && echo "    PASS menu.py"
	@python3 -m py_compile src/mini_xl/analyseur.py && echo "    PASS analyseur.py"
	@python3 -m py_compile src/mini_xl/generateur.py && echo "    PASS generateur.py"
	@python3 -m py_compile src/mini_xl/main.py && echo "    PASS main.py"
	@echo "  Compilation OK"

lint: ## Static analysis
	@python3 -m pyflakes src/mini_xl/*.py 2>&1 || \
		echo "  (pyflakes not installed — pip install pyflakes)"

test: ## Run the test suite
	python3 tests/test_mini_xl.py

check: compile lint test ## Full verification (compile + lint + test)

# ------------------------------------------------------------------ #
#  Build & Distribution
# ------------------------------------------------------------------ #

build: ## Build wheel and source distribution
	python3 -m build

upload: ## Upload to PyPI (requires twine)
	twine upload dist/*

clean-dist: ## Remove built distributions
	rm -rf dist/ build/ *.egg-info src/*.egg-info

# ------------------------------------------------------------------ #
#  Setup
# ------------------------------------------------------------------ #

setup: install-dev compile ## Full setup (install + verify)
	@echo ""
	@echo "  MINI-XL ready! Run: mini-xl"
	@echo ""

# ------------------------------------------------------------------ #
#  Cleanup
# ------------------------------------------------------------------ #

clean: ## Remove cache and temporary files
	@rm -rf __pycache__ *.pyc src/mini_xl/__pycache__
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "  Clean OK"

# ------------------------------------------------------------------ #
#  Info
# ------------------------------------------------------------------ #

info: ## Display project info
	@echo ""
	@echo "  MINI-XL v2.0"
	@echo "  ─────────────"
	@echo "  Python : $$(python3 --version)"
	@echo "  openpyxl : $$(python3 -c 'import openpyxl; print(openpyxl.__version__)' 2>/dev/null || echo 'not installed')"
	@echo "  Package : $$(pip show mini-xl 2>/dev/null | grep Version || echo 'not installed')"
	@echo "  CLI     : $$(which mini-xl 2>/dev/null || echo 'not on PATH')"
	@echo ""
