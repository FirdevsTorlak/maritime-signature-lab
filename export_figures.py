from __future__ import annotations

import sys
from pathlib import Path

# Make sure the "src" directory is on sys.path so that "shipsig" can be imported
PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shipsig.db import get_connection
from shipsig.analysis.acoustic import plot_acoustic_bands
from shipsig.analysis.magnetic import plot_magnetic_axes
from shipsig.analysis.rcs import plot_rcs_curve


def main() -> None:
    conn = get_connection()

    # Save plots without popping up windows
    plot_acoustic_bands(conn, "Alpha", save=True, show=False)
    plot_acoustic_bands(conn, "Bravo", save=True, show=False)
    plot_acoustic_bands(conn, "Charlie", save=True, show=False)

    plot_magnetic_axes(conn, "Alpha", save=True, show=False)
    plot_rcs_curve(conn, "Alpha", save=True, show=False)


if __name__ == "__main__":
    main()