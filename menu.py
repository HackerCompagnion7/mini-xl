"""MINI-XL v2.0 - Menu interactif.

Affiche la liste des fichiers et gère la sélection utilisateur.
"""

import logging
from typing import Optional

from scanner import FichierInfo


# ------------------------------------------------------------------ #
#  Affichage du menu
# ------------------------------------------------------------------ #

def afficher_menu(fichiers: list[FichierInfo]) -> None:
    """Affiche la liste numérotée des fichiers compatibles.

    Args:
        fichiers: Liste des fichiers détectés.
    """
    print("\n" + "=" * 50)
    print("  MINI-XL v2.0 — Convertisseur tabulaire → Excel")
    print("=" * 50)
    print(f"\n  {len(fichiers)} fichier(s) compatible(s) trouvé(s) :\n")

    for i, f in enumerate(fichiers, start=1):
        print(f"  [{i}]  {f.affichage()}")

    print(f"\n  [0]  Quitter")
    print()


# ------------------------------------------------------------------ #
#  Sélection utilisateur
# ------------------------------------------------------------------ #

def demander_choix(
    fichiers: list[FichierInfo],
    logger: Optional[logging.Logger] = None,
) -> Optional[FichierInfo]:
    """Demande à l'utilisateur de choisir un fichier.

    Args:
        fichiers: Liste des fichiers disponibles.
        logger: Logger optionnel.

    Returns:
        FichierInfo sélectionné, ou None si l'utilisateur quitte.
    """
    max_idx = len(fichiers)

    while True:
        try:
            saisie = input("  Votre choix : ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Opération annulée.")
            return None

        if saisie == "0":
            print("  Au revoir !")
            return None

        if not saisie.isdigit():
            print("  ⚠ Veuillez entrer un nombre.")
            continue

        idx = int(saisie)
        if idx < 1 or idx > max_idx:
            print(f"  ⚠ Choix invalide (1-{max_idx}).")
            continue

        choisi = fichiers[idx - 1]

        if choisi.vide:
            print("  ⚠ Ce fichier est vide. Choisissez-en un autre.")
            continue

        if logger:
            logger.info(f"Fichier sélectionné : {choisi.nom}")

        return choisi


# ------------------------------------------------------------------ #
#  Confirmation en-têtes
# ------------------------------------------------------------------ #

def confirmer_en_tetes(en_tetes_detectes: bool) -> bool:
    """Demande confirmation si la détection des en-têtes est incertaine.

    Args:
        en_tetes_detectes: Résultat de l'heuristique de détection.

    Returns:
        True si on utilise la première ligne comme en-têtes.
    """
    etiquette = "OUI" if en_tetes_detectes else "NON"
    print(f"\n  En-têtes détectés : {etiquette}")

    while True:
        try:
            saisie = input("  Confirmer ? (o/n) : ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n  Opération annulée.")
            return en_tetes_detectes

        if saisie in ("o", "oui", "y", "yes"):
            return True
        if saisie in ("n", "non", "no"):
            return False

        print("  ⚠ Répondez par 'o' ou 'n'.")


# ------------------------------------------------------------------ #
#  Message d'erreur dossier vide
# ------------------------------------------------------------------ #

def afficher_aucun_fichier() -> None:
    """Affiche le message quand aucun fichier compatible n'est trouvé."""
    print("\n  Aucun fichier compatible trouvé.")
    print("  Formats supportés : CSV, TSV, JSON, TXT\n")
