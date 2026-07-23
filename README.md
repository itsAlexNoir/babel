# Babel — Library Catalogue Manager

A local library catalogue app for managing your book collection. Track books, mark them as borrowed or archived, upload covers, and extract book data from photos using OCR.

**Stack:** FastAPI (Python) · SvelteKit (TypeScript) · SQLite · Tesseract OCR · Docker

> **Platform note:** This guide targets macOS on Apple Silicon (M4/M3/M2/M1). The Docker images are built natively for `linux/arm64`.

---

## Quick Start with Docker

### 1. Install prerequisites

```bash
# Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Docker CLI, Compose plugin, Buildx plugin, and Colima (lightweight Docker runtime)
brew install docker docker-compose docker-buildx colima

# Register the Compose and Buildx plugins so `docker compose` works
mkdir -p ~/.docker/cli-plugins
ln -sfn /opt/homebrew/opt/docker-compose/bin/docker-compose ~/.docker/cli-plugins/docker-compose
ln -sfn /opt/homebrew/opt/docker-buildx/bin/docker-buildx ~/.docker/cli-plugins/docker-buildx
```

### 2. (One-time) Fix Docker Hub CDN connectivity

Docker Hub serves image layers via Cloudflare CDN, which can be blocked on some networks. Configure a daemon mirror to avoid timeouts:

```bash
mkdir -p ~/.colima/default
cat > ~/.colima/default/daemon.json << 'EOF'
{
  "registry-mirrors": ["https://mirror.gcr.io"]
}
EOF
```

### 3. Start the Docker runtime

```bash
colima start --dns 8.8.8.8
```

> Colima must be running before any `docker` command. After a reboot just run `colima start` again.

### 4. Build and run

```bash
docker compose up --build
```

- **Frontend:** <http://localhost:3000>
- **Backend API docs:** <http://localhost:8000/docs>

Data (SQLite DB and cover images) persists in `./data_library/`.

To stop:

```bash
docker compose down
```

---

## Development Setup (without Docker)

### Prerequisites

```bash
# Python package manager
brew install uv

# Node.js 20+
brew install node

# Tesseract OCR
brew install tesseract
```

### Backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

API docs available at <http://localhost:8000/docs>

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App available at <http://localhost:5173> (Vite proxies API requests to the backend)

---

## Importing from a CSV file

If you already have a book catalogue in a CSV file, `backend/import_csv.py` can populate the database in one step.

### Expected CSV format

The script expects the following column headers (the same format used in the original Babel spreadsheet):

```text
autor/a, título, título original, editorial, traductor/a, año publicacion, año edicion, idioma, etiquetas
```

| CSV column | DB field | Notes |
| --- | --- | --- |
| `autor/a` | Author | Required — rows without this are skipped |
| `título` | Title | Required — rows without this are skipped |
| `título original` | Original Title | Omitted if identical to title |
| `editorial` | Publisher | |
| `año publicacion` | Publishing Date | Free-text; year-only values like `1951` are fine |
| `año edicion` | Edition Date | |
| `idioma` | Language | |
| `traductor/a` | Notes (Translator) | Combined into the Notes field |
| `etiquetas` | Notes (Tags) | Combined into the Notes field |

All books are imported with status **Available**.

### Running the import

**Step 1 — dry run** (preview what will be imported, no changes written):

```bash
cd backend
uv run python import_csv.py /path/to/your_catalogue.csv --dry-run
```

This prints every line that would be added, skipped as a duplicate, or skipped due to missing data. Review the output before proceeding.

**Step 2 — real import:**

```bash
uv run python import_csv.py /path/to/your_catalogue.csv
```

A summary is printed at the end:

```text
==================================================
  Added:            312
  Skipped (dup):      4
  Skipped (empty):    1
  Errors:             0
==================================================
```

### Duplicate detection

The script checks for duplicates in two ways:

- **Against the database** — any book already in the DB with the same title and author (case-insensitive) is skipped.
- **Within the CSV** — if the same title+author appears more than once in the file, only the first occurrence is imported.

Running the import a second time on the same file is safe — all rows will be detected as duplicates and skipped.

### Running inside Docker

If the app is running via Docker Compose, copy the CSV into the container and run the script there:

```bash
docker compose cp /path/to/your_catalogue.csv backend:/tmp/catalogue.csv
docker compose exec backend uv run python import_csv.py /tmp/catalogue.csv --dry-run
docker compose exec backend uv run python import_csv.py /tmp/catalogue.csv
```

---

## Using the App

### 1. Adding a book manually

