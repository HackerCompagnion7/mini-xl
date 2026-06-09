"""MINI-XL v2.0 - Shared utilities."""

import re
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

EXTENSIONS_COMPATIBLES: tuple[str, ...] = (".csv", ".tsv", ".json", ".txt")
SEPARATEURS_TESTES: tuple[str, ...] = (",", ";", "\t")
TAILLE_LIMITE_MO: int = 100
REP_DOWNLOADS: str = str(Path.home() / "storage" / "downloads")
FICHIER_LOG: str = str(Path.home() / "storage" / "downloads" / "mini-xl.log")


def horodatage() -> str:
    """Compact timestamp: YYYYMMDD_HHMMSS."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def horodatage_lisible() -> str:
    """Human-readable timestamp for logs."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def nettoyer_nom(nom: str) -> str:
    """Clean filename: spaces → _, special chars removed."""
    nom = nom.replace(" ", "_")
    nom = re.sub(r"[^A-Za-z0-9_\-]", "", nom)
    nom = re.sub(r"_+", "_", nom)
    nom = nom.strip("_")
    return nom if nom else "sans_nom"


def generer_nom_xlsx(nom_source: str) -> str:
    """Generate Excel filename: rapport_ventes_20260608_154530.xlsx."""
    base = Path(nom_source).stem
    base_propre = nettoyer_nom(base)
    return f"{base_propre}_{horodatage()}.xlsx"


def est_extension_compatible(chemin: Path) -> bool:
    """Check if the file extension is supported."""
    return chemin.suffix.lower() in EXTENSIONS_COMPATIBLES


def verifier_taille_fichier(chemin: Path) -> Optional[str]:
    """Return warning if file > 100 MB, None otherwise."""
    try:
        taille_mo = chemin.stat().st_size / (1024 * 1024)
    except OSError:
        return "Cannot read file size."
    if taille_mo > TAILLE_LIMITE_MO:
        return f"Warning: {taille_mo:.1f} MB (limit {TAILLE_LIMITE_MO} MB)"
    return None


def fichier_est_vide(chemin: Path) -> bool:
    """Check if a file is empty (0 bytes)."""
    try:
        return chemin.stat().st_size == 0
    except OSError:
        return True


def resoudre_repertoire(repertoire: Optional[str] = None) -> Path:
    """Resolve working directory (default: ~/storage/downloads)."""
    if repertoire:
        return Path(repertoire).expanduser().resolve()
    return Path(REP_DOWNLOADS).expanduser().resolve()


def chemin_sortie(repertoire: Path, nom_source: str) -> Path:
    """Build full path for the output Excel file."""
    return repertoire / generer_nom_xlsx(nom_source)


def configurer_logging() -> logging.Logger:
    """Configure and return the MINI-XL logger."""
    logger = logging.getLogger("mini-xl")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        try:
            handler = logging.FileHandler(FICHIER_LOG, encoding="utf-8")
            handler.setLevel(logging.DEBUG)
            fmt = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            handler.setFormatter(fmt)
            logger.addHandler(handler)
        except OSError:
            handler = logging.StreamHandler()
            handler.setLevel(logging.INFO)
            logger.addHandler(handler)
    return logger


def journaliser(
    logger: logging.Logger,
    fichier: str,
    resultat: str,
    erreur: Optional[str] = None,
) -> None:
    """Write an entry to the operation log."""
    msg = f"File: {fichier} | Result: {resultat}"
    if erreur:
        msg += f" | Error: {erreur}"
        logger.error(msg)
    else:
        logger.info(msg)
