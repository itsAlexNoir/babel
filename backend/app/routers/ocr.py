from fastapi import APIRouter, HTTPException, UploadFile
from PIL import Image

from ..schemas import OCRResult
from ..services.ocr_service import process_images

router = APIRouter(prefix="/api/ocr", tags=["ocr"])


@router.post("/extract", response_model=OCRResult)
async def extract_book_data(files: list[UploadFile]):
    if not files:
        raise HTTPException(status_code=400, detail="At least one image file is required")

    images: list[Image.Image] = []
    for f in files:
        if f.content_type and not f.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail=f"File '{f.filename}' is not an image")
        try:
            img = Image.open(f.file)
            images.append(img)
        except Exception:
            raise HTTPException(status_code=400, detail=f"Could not read image '{f.filename}'")

    result = process_images(images)
    return result
