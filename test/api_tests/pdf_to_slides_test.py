import io
import pytest
from app.app import create_app

@pytest.fixture
def client():
    """Create a Flask test client."""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_pdf2slides_success(client, mocker, test_pdf_path):
    """Test uploading a valid PDF file and receiving a PPTX file."""
    with open(test_pdf_path, "rb") as f:
        pdf_bytes = io.BytesIO(f.read())
        pdf_bytes.name = "test_simple_pdf.pdf"
    mocker.patch.dict("os.environ", {"GOOGLE_API_KEY": "FAKE_KEY"})
    mock_model_instance = mocker.MagicMock()
    mock_model_instance.generate_content.return_value.text = '{"title": "Mocked slide content", "slides": [{"header": "Title", "bullets": "One point"}]}'
    mocker.patch(
        'app.tools.TextToSlideContent.genai.GenerativeModel',
        return_value=mock_model_instance
    )
    response = client.post(
        "/pdf2slides",
        data={"file": (pdf_bytes, pdf_bytes.name)},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith(
        "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )
    assert response.data[:4] != b""  # check that some file content was returned


def test_no_gemini_api_key(client, mocker, test_pdf_path):
    """Test 500 error when no gemini api key in the environment"""
    mocker.patch.dict("os.environ", {}, clear=True)
    with open(test_pdf_path, "rb") as f:
        pdf_bytes = io.BytesIO(f.read())
        pdf_bytes.name = "test_simple_pdf.pdf"
    mock_model_instance = mocker.MagicMock()
    mocker.patch(
        'app.tools.TextToSlideContent.genai.GenerativeModel',
        return_value=mock_model_instance
    )
    response = client.post(
        "/pdf2slides",
        data={"file": (pdf_bytes, pdf_bytes.name)},
        content_type="multipart/form-data",
    )

    assert response.status_code == 500

def test_not_a_pdf_file(client):
    """Uploading a non-PDF file should return 400 with an error message."""
    # Create an in-memory fake .txt file
    fake_txt = io.BytesIO(b"Hello, I am not a PDF file")
    fake_txt.name = "not_a_pdf.txt"

    response = client.post(
        "/pdf2slides",
        data={"file": (fake_txt, fake_txt.name)},
        content_type="multipart/form-data",
    )

    # Assertions
    assert response.status_code == 400
    assert "error" in response.json
