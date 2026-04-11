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
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


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
