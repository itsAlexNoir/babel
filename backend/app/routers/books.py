import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Book, BookStatus
from ..schemas import BookCreate, BookResponse, BookStats, BookUpdate, BorrowRequest, CountItem, LibraryStats, StatusUpdate
from ..services.cover_service import fetch_cover_from_openlibrary

router = APIRouter(prefix="/api/books", tags=["books"])

UPLOAD_DIR = Path(os.environ.get("BABEL_UPLOAD_DIR", Path(__file__).resolve().parent.parent / "uploads"))
COVERS_DIR = UPLOAD_DIR / "covers"
COVERS_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/stats", response_model=BookStats)
def get_stats(db: Session = Depends(get_db)):
    total = db.query(Book).count()
    available = db.query(Book).filter(Book.status == BookStatus.available).count()
    borrowed = db.query(Book).filter(Book.status == BookStatus.borrowed).count()
    archived = db.query(Book).filter(Book.status == BookStatus.archived).count()
    return BookStats(total=total, available=available, borrowed=borrowed, archived=archived)


@router.get("/library-stats", response_model=LibraryStats)
def get_library_stats(db: Session = Depends(get_db)):
    total = db.query(Book).count()
    available = db.query(Book).filter(Book.status == BookStatus.available).count()
    borrowed = db.query(Book).filter(Book.status == BookStatus.borrowed).count()
    archived = db.query(Book).filter(Book.status == BookStatus.archived).count()

    top_authors = [
        CountItem(name=name, count=c)
        for name, c in db.query(Book.author, func.count()).group_by(Book.author).order_by(func.count().desc()).limit(15).all()
    ]

    top_publishers = [
        CountItem(name=name, count=c)
        for name, c in db.query(Book.publisher, func.count())
        .filter(Book.publisher.isnot(None))
        .group_by(Book.publisher)
        .order_by(func.count().desc())
        .limit(15)
        .all()
    ]

    languages = [
        CountItem(name=name or "Unknown", count=c)
        for name, c in db.query(Book.language, func.count()).group_by(Book.language).order_by(func.count().desc()).all()
    ]

    # Books by decade using publishing_date (fall back to edition_date)
    books = db.query(Book.publishing_date, Book.edition_date).all()
    decade_counts: dict[str, int] = {}
    for pub, ed in books:
        year_str = pub or ed
        if not year_str:
            continue
        try:
            year = int(year_str[:4])
            decade = f"{(year // 10) * 10}s"
            decade_counts[decade] = decade_counts.get(decade, 0) + 1
        except (ValueError, IndexError):
            continue
    books_by_decade = [
        CountItem(name=d, count=c)
        for d, c in sorted(decade_counts.items())
    ]

    return LibraryStats(
        total=total,
        available=available,
        borrowed=borrowed,
        archived=archived,
        top_authors=top_authors,
        top_publishers=top_publishers,
        languages=languages,
        books_by_decade=books_by_decade,
    )


@router.get("", response_model=list[BookResponse])
def list_books(
    status: BookStatus | None = None,
    search: str | None = Query(None, description="Search by title or author"),
    db: Session = Depends(get_db),
):
    query = db.query(Book)
    if status is not None:
        query = query.filter(Book.status == status)
    if search:
        term = f"%{search}%"
        query = query.filter(or_(Book.title.ilike(term), Book.author.ilike(term)))
    return query.order_by(Book.updated_at.desc()).all()


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("", response_model=BookResponse, status_code=201)
def create_book(data: BookCreate, db: Session = Depends(get_db)):
    book = Book(**data.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, data: BookUpdate, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(book, field, value)
    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    # Remove cover file if it exists
    if book.cover_image_path:
        cover_path = UPLOAD_DIR / book.cover_image_path
        if cover_path.exists():
            cover_path.unlink()
    db.delete(book)
    db.commit()


@router.patch("/{book_id}/status", response_model=BookResponse)
def update_status(book_id: int, data: StatusUpdate, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.status = data.status
    if data.status != BookStatus.borrowed:
        book.borrower_name = None
        book.borrowed_at = None
    if data.status == BookStatus.archived:
        book.archived_at = datetime.now(timezone.utc)
    elif data.status != BookStatus.archived:
        book.archived_at = None
    db.commit()
    db.refresh(book)
    return book


@router.post("/{book_id}/borrow", response_model=BookResponse)
def borrow_book(book_id: int, data: BorrowRequest, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.status = BookStatus.borrowed
    book.borrower_name = data.borrower_name
    book.borrowed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(book)
    return book


@router.post("/{book_id}/cover", response_model=BookResponse)
async def upload_cover(book_id: int, file: UploadFile, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if file.content_type not in ("image/jpeg", "image/png", "image/webp"):
        raise HTTPException(status_code=400, detail="Only JPEG, PNG, and WebP images are accepted")

    ext = file.filename.rsplit(".", 1)[-1] if file.filename and "." in file.filename else "jpg"
    filename = f"{book_id}.{ext}"
    dest = COVERS_DIR / filename

    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)

    book.cover_image_path = f"covers/{filename}"
    db.commit()
    db.refresh(book)
    return book


@router.post("/{book_id}/fetch-cover", response_model=BookResponse)
async def fetch_cover(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    cover_path = await fetch_cover_from_openlibrary(book.title, book.author, book_id, COVERS_DIR)
    if not cover_path:
        raise HTTPException(status_code=404, detail="Cover not found on Open Library")

    book.cover_image_path = f"covers/{cover_path.name}"
    db.commit()
    db.refresh(book)
    return book
