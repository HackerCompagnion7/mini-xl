"""MINI-XL v2.0 - Main entry point."""

import sys
import logging
from pathlib import Path
from typing import Optional

from mini_xl.utils import (
    configurer_logging, journaliser, chemin_sortie,
    nettoyer_nom, resoudre_repertoire,
)
from mini_xl.scanner import scanner_repertoire, verifier_avertissement_taille
from mini_xl.menu import (
    afficher_menu, demander_choix,
    confirmer_en_tetes, afficher_aucun_fichier,
)
from mini_xl.analyseur import analyser_fichier, detecter_en_tetes
from mini_xl.generateur import generer_xlsx


def main() -> int:
    """Main entry point for MINI-XL."""
    logger = configurer_logging()
    repertoire = _obtenir_repertoire(logger)
    if repertoire is None:
        return 1

    fichiers = scanner_repertoire(str(repertoire), logger)
    if not fichiers:
        afficher_aucun_fichier()
        return 1

    _afficher_avertissements(fichiers, logger)
    afficher_menu(fichiers)
    choisi = demander_choix(fichiers, logger)
    if choisi is None:
        return 0

    resultat = _traiter_fichier(choisi.chemin, repertoire, logger)
    if resultat:
        journaliser(logger, choisi.nom, "success")
        return 0
    journaliser(logger, choisi.nom, "failure")
    return 1


def _obtenir_repertoire(logger: logging.Logger) -> Optional[Path]:
    """Resolve working directory, create if needed."""
    repertoire = resoudre_repertoire()
    if not repertoire.exists():
        print(f"\n  Directory not found: {repertoire}")
        print("  Creating directory...\n")
        try:
            repertoire.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            _erreur(f"Cannot create directory: {e}")
            logger.error(f"Directory inaccessible: {repertoire} - {e}")
            return None
    return repertoire


def _afficher_avertissements(
    fichiers: list, logger: logging.Logger,
) -> None:
    """Display file size warnings."""
    for msg in verifier_avertissement_taille(fichiers, logger):
        print(f"  {msg}")


def _traiter_fichier(
    chemin: Path, repertoire: Path, logger: logging.Logger,
) -> bool:
    """Process a file: analyze → validate → generate Excel."""
    try:
        resultat = analyser_fichier(chemin, logger)
    except ValueError as e:
        _erreur(str(e))
        return False
    except OSError as e:
        _erreur(f"Read error: {e}")
        return False

    if not resultat.en_tetes:
        _erreur("Empty file or no data")
        return False

    en_tetes, donnees = _valider_en_tetes(resultat)
    nom_feuille = nettoyer_nom(chemin.stem)
    chemin_xlsx = chemin_sortie(repertoire, chemin.name)

    try:
        generer_xlsx(en_tetes, donnees, chemin_xlsx, nom_feuille, logger)
    except (ValueError, OSError) as e:
        _erreur(f"Generation error: {e}")
        return False

    _succes(chemin_xlsx)
    return True


def _valider_en_tetes(
    resultat: object,
) -> tuple[list[str], list[list[str]]]:
    """Validate and confirm headers if necessary."""
    en_tetes = resultat.en_tetes
    donnees = resultat.donnees
    probable = detecter_en_tetes(en_tetes, donnees)

    if not probable:
        confirme = confirmer_en_tetes(probable)
        if not confirme:
            nb_cols = len(donnees[0]) if donnees else len(en_tetes)
            en_tetes = [f"Col_{i}" for i in range(1, nb_cols + 1)]
            if resultat.en_tetes:
                donnees = [resultat.en_tetes] + donnees

    return en_tetes, donnees


def _erreur(message: str) -> None:
    """Display an error message."""
    print(f"\n  {message}\n")


def _succes(chemin: Path) -> None:
    """Display success message with file path."""
    print("\n  Conversion successful!")
    print(f"  File: {chemin}\n")
