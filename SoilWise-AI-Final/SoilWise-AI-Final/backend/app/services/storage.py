from pathlib import Path
from uuid import uuid4
from io import BytesIO
import warnings
from PIL import Image, ImageOps, UnidentifiedImageError
from fastapi import UploadFile, HTTPException
from app.core.config import settings

ALLOWED = {"image/jpeg", "image/png", "image/webp"}
MAX_PIXELS = 20_000_000

async def save_image(file: UploadFile | None) -> str | None:
    if file is None:
        return None
    if file.content_type not in ALLOWED:
        raise HTTPException(status_code=415, detail="Upload a JPEG, PNG or WebP image.")
    raw = await file.read(settings.max_upload_mb * 1024 * 1024 + 1)
    if len(raw) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Image exceeds upload limit.")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            image = Image.open(BytesIO(raw))
            if image.width * image.height > MAX_PIXELS:
                raise HTTPException(status_code=413, detail="Image dimensions are too large.")
            image.verify()
            image = ImageOps.exif_transpose(Image.open(BytesIO(raw))).convert("RGB")
        image.thumbnail((1600, 1600))
        folder = Path(settings.upload_dir)
        folder.mkdir(parents=True, exist_ok=True)
        name = f"{uuid4().hex}.jpg"
        path = folder / name
        image.save(path, format="JPEG", quality=85, optimize=True)
        return str(path)
    except HTTPException:
        raise
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError, Image.DecompressionBombWarning):
        raise HTTPException(status_code=400, detail="Invalid or unsafe image file.")
