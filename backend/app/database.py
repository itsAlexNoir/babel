import os
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATA_DIR = Path(os.environ.get("BABEL_DATA_DIR", Path(__file__).resolve().parent.parent))
DB_PATH = DATA_DIR / "babel.db"

engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def migrate(eng=None):
    """Add new columns to existing DB without dropping data."""
    target = eng or engine
    new_cols = [
        ("translator", "VARCHAR(300)"),
        ("tags", "VARCHAR(500)"),
        ("borrower_name", "VARCHAR(300)"),
        ("borrowed_at", "DATETIME"),
        ("archived_at", "DATETIME"),
    ]
    with target.connect() as conn:
        existing = {row[1] for row in conn.execute(text("PRAGMA table_info(books)"))}
        for col, col_type in new_cols:
            if col not in existing:
                conn.execute(text(f"ALTER TABLE books ADD COLUMN {col} {col_type}"))
        conn.commit()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
