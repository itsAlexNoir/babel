import re

from PIL import Image
import pytesseract

from ..schemas import OCRResult


def extract_text_from_image(image: Image.Image) -> str:
    """Run Tesseract OCR on a PIL Image and return the extracted text."""
    return pytesseract.image_to_string(image)


def parse_book_data(raw_text: str) -> OCRResult:
    """Parse raw OCR text and attempt to extract structured book fields."""
    lines = [line.strip() for line in raw_text.strip().splitlines() if line.strip()]

    result = OCRResult(raw_text=raw_text)

    if not lines:
        return result

    # Heuristic: the first prominent line is often the title
    result.title = lines[0] if lines else None

    # Look for author patterns: "by Author", "By Author Name"
    for i, line in enumerate(lines):
        by_match = re.match(r"^[Bb]y\s+(.+)$", line)
        if by_match:
            result.author = by_match.group(1).strip()
            break

    # If no "by" pattern, the second line is often the author
    if not result.author and len(lines) > 1:
        candidate = lines[1]
        # If it looks like a name (2-4 capitalized words, no numbers)
        if re.match(r"^[A-Z][a-z]+(?:\s+[A-Z]\.?\s*)?(?:\s+[A-Z][a-z]+){0,3}$", candidate):
            result.author = candidate

    # Look for publisher patterns
    publisher_keywords = [
        "press", "publishing", "publishers", "books", "editions",
        "editorial", "verlag", "ediciones", "edition",
    ]
    for line in lines:
        if any(kw in line.lower() for kw in publisher_keywords):
            result.publisher = line
            break

    # Extract year patterns (4-digit numbers between 1400 and 2030)
    years = re.findall(r"\b(1[4-9]\d{2}|20[0-2]\d)\b", raw_text)
    if years:
        # If multiple years, smallest is likely original pub date, largest is edition
        sorted_years = sorted(set(years))
        if len(sorted_years) >= 2:
            result.original_pub_date = sorted_years[0]
            result.publishing_date = sorted_years[-1]
        else:
            result.publishing_date = sorted_years[0]

    # Look for language indicators
    lang_patterns = {
        "english": "English",
        "spanish": "Spanish",
        "español": "Spanish",
        "french": "French",
        "français": "French",
        "german": "German",
        "deutsch": "German",
        "italian": "Italian",
        "italiano": "Italian",
        "portuguese": "Portuguese",
        "português": "Portuguese",
    }
    text_lower = raw_text.lower()
    for pattern, lang in lang_patterns.items():
        if pattern in text_lower:
            result.language = lang
            break

    return result


def process_images(images: list[Image.Image]) -> OCRResult:
    """Process multiple images and combine OCR results."""
    all_text_parts: list[str] = []
    for img in images:
        text = extract_text_from_image(img)
        if text.strip():
            all_text_parts.append(text)

    combined_text = "\n---\n".join(all_text_parts)
    return parse_book_data(combined_text)
