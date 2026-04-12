from datetime import datetime

from pydantic import BaseModel

from .models import BookStatus


class BookCreate(BaseModel):
    title: str
    original_title: str | None = None
    author: str
    publisher: str | None = None
    original_pub_date: str | None = None
    publishing_date: str | None = None
    edition_date: str | None = None
    language: str | None = None
    original_language: str | None = None
    status: BookStatus = BookStatus.available
    notes: str | None = None
    translator: str | None = None
    tags: str | None = None


class BookUpdate(BaseModel):
    title: str | None = None
    original_title: str | None = None
    author: str | None = None
    publisher: str | None = None
    original_pub_date: str | None = None
    publishing_date: str | None = None
    edition_date: str | None = None
    language: str | None = None
    original_language: str | None = None
    status: BookStatus | None = None
    notes: str | None = None
    translator: str | None = None
    tags: str | None = None
    borrowed_at: datetime | None = None
    archived_at: datetime | None = None


class BookResponse(BaseModel):
    id: int
    title: str
    original_title: str | None = None
    author: str
    publisher: str | None = None
    original_pub_date: str | None = None
    publishing_date: str | None = None
    edition_date: str | None = None
    language: str | None = None
    original_language: str | None = None
    cover_image_path: str | None = None
    status: BookStatus
    notes: str | None = None
    translator: str | None = None
    tags: str | None = None
    borrower_name: str | None = None
    borrowed_at: datetime | None = None
    archived_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class BorrowRequest(BaseModel):
    borrower_name: str


class StatusUpdate(BaseModel):
    status: BookStatus


class OCRResult(BaseModel):
    title: str | None = None
    original_title: str | None = None
    author: str | None = None
    publisher: str | None = None
    original_pub_date: str | None = None
    publishing_date: str | None = None
    language: str | None = None
    raw_text: str = ""


class BookStats(BaseModel):
    total: int
    available: int
    borrowed: int
    archived: int


class CountItem(BaseModel):
    name: str
    count: int


class LibraryStats(BaseModel):
    total: int
    available: int
    borrowed: int
    archived: int
    top_authors: list[CountItem]
    top_publishers: list[CountItem]
    languages: list[CountItem]
    books_by_decade: list[CountItem]
