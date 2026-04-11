from pathlib import Path

import httpx


async def fetch_cover_from_openlibrary(
    title: str, author: str, book_id: int, covers_dir: Path
) -> Path | None:
    """Search Open Library for a book and download its cover image."""
    search_url = "https://openlibrary.org/search.json"
    params = {"title": title, "author": author, "limit": 1}

    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(search_url, params=params)
        if resp.status_code != 200:
            return None

        data = resp.json()
        docs = data.get("docs", [])
        if not docs:
            return None

        # Try to get cover ID from the first result
        cover_id = docs[0].get("cover_i")
        if not cover_id:
            return None

        # Download the cover (medium size)
        cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
        cover_resp = await client.get(cover_url, follow_redirects=True)
        if cover_resp.status_code != 200:
            return None

        # Verify we got an actual image (Open Library returns a 1x1 pixel for missing covers)
        if len(cover_resp.content) < 1000:
            return None

        dest = covers_dir / f"{book_id}.jpg"
        dest.write_bytes(cover_resp.content)
        return dest
