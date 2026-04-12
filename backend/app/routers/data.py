import csv
import io
import json
import shutil
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..database import DB_PATH, get_db
from ..models import Book, BookStatus

router = APIRouter(prefix="/api/data", tags=["data"])

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

SUPPORTED_FORMATS = ["json", "csv", "jsonl"]


def _book_to_dict(book: Book) -> dict:
    d = {}
    for col in COLUMNS:
        value = getattr(book, col)
        if isinstance(value, datetime):
            value = value.isoformat()
        elif hasattr(value, "value"):
            value = value.value
        d[col] = value
    return d


# ----------- Import CSV -----------

def _clean(value: str) -> str | None:
    v = value.strip()
    return v if v else None


def _build_notes(translator: str | None, tags: str | None) -> str | None:
    parts = []
    if translator:
        parts.append(f"Translator: {translator}")
    if tags:
        parts.append(f"Tags: {tags}")
    return "\n".join(parts) if parts else None


def _book_exists_in_db(
    db: Session,
    title: str,
    author: str | None,
    publisher: str | None,
    publishing_date: str | None,
    edition_date: str | None,
    language: str | None,
) -> bool:
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


@router.post("/import-csv")
async def import_csv_endpoint(file: UploadFile, db: Session = Depends(get_db)):
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted")

    content = await file.read()
    text = content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    reader.fieldnames = [h.strip() for h in (reader.fieldnames or [])]

    seen_this_run: set[tuple[str | None, ...]] = set()
    added = 0
    skipped_duplicate = 0
    skipped_missing = 0
    errors = 0

    for line_num, row in enumerate(reader, start=2):
        row = {k: v.strip() for k, v in row.items()}

        title = _clean(row.get("título", ""))
        author = _clean(row.get("autor/a", ""))

        if not title:
            skipped_missing += 1
            continue

        publisher = _clean(row.get("editorial", ""))
        publishing_date = _clean(row.get("año publicacion", ""))
        edition_date = _clean(row.get("año edicion", ""))
        language = _clean(row.get("idioma", ""))

        key = (
            title.lower(),
            author.lower() if author else None,
            publisher.lower() if publisher else None,
            publishing_date,
            edition_date,
            language.lower() if language else None,
        )
        if key in seen_this_run or _book_exists_in_db(
            db, title, author, publisher, publishing_date, edition_date, language
        ):
            skipped_duplicate += 1
            continue

        original_title = _clean(row.get("título original", ""))
        if original_title and original_title.lower() == title.lower():
            original_title = None

        notes = _build_notes(
            _clean(row.get("traductor/a", "")),
            _clean(row.get("etiquetas", "")),
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

        try:
            db.add(book)
            db.flush()
            seen_this_run.add(key)
            added += 1
        except Exception:
            db.rollback()
            errors += 1
            continue

    db.commit()

    return {
        "added": added,
        "skipped_duplicate": skipped_duplicate,
        "skipped_missing": skipped_missing,
        "errors": errors,
    }


# ----------- Export / Dump -----------

@router.get("/export")
def export_database(
    format: str = "json",
    db: Session = Depends(get_db),
):
    if format not in SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format '{format}'. Choose from: {', '.join(SUPPORTED_FORMATS)}",
        )

    books = db.query(Book).order_by(Book.id).all()
    rows = [_book_to_dict(b) for b in books]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if format == "json":
        content = json.dumps(rows, ensure_ascii=False, indent=2)
        media_type = "application/json"
        filename = f"babel_dump_{timestamp}.json"
    elif format == "csv":
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
        content = buf.getvalue()
        media_type = "text/csv"
        filename = f"babel_dump_{timestamp}.csv"
    else:  # jsonl
        content = "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n"
        media_type = "application/x-ndjson"
        filename = f"babel_dump_{timestamp}.jsonl"

    return StreamingResponse(
        iter([content]),
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ----------- Backup (raw .db copy) -----------

@router.get("/backup")
def backup_database():
    if not DB_PATH.exists():
        raise HTTPException(status_code=404, detail="Database file not found")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"babel_{timestamp}.db"

    def iter_file():
        with open(DB_PATH, "rb") as f:
            while chunk := f.read(64 * 1024):
                yield chunk

    return StreamingResponse(
        iter_file(),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
