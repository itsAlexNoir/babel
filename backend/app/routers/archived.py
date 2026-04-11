from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Book, BookStatus
from ..schemas import BookResponse

router = APIRouter(prefix="/api/archived", tags=["archived"])


@router.get("", response_model=list[BookResponse])
def list_archived(
    search: str | None = Query(None, description="Search by title or author"),
    db: Session = Depends(get_db),
):
    query = db.query(Book).filter(Book.status == BookStatus.archived)
    if search:
        term = f"%{search}%"
        query = query.filter(or_(Book.title.ilike(term), Book.author.ilike(term)))
    return query.order_by(Book.updated_at.desc()).all()
