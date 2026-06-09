#!/usr/bin/env python3
"""MINI-XL v2.0 - Point d'entrée principal."""

import sys
import logging
from pathlib import Path
from typing import Optional

from utils import (
    configurer_logging, journaliser, chemin_sortie,
    nettoyer_nom, resoudre_repertoire,
)
from scanner import scanner_repertoire, verifier_avertissement_taille
from menu import (
    afficher_menu, demander_choix,
    confirmer_en_tetes, afficher_aucun_fichier,
)
from analyseur import analyser_fichier, detecter_en_tetes
from generateur import generer_xlsx


def main() -> int:
    """Point d'entrée principal de MINI-XL."""
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
        journaliser(logger, choisi.nom, "succès")
        return 0
    journaliser(logger, choisi.nom, "échec")
    return 1


def _obtenir_repertoire(logger: logging.Logger) -> Optional[Path]:
    """Résout le répertoire de travail, le crée si nécessaire."""
    repertoire = resoudre_repertoire()
    if not repertoire.exists():
        print(f"\n  ⚠ Répertoire introuvable : {repertoire}")
        print("  Création du répertoire...\n")
        try:
            repertoire.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            _erreur(f"Impossible de créer le répertoire : {e}")
            logger.error(f"Répertoire inaccessible : {repertoire} - {e}")
            return None
    return repertoire


def _afficher_avertissements(
    fichiers: list, logger: logging.Logger,
) -> None:
    """Affiche les avertissements de taille de fichiers."""
    for msg in verifier_avertissement_taille(fichiers, logger):
        print(f"  ⚠ {msg}")


def _traiter_fichier(
    chemin: Path, repertoire: Path, logger: logging.Logger,
) -> bool:
    """Traite un fichier : analyse → validation → génération Excel."""
    try:
        resultat = analyser_fichier(chemin, logger)
    except ValueError as e:
        _erreur(str(e))
        return False
    except OSError as e:
        _erreur(f"Erreur de lecture : {e}")
        return False

    if not resultat.en_tetes:
        _erreur("Fichier vide ou sans données")
        return False

    en_tetes, donnees = _valider_en_tetes(resultat)
    nom_feuille = nettoyer_nom(chemin.stem)
    chemin_xlsx = chemin_sortie(repertoire, chemin.name)

    try:
        generer_xlsx(en_tetes, donnees, chemin_xlsx, nom_feuille, logger)
    except (ValueError, OSError) as e:
        _erreur(f"Erreur de génération : {e}")
        return False

    _succes(chemin_xlsx)
    return True


def _valider_en_tetes(
    resultat: object,
) -> tuple[list[str], list[list[str]]]:
    """Valide et confirme les en-têtes si nécessaire."""
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
    """Affiche un message d'erreur."""
    print(f"\n  ✗ {message}\n")


def _succes(chemin: Path) -> None:
    """Affiche le message de succès avec le chemin du fichier."""
    print("\n  ✔ Conversion réussie !")
    print(f"  📄 Fichier : {chemin}\n")


if __name__ == "__main__":
    try:
        code = main()
    except KeyboardInterrupt:
        print("\n\n  Opération interrompue.")
        code = 1
    except Exception as e:
        logging.getLogger("mini-xl").critical(
            f"Erreur inattendue : {e}", exc_info=True
        )
        print(f"\n  ✗ Erreur inattendue : {e}")
        print("  Consultez le journal pour plus de détails.\n")
        code = 1
    sys.exit(code)
