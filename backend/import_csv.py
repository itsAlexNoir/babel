"""
Import books from a CSV file into the Babel SQLite database.

CSV columns expected:
  autor/a, título, título original, editorial, traductor/a,
  año publicacion, año edicion, idioma, etiquetas

Usage:
  uv run python import_csv.py <path/to/file.csv>
  uv run python import_csv.py <path/to/file.csv> --dry-run
"""

import argparse
import csv
import sys
from pathlib import Path

# Ensure the backend app package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.database import SessionLocal, engine
from app.models import Base, Book, BookStatus


def clean(value: str) -> str | None:
    """Strip whitespace; return None for empty strings."""
    v = value.strip()
    return v if v else None


def build_notes(translator: str | None, tags: str | None) -> str | None:
    parts = []
    if translator:
        parts.append(f"Translator: {translator}")
    if tags:
        parts.append(f"Tags: {tags}")
    return "\n".join(parts) if parts else None


def book_exists_in_db(
    db,
    title: str,
    author: str | None,
    publisher: str | None,
    publishing_date: str | None,
    edition_date: str | None,
    language: str | None,
) -> bool:
    """Return True if a fully identical entry already exists in the DB (case-insensitive)."""
    q = db.query(Book).filter(Book.title.ilike(title))
    if author:
        q = q.filter(Book.author.ilike(author))
    else:
        q = q.filter(Book.author.is_(None))
    if publisher:
        q = q.filter(Book.publisher.ilike(publisher))
    else:
        q = q.filter(Book.publisher.is_(None))
    if publishing_date:
        q = q.filter(Book.publishing_date == publishing_date)
    else:
        q = q.filter(Book.publishing_date.is_(None))
    if edition_date:
        q = q.filter(Book.edition_date == edition_date)
    else:
        q = q.filter(Book.edition_date.is_(None))
    if language:
        q = q.filter(Book.language.ilike(language))
    else:
        q = q.filter(Book.language.is_(None))
    return q.first() is not None


def import_csv(csv_path: Path, dry_run: bool = False) -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Tracks full-entry tuples added during this run to catch intra-CSV duplicates
    seen_this_run: set[tuple[str | None, ...]] = set()

    added = 0
    skipped_duplicate = 0
    skipped_missing = 0
    errors = 0

    try:
        with open(csv_path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            # Normalise header names (strip surrounding whitespace)
            reader.fieldnames = [h.strip() for h in (reader.fieldnames or [])]

            for line_num, row in enumerate(reader, start=2):  # 1-indexed, row 1 is header
                # Strip all values
                row = {k: v.strip() for k, v in row.items()}

                title = clean(row.get("título", ""))
                author = clean(row.get("autor/a", ""))

                if not title:
                    print(f"  [LINE {line_num}] SKIP — missing title: {row}")
                    skipped_missing += 1
                    continue

                publisher = clean(row.get("editorial", ""))
                publishing_date = clean(row.get("año publicacion", ""))
                edition_date = clean(row.get("año edicion", ""))
                language = clean(row.get("idioma", ""))

                key = (
                    title.lower(),
                    author.lower() if author else None,
                    publisher.lower() if publisher else None,
                    publishing_date,
                    edition_date,
                    language.lower() if language else None,
                )
                if key in seen_this_run or book_exists_in_db(
                    db, title, author, publisher, publishing_date, edition_date, language
                ):
                    print(f"  [LINE {line_num}] DUPLICATE — '{title}' by {author}")
                    skipped_duplicate += 1
                    continue

                original_title = clean(row.get("título original", ""))
                # If original title is identical to title, treat as None (no value added)
                if original_title and original_title.lower() == title.lower():
                    original_title = None

                notes = build_notes(
                    clean(row.get("traductor/a", "")),
                    clean(row.get("etiquetas", "")),
                )

                book = Book(
                    title=title,
                    original_title=original_title,
                    author=author,
                    publisher=publisher,
                    publishing_date=publishing_date,
                    edition_date=edition_date,
                    language=language,
                    notes=notes,
                    status=BookStatus.available,
                )

                if dry_run:
                    print(f"  [LINE {line_num}] WOULD ADD — '{title}' by {author}")
                    seen_this_run.add(key)
                else:
                    try:
                        db.add(book)
                        db.flush()  # catch constraint errors early
                        seen_this_run.add(key)
                        print(f"  [LINE {line_num}] ADDED — '{title}' by {author}")
                        added += 1
                    except Exception as exc:
                        db.rollback()
                        print(f"  [LINE {line_num}] ERROR — '{title}' by {author}: {exc}")
                        errors += 1
                        continue

        if not dry_run:
            db.commit()

    except FileNotFoundError:
        print(f"ERROR: File not found: {csv_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        db.rollback()
        print(f"ERROR: Unexpected error: {exc}", file=sys.stderr)
        sys.exit(1)
    finally:
        db.close()

    print()
    print("=" * 50)
    if dry_run:
        print("DRY RUN — no changes written to database.")
    print(f"  Added:            {added}")
    print(f"  Skipped (dup):    {skipped_duplicate}")
    print(f"  Skipped (empty):  {skipped_missing}")
    print(f"  Errors:           {errors}")
    print("=" * 50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import books from CSV into Babel database.")
    parser.add_argument("csv_file", help="Path to the CSV file")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be imported without writing to the database",
    )
    args = parser.parse_args()

    import_csv(Path(args.csv_file), dry_run=args.dry_run)
