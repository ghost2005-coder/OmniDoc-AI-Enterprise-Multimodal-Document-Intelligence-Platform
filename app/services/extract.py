from pathlib import Path
from pypdf import PdfReader

def extract_text_from_pdf(data: bytes) -> str:
    import io
    reader = PdfReader(io.BytesIO(data))
    return "\n".join(page.extract_text() or "" for page in reader.pages).strip()

def extract_text_from_image(data: bytes) -> str:
    import io
    from PIL import Image
    import pytesseract
    return pytesseract.image_to_string(Image.open(io.BytesIO(data))).strip()

def extract_by_filename(filename: str, data: bytes) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix == ".pdf": return extract_text_from_pdf(data)
    if suffix in {".txt", ".md", ".csv", ".json"}: return data.decode("utf-8", errors="replace").strip()
    if suffix in {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}:
        try: return extract_text_from_image(data)
        except ImportError as exc: raise ValueError("Image OCR requires Pillow, pytesseract, and system Tesseract") from exc
    raise ValueError("Supported types: PDF, TXT, MD, CSV, JSON, PNG, JPG, TIFF, BMP")
