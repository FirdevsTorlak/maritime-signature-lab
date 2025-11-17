from __future__ import annotations

import argparse

from . import config
from .db import get_connection, init_db
from .loaders import import_all_sample_data
from .analysis.acoustic import acoustic_summary
from .analysis.magnetic import magnetic_summary
from .analysis.rcs import rcs_summary
from .analysis.ir_cv import process_ir_directory


def cmd_init_db(args: argparse.Namespace) -> None:
    init_db()
    print(f"Database initialised at: {config.DB_PATH}")


def cmd_import_data(args: argparse.Namespace) -> None:
    with get_connection() as conn:
        import_all_sample_data(conn)
    print("Sample CSV data imported into the database.")


def cmd_acoustic_summary(args: argparse.Namespace) -> None:
    with get_connection() as conn:
        df = acoustic_summary(conn)
    print(df.to_string(index=False))


def cmd_magnetic_summary(args: argparse.Namespace) -> None:
    with get_connection() as conn:
        df = magnetic_summary(conn)
    print(df.to_string(index=False))


def cmd_rcs_summary(args: argparse.Namespace) -> None:
    with get_connection() as conn:
        df = rcs_summary(conn)
    print(df.to_string(index=False))


def cmd_ir_features(args: argparse.Namespace) -> None:
    with get_connection() as conn:
        process_ir_directory(conn)
    print("IR features computed (where possible) and stored in the database.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shipsig",
        description="Maritime Signature Lab CLI (synthetic data demo)."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_init = subparsers.add_parser("init-db", help="Initialise the SQLite database.")
    p_init.set_defaults(func=cmd_init_db)

    p_import = subparsers.add_parser("import-data", help="Import sample CSV data.")
    p_import.set_defaults(func=cmd_import_data)

    p_acoustic = subparsers.add_parser(
        "acoustic-summary",
        help="Show acoustic signature summary per ship.",
    )
    p_acoustic.set_defaults(func=cmd_acoustic_summary)

    p_magnetic = subparsers.add_parser(
        "magnetic-summary",
        help="Show magnetic signature summary per ship.",
    )
    p_magnetic.set_defaults(func=cmd_magnetic_summary)

    p_rcs = subparsers.add_parser(
        "rcs-summary",
        help="Show RCS values per ship and aspect angle.",
    )
    p_rcs.set_defaults(func=cmd_rcs_summary)

    p_ir = subparsers.add_parser(
        "ir-features",
        help="Compute IR features for images in data/images/ir.",
    )
    p_ir.set_defaults(func=cmd_ir_features)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
