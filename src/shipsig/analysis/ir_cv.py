from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, cast

import cv2
import numpy as np
import numpy.typing as npt
import sqlite3

from ..config import IR_IMAGE_DIR

# Pattern for filenames like "ship_001_view_000.png"
SHIP_ID_PATTERN = re.compile(r"ship_(\d+)_", re.IGNORECASE)


def infer_ship_id_from_name(filename: str) -> Optional[int]:
    """Infer ship ID from a filename like 'ship_001_view_000.png'."""
    match = SHIP_ID_PATTERN.search(filename)
    if not match:
        return None
    return int(match.group(1))


def compute_ir_features(image_path: Path) -> Dict[str, float | int]:
    """Compute simple features from a grayscale IR image.

    Features
    --------
    mean_intensity:
        Mean pixel value of the image.
    hotspot_count:
        Number of pixels above a high intensity threshold.
    area_px:
        Number of pixels above a lower threshold (approx. silhouette area).
    """
    # OpenCV returns a "MatLike | None" here; we explicitly cast to NDArray[uint8]
    img_raw = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if img_raw is None:
        raise ValueError(f"Could not read image: {image_path}")

    # Make the type checker happy by casting to a concrete NumPy dtype
    img: npt.NDArray[np.uint8] = cast(npt.NDArray[np.uint8], img_raw)

    # Use an explicit float dtype for numerical stability and clearer typing
    mean_intensity = float(np.mean(img, dtype=np.float64))

    # Define thresholds based on 8-bit intensity
    _, mask_silhouette = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
    _, mask_hot = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)

    area_px = int(np.count_nonzero(mask_silhouette))
    hotspot_count = int(np.count_nonzero(mask_hot))

    return {
        "mean_intensity": mean_intensity,
        "hotspot_count": hotspot_count,
        "area_px": area_px,
    }


def insert_ir_features(
    conn: sqlite3.Connection,
    ship_id: int,
    image_path: Path,
    features: Dict[str, float | int],
) -> None:
    """Insert one IR feature row into the ir_features table."""
    conn.execute(
        """
        INSERT INTO ir_features (ship_id, image_path, mean_intensity, hotspot_count, area_px)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            ship_id,
            str(image_path),
            float(features["mean_intensity"]),
            int(features["hotspot_count"]),
            int(features["area_px"]),
        ),
    )


def process_ir_directory(
    conn: sqlite3.Connection,
    directory: Path | None = None,
) -> None:
    """Process all PNG images in the IR directory and store features in the DB.

    Parameters
    ----------
    conn:
        Open SQLite connection.
    directory:
        Optional path to the directory with IR images. If None, the default
        IR_IMAGE_DIR from the configuration is used.
    """
    dir_path = directory or IR_IMAGE_DIR
    if not dir_path.exists():
        print(f"IR image directory does not exist: {dir_path}")
        return

    png_files: List[Path] = sorted(dir_path.glob("*.png"))
    if not png_files:
        print(f"No PNG images found in {dir_path}")
        return

    for img_path in png_files:
        ship_id = infer_ship_id_from_name(img_path.name)
        if ship_id is None:
            print(f"Could not infer ship_id for {img_path.name}, skipping.")
            continue

        try:
            features = compute_ir_features(img_path)
        except ValueError as exc:
            print(exc)
            continue

        insert_ir_features(conn, ship_id, img_path, features)

    conn.commit()