1. Click **Catalogue** in the sidebar, then **+ Add Book**.
2. Fill in at least **Title** and **Author**. All other fields (publisher, dates, language, notes) are optional.
3. For dates, you can enter just a year (`1605`), a year and month (`2023-05`), or a full date (`2023-05-15`). This is especially useful for classics that have been republished many times — use **Original Publication** for the first edition year and **Publishing Date** for the copy you own.
4. Click **Add Book**. The book appears in the catalogue.

### 2. Adding a cover image

From the book's detail page you have two options:

- **Fetch Cover** — Searches [Open Library](https://openlibrary.org/) by title and author and downloads the cover automatically. Works best for well-known books.
- **Upload** — Click the Upload button to pick an image from your computer (JPEG, PNG, or WebP).

### 3. Scanning a book with OCR

This is the fastest way to add a book when you have a physical copy in hand.

1. Click **Scan** in the sidebar.
2. Drag and drop (or click to browse) one or more photos of the book. The best shots to use are:
   - The **front cover** — usually contains the title and author.
   - The **title page** (inside front) — often has publisher and year.
   - The **copyright page** (verso of title page) — has edition year, ISBN, and original publication info.
3. Click **Scan X image(s)**. Tesseract will extract the text.
4. The **Review & Save** form appears pre-filled with whatever the OCR could identify. Check each field, correct any mistakes, and click **Save Book**.
5. You can expand **View raw OCR text** to see exactly what was detected if a field looks wrong.

> **Tip:** The cleaner and flatter the photo, the better the results. Good lighting matters more than resolution.

### 4. Borrowing and returning books

- Open a book's detail page and click **Mark Borrowed**. The book moves to the **Borrowed** section.
- To return it, either open the detail page and click **Return**, or go to **Borrowed**, find the book, and click the **Return** button on its card.
- The book's status returns to *Available* in the catalogue.

### 5. Archiving books

Use the **Archived** status for books stored outside the library (e.g., in boxes in storage).

- Open a book's detail page and click **Archive**.
- To bring it back, go to **Archived** and click **Restore** on the card, or use the **Restore** button on the detail page.

### 6. Searching

Every section (Catalogue, Borrowed, Archived) has a search bar that filters by **title** and **author** as you type. The search is debounced — just start typing and results update automatically.

### 7. Editing or deleting a book

Open any book from its card, then:

- Click **Edit** to modify any field, including status.
- Click **Delete** → **Confirm Delete** to permanently remove the book and its cover image.

---

## Features

- **Book catalogue** — Add, edit, delete books with title, author, publisher, dates, language, and more
- **Cover images** — Upload covers manually or auto-fetch from Open Library
- **Borrowed books** — Mark books as borrowed and track them in a dedicated section
- **Archived books** — Archive books stored outside the library (e.g., in boxes)
- **OCR scanning** — Upload photos of books to extract metadata via Tesseract OCR
- **Search** — Filter books by title or author across all sections
- **Flexible dates** — Supports year-only dates (e.g., "1605") for classics

## Project Structure

```text
babel/
├── backend/           # FastAPI + SQLite
│   ├── app/
│   │   ├── main.py        # App entry point
│   │   ├── database.py    # SQLAlchemy setup
│   │   ├── models.py      # Book model
│   │   ├── schemas.py     # Pydantic schemas
│   │   ├── routers/       # API endpoints
│   │   └── services/      # OCR + cover services
│   ├── pyproject.toml     # Python dependencies (uv)
│   └── Dockerfile
├── frontend/          # SvelteKit
│   ├── src/
│   │   ├── routes/        # Pages
│   │   └── lib/           # Components, API client, types
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```


> See the earlier **Importing from a CSV file** section for the CSV import workflow and expected file format.
### Expected CSV format

The script expects the following column headers (the same format used in the original Babel spreadsheet):

```text
autor/a, título, título original, editorial, traductor/a, año publicacion, año edicion, idioma, etiquetas
```

| CSV column | DB field | Notes |
| --- | --- | --- |
| `autor/a` | Author | Optional |
| `título` | Title | Required — rows without this are skipped |
| `título original` | Original Title | Omitted if identical to title |
| `editorial` | Publisher | |
| `año publicacion` | Publishing Date | Free-text; year-only values like `1951` are fine |
| `año edicion` | Edition Date | |
| `idioma` | Language | |
| `traductor/a` | Notes (Translator) | Combined into the Notes field |
| `etiquetas` | Notes (Tags) | Combined into the Notes field |

All books are imported with status **Available**.

### Running the import

**Step 1 — dry run** (preview what will be imported, no changes written):

```bash
cd backend
uv run python import_csv.py /path/to/your_catalogue.csv --dry-run
```

This prints every line that would be added, skipped as a duplicate, or skipped due to missing data. Review the output before proceeding.

**Step 2 — real import:**

```bash
uv run python import_csv.py /path/to/your_catalogue.csv
```

A summary is printed at the end:

```text
==================================================
  Added:            312
  Skipped (dup):      4
  Skipped (empty):    1
  Errors:             0
==================================================
```

### Duplicate detection

The script checks for duplicates in two ways:

- **Against the database** — any book already in the DB with the same `title`, `author`, `publisher`, `publishing_date`, `edition_date`, and `language` is skipped.
- **Within the CSV** — if the same combination of `title`, `author`, `publisher`, `publishing_date`, `edition_date`, and `language` appears more than once in the file, only the first occurrence is imported.

Running the import a second time on the same file is safe — all rows will be detected as duplicates and skipped.

### Running inside Docker

If the app is running via Docker Compose, copy the CSV into the container and run the script there:

```bash
docker compose cp /path/to/your_catalogue.csv backend:/tmp/catalogue.csv
docker compose exec backend uv run python import_csv.py /tmp/catalogue.csv --dry-run
docker compose exec backend uv run python import_csv.py /tmp/catalogue.csv
```

---

## Using the App

### 1. Adding a book manually

1. Click **Catalogue** in the sidebar, then **+ Add Book**.
2. Fill in at least **Title** and **Author**. All other fields (publisher, dates, language, notes) are optional.
3. For dates, you can enter just a year (`1605`), a year and month (`2023-05`), or a full date (`2023-05-15`). This is especially useful for classics that have been republished many times — use **Original Publication** for the first edition year and **Publishing Date** for the copy you own.
4. Click **Add Book**. The book appears in the catalogue.

### 2. Adding a cover image

From the book's detail page you have two options:

- **Fetch Cover** — Searches [Open Library](https://openlibrary.org/) by title and author and downloads the cover automatically. Works best for well-known books.
- **Upload** — Click the Upload button to pick an image from your computer (JPEG, PNG, or WebP).

### 3. Scanning a book with OCR

This is the fastest way to add a book when you have a physical copy in hand.

1. Click **Scan** in the sidebar.
2. Drag and drop (or click to browse) one or more photos of the book. The best shots to use are:
   - The **front cover** — usually contains the title and author.
   - The **title page** (inside front) — often has publisher and year.
   - The **copyright page** (verso of title page) — has edition year, ISBN, and original publication info.
3. Click **Scan X image(s)**. Tesseract will extract the text.
4. The **Review & Save** form appears pre-filled with whatever the OCR could identify. Check each field, correct any mistakes, and click **Save Book**.
5. You can expand **View raw OCR text** to see exactly what was detected if a field looks wrong.

> **Tip:** The cleaner and flatter the photo, the better the results. Good lighting matters more than resolution.

### 4. Borrowing and returning books

- Open a book's detail page and click **Mark Borrowed**. The book moves to the **Borrowed** section.
- To return it, either open the detail page and click **Return**, or go to **Borrowed**, find the book, and click the **Return** button on its card.
- The book's status returns to *Available* in the catalogue.

### 5. Archiving books

Use the **Archived** status for books stored outside the library (e.g., in boxes in storage).

- Open a book's detail page and click **Archive**.
- To bring it back, go to **Archived** and click **Restore** on the card, or use the **Restore** button on the detail page.

### 6. Searching

Every section (Catalogue, Borrowed, Archived) has a search bar that filters by **title** and **author** as you type. The search is debounced — just start typing and results update automatically.

### 7. Editing or deleting a book

Open any book from its card, then:

- Click **Edit** to modify any field, including status.
- Click **Delete** → **Confirm Delete** to permanently remove the book and its cover image.

---

## Features

- **Book catalogue** — Add, edit, delete books with title, author, publisher, dates, language, and more
- **Cover images** — Upload covers manually or auto-fetch from Open Library
- **Borrowed books** — Mark books as borrowed and track them in a dedicated section
- **Archived books** — Archive books stored outside the library (e.g., in boxes)
- **OCR scanning** — Upload photos of books to extract metadata via Tesseract OCR
- **Search** — Filter books by title or author across all sections
- **Flexible dates** — Supports year-only dates (e.g., "1605") for classics

## Project Structure

```text
babel/
├── backend/           # FastAPI + SQLite
│   ├── app/
│   │   ├── main.py        # App entry point
│   │   ├── database.py    # SQLAlchemy setup
│   │   ├── models.py      # Book model
│   │   ├── schemas.py     # Pydantic schemas
│   │   ├── routers/       # API endpoints
│   │   └── services/      # OCR + cover services
│   ├── pyproject.toml     # Python dependencies (uv)
│   └── Dockerfile
├── frontend/          # SvelteKit
│   ├── src/
│   │   ├── routes/        # Pages
│   │   └── lib/           # Components, API client, types
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```
