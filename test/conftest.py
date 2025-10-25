import pytest
import fitz
from pathlib import Path
@pytest.fixture(scope="session")
def test_pdf_path():
    base_path = Path(__file__).resolve().parent
    pdf_path = base_path / "files" / "test_simple_pdf.pdf"

    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Hello pytest fixture!")
    doc.save(pdf_path)
    doc.close()
    return pdf_path
