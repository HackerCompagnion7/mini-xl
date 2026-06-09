"""MINI-XL v2.0 - Scanner de fichiers.

Scanne un répertoire et détecte les fichiers tabulaires compatibles.
"""

import logging
from pathlib import Path
from typing import Optional

from utils import (
    est_extension_compatible,
    fichier_est_vide,
    verifier_taille_fichier,
    resoudre_repertoire,
)


# ------------------------------------------------------------------ #
#  Structure de résultat
# ------------------------------------------------------------------ #

class FichierInfo:
    """Informations sur un fichier compatible détecté."""

    def __init__(self, chemin: Path, taille_mo: float, vide: bool) -> None:
        self.chemin: Path = chemin
        self.nom: str = chemin.name
        self.extension: str = chemin.suffix.lower()
        self.taille_mo: float = taille_mo
        self.vide: bool = vide

    def affichage(self) -> str:
        """Retourne la représentation pour le menu."""
        etat = " (vide)" if self.vide else f" ({self.taille_mo:.2f} MB)"
        return f"{self.nom}{etat}"


# ------------------------------------------------------------------ #
#  Scan du répertoire
# ------------------------------------------------------------------ #

def scanner_repertoire(
    repertoire: Optional[str] = None,
    logger: Optional[logging.Logger] = None,
) -> list[FichierInfo]:
    """Scanne le répertoire et retourne les fichiers compatibles.

    Args:
        repertoire: Chemin du répertoire. Par défaut ~/storage/downloads.
        logger: Logger optionnel.

    Returns:
        Liste triée de FichierInfo pour les fichiers compatibles.
    """
    rep = resoudre_repertoire(repertoire)
    fichiers: list[FichierInfo] = []

    if not rep.exists():
        _log(logger, f"Répertoire introuvable : {rep}")
        return fichiers

    if not rep.is_dir():
        _log(logger, f"Ce n'est pas un répertoire : {rep}")
        return fichiers

    try:
        entrees = list(rep.iterdir())
    except PermissionError:
        _log(logger, f"Permission refusée : {rep}")
        return fichiers

    for entree in entrees:
        if not entree.is_file():
            continue
        if not est_extension_compatible(entree):
            continue

        info = _creer_fichier_info(entree)
        fichiers.append(info)

    fichiers.sort(key=lambda f: f.nom.lower())
    _log(logger, f"{len(fichiers)} fichier(s) compatible(s) trouvé(s)")
    return fichiers


def _creer_fichier_info(chemin: Path) -> FichierInfo:
    """Crée un objet FichierInfo à partir d'un chemin.

    Args:
        chemin: Chemin vers le fichier.

    Returns:
        Instance de FichierInfo.
    """
    try:
        taille_mo = chemin.stat().st_size / (1024 * 1024)
    except OSError:
        taille_mo = 0.0

    vide = fichier_est_vide(chemin)
    return FichierInfo(chemin=chemin, taille_mo=taille_mo, vide=vide)


# ------------------------------------------------------------------ #
#  Avertissement taille
# ------------------------------------------------------------------ #

def verifier_avertissement_taille(
    fichiers: list[FichierInfo],
    logger: Optional[logging.Logger] = None,
) -> list[str]:
    """Vérifie les fichiers dépassant la limite recommandée.

    Args:
        fichiers: Liste des fichiers à vérifier.
        logger: Logger optionnel.

    Returns:
        Liste des messages d'avertissement.
    """
    avertissements: list[str] = []

    for f in fichiers:
        msg = verifier_taille_fichier(f.chemin)
        if msg:
            avertissements.append(f"{f.nom} : {msg}")
            _log(logger, msg)

    return avertissements


# ------------------------------------------------------------------ #
#  Utilitaire interne
# ------------------------------------------------------------------ #

def _log(
    logger: Optional[logging.Logger], message: str
) -> None:
    """Log un message si le logger est disponible.

    Args:
        logger: Logger optionnel.
        message: Message à journaliser.
    """
    if logger:
        logger.debug(message)
