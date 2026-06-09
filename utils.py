"""MINI-XL v2.0 - Utilitaires partagés."""

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
    """Horodatage compact : AAAAMMJJ_HHMMSS."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def horodatage_lisible() -> str:
    """Horodatage lisible pour les logs."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def nettoyer_nom(nom: str) -> str:
    """Nettoie un nom de fichier : espaces → _, car. spéciaux supprimés."""
    nom = nom.replace(" ", "_")
    nom = re.sub(r"[^A-Za-z0-9_\-]", "", nom)
    nom = re.sub(r"_+", "_", nom)
    nom = nom.strip("_")
    return nom if nom else "sans_nom"


def generer_nom_xlsx(nom_source: str) -> str:
    """Génère le nom Excel : rapport_ventes_20260608_154530.xlsx."""
    base = Path(nom_source).stem
    base_propre = nettoyer_nom(base)
    return f"{base_propre}_{horodatage()}.xlsx"


def est_extension_compatible(chemin: Path) -> bool:
    """Vérifie si l'extension est supportée."""
    return chemin.suffix.lower() in EXTENSIONS_COMPATIBLES


def verifier_taille_fichier(chemin: Path) -> Optional[str]:
    """Retourne un avertissement si > 100 MB, None sinon."""
    try:
        taille_mo = chemin.stat().st_size / (1024 * 1024)
    except OSError:
        return "Impossible de lire la taille du fichier."
    if taille_mo > TAILLE_LIMITE_MO:
        return f"Avertissement : {taille_mo:.1f} MB (limite {TAILLE_LIMITE_MO} MB)"
    return None


def fichier_est_vide(chemin: Path) -> bool:
    """Vérifie si un fichier est vide (0 octet)."""
    try:
        return chemin.stat().st_size == 0
    except OSError:
        return True


def resoudre_repertoire(repertoire: Optional[str] = None) -> Path:
    """Résout le répertoire de travail (défaut : ~/storage/downloads)."""
    if repertoire:
        return Path(repertoire).expanduser().resolve()
    return Path(REP_DOWNLOADS).expanduser().resolve()


def chemin_sortie(repertoire: Path, nom_source: str) -> Path:
    """Construit le chemin complet du fichier Excel de sortie."""
    return repertoire / generer_nom_xlsx(nom_source)


def configurer_logging() -> logging.Logger:
    """Configure et retourne le logger MINI-XL."""
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
    """Enregistre une entrée dans le journal."""
    msg = f"Fichier: {fichier} | Résultat: {resultat}"
    if erreur:
        msg += f" | Erreur: {erreur}"
        logger.error(msg)
    else:
        logger.info(msg)
