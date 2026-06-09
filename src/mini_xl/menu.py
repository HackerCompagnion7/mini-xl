"""MINI-XL v2.0 - Interactive menu.

Displays the file list and handles user selection.
"""

import logging
from typing import Optional

from mini_xl.scanner import FichierInfo


def afficher_menu(fichiers: list[FichierInfo]) -> None:
    """Display the numbered list of compatible files."""
    print("\n" + "=" * 50)
    print("  MINI-XL v2.0 — Tabular → Excel Converter")
    print("=" * 50)
    print(f"\n  {len(fichiers)} compatible file(s) found:\n")

    for i, f in enumerate(fichiers, start=1):
        print(f"  [{i}]  {f.affichage()}")

    print(f"\n  [0]  Quit")
    print()


def demander_choix(
    fichiers: list[FichierInfo],
    logger: Optional[logging.Logger] = None,
) -> Optional[FichierInfo]:
    """Ask the user to choose a file from the list."""
    max_idx = len(fichiers)

    while True:
        try:
            saisie = input("  Your choice: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Operation cancelled.")
            return None

        if saisie == "0":
            print("  Goodbye!")
            return None

        if not saisie.isdigit():
            print("  Please enter a number.")
            continue

        idx = int(saisie)
        if idx < 1 or idx > max_idx:
            print(f"  Invalid choice (1-{max_idx}).")
            continue

        choisi = fichiers[idx - 1]

        if choisi.vide:
            print("  This file is empty. Choose another one.")
            continue

        if logger:
            logger.info(f"File selected: {choisi.nom}")

        return choisi


def confirmer_en_tetes(en_tetes_detectes: bool) -> bool:
    """Ask confirmation when header detection is uncertain."""
    label = "YES" if en_tetes_detectes else "NO"
    print(f"\n  Headers detected: {label}")

    while True:
        try:
            saisie = input("  Confirm? (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n  Operation cancelled.")
            return en_tetes_detectes

        if saisie in ("o", "oui", "y", "yes"):
            return True
        if saisie in ("n", "non", "no"):
            return False

        print("  Answer with 'y' or 'n'.")


def afficher_aucun_fichier() -> None:
    """Display message when no compatible files are found."""
    print("\n  No compatible files found.")
    print("  Supported formats: CSV, TSV, JSON, TXT\n")
