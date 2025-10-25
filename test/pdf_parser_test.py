import pytest
from pathlib import Path
from app.tools.pdf_parser import extract_text, extract_images, parse_pdf

import fitz

# generate small pdf
@pytest.fixture(scope="session")
def test_pdf_path():
    """Create a single PDF file once for all tests."""
    base_path = Path(__file__).resolve().parent  # tests/
    pdf_path = base_path / "files" / "test_simple_pdf.pdf"

    # Create the file once
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Hello from shared test PDF!")
    doc.save(pdf_path)
    doc.close()
    return pdf_path

def test_extract_text(test_pdf_path):
    """Test if text can be extracted from test pdf"""
    with open(test_pdf_path, "rb") as f:
        pdf_bytes = f.read()
    text = extract_text(pdf_bytes)
    assert "Hello" in text

def test_extract_images_empty(test_pdf_path):
    """Test extracting empty image """
    with open(test_pdf_path, "rb") as f:
        pdf_bytes = f.read()
    imgs = extract_images(pdf_bytes)
    assert isinstance(imgs, list)
    assert len(imgs) == 0  # no images in our fake PDF

def test_parse_pdf(test_pdf_path):
    """Test pdf parsing function"""
    with open(test_pdf_path, "rb") as f:
        parsed = parse_pdf(f)
    assert "Hello from shared test PDF!" in parsed["text"]
