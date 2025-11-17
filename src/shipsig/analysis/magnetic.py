from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt

from ..config import BASE_DIR

FIGURES_DIR: Path = BASE_DIR / "docs" / "figures"


def magnetic_summary(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Return mean magnetic field per axis and ship.

    Parameters
    ----------
    conn:
        Open SQLite connection.

    Returns
    -------
    pandas.DataFrame
        Columns: ship_name, axis, mean_value_nt
    """
    query = """
    SELECT s.name AS ship_name,
           m.axis,
           AVG(m.value_nt) AS mean_value_nt
    FROM magnetic_signatures m
    JOIN ships s ON s.id = m.ship_id
    GROUP BY s.name, m.axis
    ORDER BY s.name, m.axis;
    """
    return pd.read_sql_query(query, conn)


def plot_magnetic_axes(
    conn: sqlite3.Connection,
    ship_name: str,
    save: bool = False,
    filename: Optional[str | Path] = None,
    show: bool = True,
) -> None:
    """
    Plot magnetic field values per axis for a given ship.

    Parameters
    ----------
    conn:
        Open SQLite connection.
    ship_name:
        Name of the ship (e.g. "Alpha").
    save:
        If True, save the figure under docs/figures/.
    filename:
        Optional PNG file name. If None, "magnetic_<ship>.png" is used.
    show:
        If True, display the figure; otherwise close it after saving.
    """
    query = """
    SELECT m.axis, m.value_nt
    FROM magnetic_signatures m
    JOIN ships s ON s.id = m.ship_id
    WHERE s.name = ?
    ORDER BY m.axis;
    """
    df = pd.read_sql_query(query, conn, params=(ship_name,))
    if df.empty:
        print(f"No magnetic data found for ship: {ship_name}")
        return

    plt.figure()
    plt.bar(df["axis"], df["value_nt"])
    plt.xlabel("Axis")
    plt.ylabel("Magnetic field [nT]")
    plt.title(f"Magnetic signature for {ship_name}")
    plt.tight_layout()

    if save:
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        if filename is None:
            safe_name = ship_name.lower().replace(" ", "_")
            filename = f"magnetic_{safe_name}.png"
        out_path = FIGURES_DIR / Path(filename).name
        plt.savefig(out_path, dpi=300, bbox_inches="tight")
        print(f"Saved magnetic plot to: {out_path}")

    if show:
        plt.show()
    else:
        plt.close()