import pytest
from app.tools.pdf_parser import extract_text, extract_images, parse_pdf
from werkzeug.datastructures import FileStorage

def test_parsing_none():
    with pytest.raises(FileNotFoundError):
        parse_pdf(None)

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
    """Simulate actual uploaded file (like Postman)"""
    with open(test_pdf_path, "rb") as f:
        upload = FileStorage(
            stream=f,                      
            filename="test.pdf",           
            content_type="application/pdf" 
        )
        parsed = parse_pdf(upload)         
    assert "Hello" in parsed["text"]