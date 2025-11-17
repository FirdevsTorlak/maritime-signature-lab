from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterator, Sequence, Optional

from .config import DB_PATH, SCHEMA_PATH


def get_connection(db_path: Optional[Path] = None) -> sqlite3.Connection:
    """Return a SQLite connection with foreign keys enabled."""
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(schema_path: Optional[Path] = None, db_path: Optional[Path] = None) -> None:
    """(Re)create the database using the SQL schema file.

    Calling this function will remove any existing SQLite file so that it can be
    used as a clean reset during development.
    """
    schema_file = schema_path or SCHEMA_PATH
    if not schema_file.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_file}")

    path = db_path or DB_PATH

    # Start from a clean database file if it already exists
    if path.exists():
        path.unlink()

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(schema_file, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    # Use get_connection so that PRAGMA foreign_keys is applied consistently
    with get_connection(path) as conn:
        conn.executescript(schema_sql)


def iter_rows(
    conn: sqlite3.Connection,
    query: str,
    params: Sequence | None = None,
) -> Iterator[tuple]:
    """Yield rows from a SELECT query as an iterator of tuples."""
    cur = conn.execute(query, params or ())
    for row in cur:
        yield row