from __future__ import annotations

import sqlite3

import pandas as pd
import matplotlib.pyplot as plt


def acoustic_summary(conn: sqlite3.Connection) -> pd.DataFrame:
    """Return average band levels per ship as a DataFrame."""
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


def plot_acoustic_bands(conn: sqlite3.Connection, ship_name: str) -> None:
    """Plot band levels for a given ship using matplotlib."""
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
    plt.show()
