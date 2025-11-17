from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ..config import BASE_DIR

FIGURES_DIR: Path = BASE_DIR / "docs" / "figures"


def rcs_summary(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Return RCS values per ship and aspect angle as a pandas DataFrame.

    Parameters
    ----------
    conn:
        Open SQLite connection to the maritime signature database.

    Returns
    -------
    pandas.DataFrame
        Columns: ship_name, aspect_deg, rcs_dbsm
    """
    query = """
    SELECT s.name AS ship_name,
           r.aspect_deg,
           r.rcs_dbsm
    FROM rcs_signatures r
    JOIN ships s ON s.id = r.ship_id
    ORDER BY s.name, r.aspect_deg;
    """
    return pd.read_sql_query(query, conn)


def plot_rcs_curve(
    conn: sqlite3.Connection,
    ship_name: str,
    save: bool = False,
    filename: Optional[str | Path] = None,
    show: bool = True,
) -> None:
    """
    Plot a simple RCS curve versus aspect angle for a given ship.

    Parameters
    ----------
    conn:
        Open SQLite connection to the maritime signature database.
    ship_name:
        Name of the ship as stored in the 'ships' table (e.g. "Alpha").
    save:
        If True, save the figure as a PNG file under docs/figures/.
    filename:
        Optional file name (or Path) for the saved figure. If None and
        `save=True`, a default name like "rcs_alpha.png" is used.
    show:
        If True (default), display the figure using plt.show(). If False,
        the figure is closed after saving.
    """
    query = """
    SELECT r.aspect_deg, r.rcs_dbsm
    FROM rcs_signatures r
    JOIN ships s ON s.id = r.ship_id
    WHERE s.name = ?
    ORDER BY r.aspect_deg;
    """
    df = pd.read_sql_query(query, conn, params=(ship_name,))
    if df.empty:
        print(f"No RCS data found for ship: {ship_name}")
        return

    angles_deg = df["aspect_deg"].to_numpy(dtype=float)
    rcs = df["rcs_dbsm"].to_numpy(dtype=float)

    plt.figure()
    plt.plot(angles_deg, rcs, marker="o")
    plt.xlabel("Aspect angle [deg]")
    plt.ylabel("RCS [dBsm]")
    plt.title(f"RCS vs. aspect angle for {ship_name}")
    plt.tight_layout()

    if save:
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        if filename is None:
            safe_name = ship_name.lower().replace(" ", "_")
            filename = f"rcs_{safe_name}.png"
        out_path = FIGURES_DIR / Path(filename).name
        plt.savefig(out_path, dpi=300, bbox_inches="tight")
        print(f"Saved RCS plot to: {out_path}")

    if show:
        plt.show()
    else:
        plt.close()