import pytest
from app.tools.TextToSlideContent import generate_slide_content, build_prompt


def test_build_prompt_creates_correct_structure():
    """Tests that the prompt includes the paper text."""
    test_text = "This is a test paper."
    prompt = build_prompt(test_text)

    # Use simple 'assert' statements
    assert test_text in prompt
    assert "You are an expert presentation creator" in prompt


def test_generate_content_with_empty_input():
    """Tests that an empty paper text raises a ValueError."""
    # Use pytest.raises to check for exceptions
    with pytest.raises(ValueError):
        generate_slide_content("")


def test_generate_slide_content_with_mock_api(mocker):
    """
    Tests the main function by mocking the Gemini API call using the 'mocker' fixture.
    """
    # 1. Use mocker to patch the GenerativeModel class
    mocker.patch.dict("os.environ", {"GOOGLE_API_KEY": "FAKE_KEY"})
    mock_model_instance = mocker.MagicMock()
    mock_model_instance.generate_content.return_value.text = "Mocked slide content"
    mocker.patch(
        'app.tools.TextToSlideContent.genai.GenerativeModel',
        return_value=mock_model_instance
    )

    # 2. Call the function with sample paper text
    paper_text = "This is a test paper about RAG."
    result = generate_slide_content(paper_text)

    # 3. Assert that the function returned the mocked data
    assert result == "Mocked slide content"

    # 4. Assert that the API was called with the correct prompt
    mock_model_instance.generate_content.assert_called_once()
    called_prompt = mock_model_instance.generate_content.call_args[0][0]
    assert paper_text in called_prompt