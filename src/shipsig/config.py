from __future__ import annotations

from pathlib import Path

# shipsig is in src/shipsig, so two levels up is the project root
BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "signatures.db"
SCHEMA_PATH = BASE_DIR / "db" / "schema.sql"
DATA_DIR = BASE_DIR / "data"

CSV_DIR = DATA_DIR / "csv"
IR_IMAGE_DIR = DATA_DIR / "images" / "ir"
