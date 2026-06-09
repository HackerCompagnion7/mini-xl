"""MINI-XL v2.0 - File scanner.

Scans a directory and detects compatible tabular files.
"""

import logging
from pathlib import Path
from typing import Optional

from mini_xl.utils import (
    est_extension_compatible,
    fichier_est_vide,
    verifier_taille_fichier,
    resoudre_repertoire,
)


class FichierInfo:
    """Information about a detected compatible file."""

    def __init__(self, chemin: Path, taille_mo: float, vide: bool) -> None:
        self.chemin: Path = chemin
        self.nom: str = chemin.name
        self.extension: str = chemin.suffix.lower()
        self.taille_mo: float = taille_mo
        self.vide: bool = vide

    def affichage(self) -> str:
        """Return the display representation for the menu."""
        etat = " (empty)" if self.vide else f" ({self.taille_mo:.2f} MB)"
        return f"{self.nom}{etat}"


def scanner_repertoire(
    repertoire: Optional[str] = None,
    logger: Optional[logging.Logger] = None,
) -> list[FichierInfo]:
    """Scan directory and return compatible files sorted by name."""
    rep = resoudre_repertoire(repertoire)
    fichiers: list[FichierInfo] = []

    if not rep.exists():
        _log(logger, f"Directory not found: {rep}")
        return fichiers

    if not rep.is_dir():
        _log(logger, f"Not a directory: {rep}")
        return fichiers

    try:
        entrees = list(rep.iterdir())
    except PermissionError:
        _log(logger, f"Permission denied: {rep}")
        return fichiers

    for entree in entrees:
        if not entree.is_file():
            continue
        if not est_extension_compatible(entree):
            continue
        info = _creer_fichier_info(entree)
        fichiers.append(info)

    fichiers.sort(key=lambda f: f.nom.lower())
    _log(logger, f"{len(fichiers)} compatible file(s) found")
    return fichiers


def _creer_fichier_info(chemin: Path) -> FichierInfo:
    """Create a FichierInfo from a file path."""
    try:
        taille_mo = chemin.stat().st_size / (1024 * 1024)
    except OSError:
        taille_mo = 0.0
    vide = fichier_est_vide(chemin)
    return FichierInfo(chemin=chemin, taille_mo=taille_mo, vide=vide)


def verifier_avertissement_taille(
    fichiers: list[FichierInfo],
    logger: Optional[logging.Logger] = None,
) -> list[str]:
    """Check files exceeding the recommended size limit."""
    avertissements: list[str] = []
    for f in fichiers:
        msg = verifier_taille_fichier(f.chemin)
        if msg:
            avertissements.append(f"{f.nom} : {msg}")
            _log(logger, msg)
    return avertissements


def _log(
    logger: Optional[logging.Logger], message: str,
) -> None:
    """Log a message if logger is available."""
    if logger:
        logger.debug(message)
