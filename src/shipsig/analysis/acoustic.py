from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt

from ..config import BASE_DIR

# Default directory for saving figures, relative to the project root
FIGURES_DIR: Path = BASE_DIR / "docs" / "figures"


def acoustic_summary(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Return average band levels per ship as a DataFrame.

    Parameters
    ----------
    conn:
        Open SQLite connection to the maritime signature database.

    Returns
    -------
    pandas.DataFrame
        Columns: ship_name, band_label, mean_level_db
    """
    query = """
    SELECT s.name AS ship_name,
           a.band_label,
           AVG(a.level_db) AS mean_level_db
    FROM acoustic_signatures a
    JOIN ships s ON s.id = a.ship_id
    GROUP BY s.name, a.band_label
    ORDER BY s.name, a.band_label;
    """
    return pd.read_sql_query(query, conn)


def plot_acoustic_bands(
    conn: sqlite3.Connection,
    ship_name: str,
    save: bool = False,
    filename: Optional[str | Path] = None,
    show: bool = True,
) -> None:
    """
    Plot acoustic band levels for a given ship.

    Parameters
    ----------
    conn:
        Open SQLite connection.
    ship_name:
        Name of the ship (e.g. "Alpha").
    save:
        If True, save the figure under docs/figures/.
    filename:
        Optional file name for the PNG. If None, a default based on the ship
        name is used (e.g. "acoustic_alpha.png").
    show:
        If True, display the figure; if False, close it after saving.
    """
    query = """
    SELECT a.band_label, a.level_db
    FROM acoustic_signatures a
    JOIN ships s ON s.id = a.ship_id
    WHERE s.name = ?
    ORDER BY a.band_label;
    """
    df = pd.read_sql_query(query, conn, params=(ship_name,))
    if df.empty:
        print(f"No acoustic data found for ship: {ship_name}")
        return

    plt.figure()
    plt.bar(df["band_label"], df["level_db"])
    plt.xlabel("Band")
    plt.ylabel("Level [dB]")
    plt.title(f"Acoustic signature bands for {ship_name}")
    plt.tight_layout()

    if save:
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        if filename is None:
            safe_name = ship_name.lower().replace(" ", "_")
            filename = f"acoustic_{safe_name}.png"
        out_path = FIGURES_DIR / Path(filename).name
        plt.savefig(out_path, dpi=300, bbox_inches="tight")
        print(f"Saved acoustic plot to: {out_path}")

    if show:
        plt.show()
    else:
        plt.close()