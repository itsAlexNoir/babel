import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .database import Base, engine, migrate
from .routers import archived, books, borrowed, data, ocr

Base.metadata.create_all(bind=engine)
migrate()

app = FastAPI(title="Babel", description="Library Catalogue Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # SvelteKit dev server
        "http://localhost:3000",  # SvelteKit production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router)
app.include_router(borrowed.router)
app.include_router(archived.router)
app.include_router(ocr.router)
app.include_router(data.router)

# Serve uploaded files (covers, etc.)
UPLOAD_DIR = Path(os.environ.get("BABEL_UPLOAD_DIR", Path(__file__).resolve().parent / "uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")


@app.get("/api/health")
def health():
    return {"status": "ok"}
