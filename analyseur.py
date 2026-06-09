"""MINI-XL v2.0 - Analyseur de fichiers tabulaires."""

import json
import logging
from pathlib import Path
from typing import Optional

from utils import SEPARATEURS_TESTES


class ResultatAnalyse:
    """Résultat de l'analyse d'un fichier."""
    def __init__(
        self, type_detecte: str,
        en_tetes: list[str], donnees: list[list[str]],
        separateur: Optional[str] = None,
    ) -> None:
        self.type_detecte = type_detecte
        self.en_tetes = en_tetes
        self.donnees = donnees
        self.separateur = separateur


def analyser_fichier(
    chemin: Path, logger: Optional[logging.Logger] = None,
) -> ResultatAnalyse:
    """Analyse un fichier et retourne sa structure tabulaire."""
    ext = chemin.suffix.lower()
    if ext == ".json":
        return _analyser_json(chemin, logger)
    if ext == ".tsv":
        return _analyser_delimite(chemin, "\t", logger)
    if ext == ".csv":
        return _analyser_csv_auto(chemin, logger)
    return _analyser_txt(chemin, logger)


def _analyser_json(
    chemin: Path, logger: Optional[logging.Logger] = None,
) -> ResultatAnalyse:
    """Analyse un fichier JSON tabulaire (tableau d'objets)."""
    try:
        contenu = chemin.read_text(encoding="utf-8")
    except OSError as e:
        raise ValueError(f"Lecture impossible : {e}") from e
    try:
        obj = json.loads(contenu)
    except json.JSONDecodeError as e:
        raise ValueError("Format JSON invalide") from e
    if not isinstance(obj, list):
        raise ValueError("JSON invalide : tableau d'objets attendu")
    if not obj:
        return ResultatAnalyse("json", [], [])
    if not isinstance(obj[0], dict):
        raise ValueError("JSON invalide : objets attendus dans le tableau")
    cles = _cles_json(obj)
    donnees = [[str(o.get(c, "")) for c in cles] for o in obj]
    _log(logger, f"JSON : {len(cles)} cols, {len(donnees)} lignes")
    return ResultatAnalyse("json", cles, donnees)


def _cles_json(objets: list[dict]) -> list[str]:
    """Extrait les clés uniques ordonnées d'un tableau d'objets."""
    cles: list[str] = []
    vues: set[str] = set()
    for obj in objets:
        for cle in obj.keys():
            if cle not in vues:
                cles.append(cle)
                vues.add(cle)
    return cles


def _analyser_csv_auto(
    chemin: Path, logger: Optional[logging.Logger] = None,
) -> ResultatAnalyse:
    """Analyse un CSV en détectant le séparateur."""
    return _analyser_delimite(chemin, _detecter_sep(chemin), logger)


def _analyser_txt(
    chemin: Path, logger: Optional[logging.Logger] = None,
) -> ResultatAnalyse:
    """Analyse un TXT en détectant sa structure tabulaire."""
    sep = _detecter_sep(chemin)
    if sep is None:
        raise ValueError("Format invalide : aucune structure tabulaire détectée")
    return _analyser_delimite(chemin, sep, logger)


def _detecter_sep(chemin: Path) -> Optional[str]:
    """Détecte le séparateur le plus cohérent (, ; \\t)."""
    try:
        lignes = _lire_premieres(chemin, 20)
    except OSError:
        return None
    if len(lignes) < 2:
        return None
    meilleur: Optional[str] = None
    top_score: float = 0.0
    for sep in SEPARATEURS_TESTES:
        s = _score(lignes, sep)
        if s > top_score:
            top_score = s
            meilleur = sep
    return meilleur if top_score > 0 else None


def _lire_premieres(chemin: Path, n: int) -> list[str]:
    """Lit les n premières lignes non vides."""
    lignes: list[str] = []
    with open(chemin, "r", encoding="utf-8", errors="replace") as f:
        for ligne in f:
            ligne = ligne.rstrip("\n\r")
            if ligne.strip():
                lignes.append(ligne)
            if len(lignes) >= n:
                break
    return lignes


def _score(lignes: list[str], sep: str) -> float:
    """Score de cohérence d'un séparateur (0-1)."""
    comptes = [len(l.split(sep)) for l in lignes]
    if not comptes or max(comptes) <= 1:
        return 0.0
    n = max(comptes)
    return sum(1 for c in comptes if c == n) / len(comptes)


def _analyser_delimite(
    chemin: Path, separateur: Optional[str],
    logger: Optional[logging.Logger] = None,
) -> ResultatAnalyse:
    """Analyse un fichier délimité générique."""
    lignes_brutes = _lire_tout(chemin)
    if not lignes_brutes:
        raise ValueError("Fichier vide")
    sep = separateur or ","
    lignes = [[c.strip() for c in l.split(sep)] for l in lignes_brutes]
    if not lignes:
        raise ValueError("Aucune donnée exploitable")
    type_fic = {",": "csv", ";": "csv_sc", "\t": "tsv"}.get(sep, "txt")
    _log(logger, f"{type_fic} : {len(lignes[0])} cols, {len(lignes)-1} lignes")
    return ResultatAnalyse(type_fic, lignes[0], lignes[1:], sep)


def _lire_tout(chemin: Path) -> list[str]:
    """Lit toutes les lignes non vides."""
    lignes: list[str] = []
    with open(chemin, "r", encoding="utf-8", errors="replace") as f:
        for ligne in f:
            ligne = ligne.rstrip("\n\r")
            if ligne.strip():
                lignes.append(ligne)
    return lignes


def detecter_en_tetes(
    en_tetes: list[str], donnees: list[list[str]],
) -> bool:
    """Heuristique : première ligne textuelle vs données mixtes/numériques."""
    if not en_tetes or not donnees:
        return bool(en_tetes)
    ratio_h = _ratio_text(en_tetes)
    ratios_d = [_ratio_text(l) for l in donnees[:5]]
    return ratio_h > sum(ratios_d) / len(ratios_d)


def _ratio_text(colonnes: list[str]) -> float:
    """Ratio de valeurs textuelles (non numériques) dans une ligne."""
    if not colonnes:
        return 0.0
    return sum(1 for v in colonnes if v.strip() and not _est_num(v)) / len(colonnes)


def _est_num(val: str) -> bool:
    """Vérifie si une chaîne représente un nombre."""
    try:
        float(val.replace(",", "."))
        return True
    except ValueError:
        return False


def _log(logger: Optional[logging.Logger], msg: str) -> None:
    """Log si le logger est disponible."""
    if logger:
        logger.debug(msg)
