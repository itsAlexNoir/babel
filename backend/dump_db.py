"""
Dump the Babel SQLite database to a file and create a backup copy of the DB.

Supported output formats: json (default), csv.

The script also copies the raw SQLite database file to the output directory.

Usage:
  uv run python dump_db.py <output_directory>
  uv run python dump_db.py <output_directory> --format csv
  uv run python dump_db.py <output_directory> --format json
"""

import argparse
import csv
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

# Ensure the backend app package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.database import DB_PATH, SessionLocal, engine
from app.models import Base, Book

# Columns to export (order preserved)
COLUMNS = [
    "id",
    "title",
    "original_title",
    "author",
    "publisher",
    "original_pub_date",
    "publishing_date",
    "edition_date",
    "language",
    "original_language",
    "cover_image_path",
    "status",
    "notes",
    "created_at",
    "updated_at",
]


def book_to_dict(book: Book) -> dict:
    """Convert a Book ORM instance to a plain dict."""
    d = {}
    for col in COLUMNS:
        value = getattr(book, col)
        if isinstance(value, datetime):
            value = value.isoformat()
        elif hasattr(value, "value"):
            # Enum → its string value
            value = value.value
        d[col] = value
    return d


def dump_json(books: list[dict], output_path: Path) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)


def dump_csv(books: list[dict], output_path: Path) -> None:
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(books)


def dump_database(output_dir: Path, fmt: str = "json") -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        books = db.query(Book).order_by(Book.id).all()
        rows = [book_to_dict(b) for b in books]
    finally:
        db.close()

    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # --- Export data file ---
    if fmt == "json":
        data_file = output_dir / f"babel_dump_{timestamp}.json"
        dump_json(rows, data_file)
    elif fmt == "csv":
        data_file = output_dir / f"babel_dump_{timestamp}.csv"
        dump_csv(rows, data_file)
    else:
        print(f"ERROR: Unsupported format '{fmt}'", file=sys.stderr)
        sys.exit(1)

    print(f"  Exported {len(rows)} books → {data_file}")

    # --- Copy raw SQLite database ---
    if DB_PATH.exists():
        db_copy = output_dir / f"babel_{timestamp}.db"
        shutil.copy2(DB_PATH, db_copy)
        print(f"  Database copy      → {db_copy}")
    else:
        print(f"  WARNING: Database file not found at {DB_PATH}, skipping copy.")

    print()
    print("=" * 50)
    print(f"  Total books exported: {len(rows)}")
    print(f"  Format:               {fmt}")
    print(f"  Output directory:     {output_dir}")
    print("=" * 50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dump the Babel database to a file and create a DB backup.")
    parser.add_argument("output_dir", help="Directory where the dump and DB copy will be saved")
    parser.add_argument(
        "--format",
        choices=["json", "csv"],
        default="json",
        help="Output format for the data dump (default: json)",
    )
    args = parser.parse_args()

    dump_database(Path(args.output_dir), fmt=args.format)
