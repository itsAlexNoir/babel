import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class BookStatus(str, enum.Enum):
    available = "available"
    borrowed = "borrowed"
    archived = "archived"


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    original_title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    author: Mapped[str] = mapped_column(String(300), nullable=False)
    publisher: Mapped[str | None] = mapped_column(String(300), nullable=True)
    original_pub_date: Mapped[str | None] = mapped_column(String(20), nullable=True)
    publishing_date: Mapped[str | None] = mapped_column(String(20), nullable=True)
    edition_date: Mapped[str | None] = mapped_column(String(20), nullable=True)
    language: Mapped[str | None] = mapped_column(String(50), nullable=True)
    original_language: Mapped[str | None] = mapped_column(String(50), nullable=True)
    cover_image_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[BookStatus] = mapped_column(
        Enum(BookStatus), nullable=False, default=BookStatus.available
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    translator: Mapped[str | None] = mapped_column(String(300), nullable=True)
    tags: Mapped[str | None] = mapped_column(String(500), nullable=True)
    borrower_name: Mapped[str | None] = mapped_column(String(300), nullable=True)
    borrowed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    archived_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
