from __future__ import annotations

import sqlite3

import pandas as pd
import matplotlib.pyplot as plt


def magnetic_summary(conn: sqlite3.Connection) -> pd.DataFrame:
    """Return mean magnetic field per axis and ship."""
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


def plot_magnetic_axes(conn: sqlite3.Connection, ship_name: str) -> None:
    """Plot magnetic field values per axis for a given ship."""
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
    plt.show()
