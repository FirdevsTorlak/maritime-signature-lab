from __future__ import annotations

import sqlite3
from typing import NoReturn  # optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def rcs_summary(conn: sqlite3.Connection) -> pd.DataFrame:
    """Return RCS values per ship and aspect angle."""
    query = """
    SELECT s.name AS ship_name,
           r.aspect_deg,
           r.rcs_dbsm
    FROM rcs_signatures r
    JOIN ships s ON s.id = r.ship_id
    ORDER BY s.name, r.aspect_deg;
    """
    return pd.read_sql_query(query, conn)


def plot_rcs_curve(conn: sqlite3.Connection, ship_name: str) -> None:
    """Plot a simple RCS curve versus aspect angle for a ship."""
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

    # Convert explicitly to NumPy arrays of float
    angles_deg = df["aspect_deg"].to_numpy(dtype=float)
    rcs = df["rcs_dbsm"].to_numpy(dtype=float)

    plt.figure()
    plt.plot(angles_deg, rcs, marker="o")
    plt.xlabel("Aspect angle [deg]")
    plt.ylabel("RCS [dBsm]")
    plt.title(f"RCS vs. aspect angle for {ship_name}")
    plt.tight_layout()
    plt.show()