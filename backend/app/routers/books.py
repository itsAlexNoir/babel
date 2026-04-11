import os
import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Book, BookStatus
from ..schemas import BookCreate, BookResponse, BookStats, BookUpdate, StatusUpdate
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
