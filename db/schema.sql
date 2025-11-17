PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS ships (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    class TEXT,
    displacement_t REAL,
    length_m REAL,
    beam_m REAL
);

CREATE TABLE IF NOT EXISTS acoustic_signatures (
    id INTEGER PRIMARY KEY,
    ship_id INTEGER NOT NULL,
    band_label TEXT NOT NULL,
    level_db REAL NOT NULL,
    FOREIGN KEY (ship_id) REFERENCES ships (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS magnetic_signatures (
    id INTEGER PRIMARY KEY,
    ship_id INTEGER NOT NULL,
    axis TEXT NOT NULL,
    value_nt REAL NOT NULL,
    FOREIGN KEY (ship_id) REFERENCES ships (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS rcs_signatures (
    id INTEGER PRIMARY KEY,
    ship_id INTEGER NOT NULL,
    aspect_deg REAL NOT NULL,
    rcs_dbsm REAL NOT NULL,
    FOREIGN KEY (ship_id) REFERENCES ships (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ir_features (
    id INTEGER PRIMARY KEY,
    ship_id INTEGER NOT NULL,
    image_path TEXT NOT NULL,
    mean_intensity REAL,
    hotspot_count INTEGER,
    area_px INTEGER,
    FOREIGN KEY (ship_id) REFERENCES ships (id) ON DELETE CASCADE
);
