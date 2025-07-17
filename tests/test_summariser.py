import pytest
from unittest.mock import Mock
from summariser import generate_summary, configure_model, generate_intro


def test_generate_summary_valid_response():
    # Create a fake model object with mocked generate_content method
    mock_model = Mock()
    mock_response = Mock()
    mock_response.parts = True
    mock_response.text = (
        "• Summary point 1\n"
        "• Summary point 2\n"
        "• Summary point 3\n"
        "Topic: Market Trends\n"
        "Mentioned Companies: Tesla, Ørsted"
    )
    mock_model.generate_content.return_value = mock_response

    article_text = "Tesla expands battery production for grid-scale renewable projects."
    summary = generate_summary(mock_model, article_text)

    assert "Summary point" in summary
    assert "Topic:" in summary
    assert "Mentioned Companies:" in summary


def test_generate_summary_empty_response():
    mock_model = Mock()
    mock_response = Mock()
    mock_response.parts = False
    mock_model.generate_content.return_value = mock_response

    summary = generate_summary(mock_model, "Some article text")
    assert "[Error: Empty response" in summary


def test_generate_summary_api_exception():
    mock_model = Mock()
    mock_model.generate_content.side_effect = Exception("Connection failed")

    summary = generate_summary(mock_model, "Important article")
    assert "Error generating summary" in summary


def test_configure_model_success():
    mock_genai = Mock()
    mock_model = Mock()
    mock_chat = Mock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_model.start_chat.return_value = mock_chat

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("summariser.genai", mock_genai)
        model, chat = configure_model("fake_api_key")

    assert model == mock_model
    assert chat == mock_chat


def test_configure_model_failure():
    mock_genai = Mock()
    mock_genai.configure.side_effect = Exception("Invalid API key")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("summariser.genai", mock_genai)
        with pytest.raises(RuntimeError, match="Failed to configure Gemini model: Invalid API key"):
            configure_model("invalid_api_key")


def test_generate_intro_valid_response():
    mock_model = Mock()
    mock_response = Mock()
    mock_response.text = "This week, the sustainable finance sector saw significant developments..."
    mock_model.generate_content.return_value = mock_response

    summaries = [
        "• Summary point 1",
        "• Summary point 2",
        "• Summary point 3",
        "• Summary point 4",
        "• Summary point 5"
    ]
    intro = generate_intro(mock_model, summaries)

    assert "sustainable finance sector" in intro
    assert "significant developments" in intro


def test_generate_intro_api_exception():
    mock_model = Mock()
    mock_model.generate_content.side_effect = Exception("API error")

    summaries = [
        "• Summary point 1",
        "• Summary point 2",
        "• Summary point 3",
        "• Summary point 4",
        "• Summary point 5"
    ]
    with pytest.raises(Exception, match="API error"):
        generate_intro(mock_model, summaries)

    summary = generate_summary(mock_model, "Important article")
    assert "Error generating summary" in summary
