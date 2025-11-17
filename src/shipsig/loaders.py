from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from .config import CSV_DIR


def _load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")
    return pd.read_csv(path)


def import_ships(conn: sqlite3.Connection, csv_path: Path | None = None) -> None:
    path = csv_path or (CSV_DIR / "ships.csv")
    df = _load_csv(path)
    df.to_sql("ships", conn, if_exists="append", index=False)


def import_acoustic(conn: sqlite3.Connection, csv_path: Path | None = None) -> None:
    path = csv_path or (CSV_DIR / "acoustic_signatures.csv")
    df = _load_csv(path)
    df.to_sql("acoustic_signatures", conn, if_exists="append", index=False)


def import_magnetic(conn: sqlite3.Connection, csv_path: Path | None = None) -> None:
    path = csv_path or (CSV_DIR / "magnetic_signatures.csv")
    df = _load_csv(path)
    df.to_sql("magnetic_signatures", conn, if_exists="append", index=False)


def import_rcs(conn: sqlite3.Connection, csv_path: Path | None = None) -> None:
    path = csv_path or (CSV_DIR / "rcs_signatures.csv")
    df = _load_csv(path)
    df.to_sql("rcs_signatures", conn, if_exists="append", index=False)


def import_all_sample_data(conn: sqlite3.Connection) -> None:
    """Import all provided CSV files into the database."""
    import_ships(conn)
    import_acoustic(conn)
    import_magnetic(conn)
    import_rcs(conn)
