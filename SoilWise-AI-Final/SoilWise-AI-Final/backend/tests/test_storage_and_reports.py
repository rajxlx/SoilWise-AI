from io import BytesIO
from types import SimpleNamespace

import pytest
from PIL import Image
from starlette.datastructures import UploadFile as StarletteUploadFile

from app.services.storage import save_image
from app.services.reports import make_report


@pytest.mark.asyncio
async def test_image_is_normalized_to_jpeg(tmp_path, monkeypatch):
    monkeypatch.setattr("app.services.storage.settings.upload_dir", str(tmp_path))
    source = BytesIO()
    Image.new("RGB", (32, 24), "green").save(source, format="PNG")
    source.seek(0)
    upload = StarletteUploadFile(filename="soil.png", file=source, headers={"content-type": "image/png"})
    saved = await save_image(upload)
    assert saved is not None
    with Image.open(saved) as image:
        assert image.format == "JPEG"
        assert image.size == (32, 24)


@pytest.mark.asyncio
async def test_upload_rejects_mismatched_mime(tmp_path):
    upload = StarletteUploadFile(filename="soil.txt", file=BytesIO(b"not an image"),
                                 headers={"content-type": "text/plain"})
    with pytest.raises(Exception) as exc:
        await save_image(upload)
    assert getattr(exc.value, "status_code", None) == 415


def test_pdf_wraps_long_untrusted_text():
    long_text = "Field <script> & " + ("long recommendation " * 180)
    record = SimpleNamespace(
        field_name=long_text, health_score=60, nitrogen=10, phosphorus=12,
        potassium=14, ph=5.2, organic_matter=0.4, moisture=8,
        diagnosis={"issues": [{"nutrient": "N", "message": long_text}]},
        recommendations=[{"title": long_text, "detail": long_text} for _ in range(20)],
    )
    pdf = make_report(record)
    assert pdf.startswith(b"%PDF")
    assert len(pdf) > 1500
