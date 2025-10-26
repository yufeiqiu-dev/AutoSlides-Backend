import fitz  # PyMuPDF
from pathlib import Path
import pytest

@pytest.fixture(scope="session")
def test_pdf_path():
    """Ensure a valid test PDF exists and return its path."""
    base_path = Path(__file__).resolve().parent
    pdf_dir = base_path / "files"
    pdf_dir.mkdir(exist_ok=True)
    pdf_path = pdf_dir / "test_simple_pdf.pdf"

    try:
        # Try opening it to confirm it's a valid PDF
        with fitz.open(pdf_path) as doc:
            _ = doc.page_count
        # If we got here, the PDF is valid
        return pdf_path

    except Exception:
        # Create a new valid PDF if missing or corrupted
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), "Hello pytest fixture!")
        doc.save(pdf_path)
        doc.close()
        return pdf_path
