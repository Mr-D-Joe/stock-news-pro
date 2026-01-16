"""Unit tests for GeminiClient."""

import pytest
from unittest.mock import MagicMock, patch
from ai_service.analyzers.gemini_client import GeminiClient, GeminiError

@pytest.fixture
def mock_settings():
    settings = MagicMock()
    settings.gemini_api_key = "test_key"
    settings.gemini_model = "gemini-3-flash-preview"
    settings.gemini_summary_model = "gemma-3-27b-it"
    # Add new config fields
    settings.gemini_fallback_model = "gemini-2.0-flash"
    settings.request_timeout_seconds = 120
    settings.rate_limit_requests_per_minute = 5
    settings.rate_limit_wait_threshold_seconds = 600
    settings.rate_limit_cumulative_threshold_seconds = 300
    return settings

def test_gemini_init(mock_settings):
    client = GeminiClient(mock_settings)
    assert client.api_key == "test_key"
    assert client.default_model == "gemini-3-flash-preview"

def test_gemini_init_no_key():
    settings = MagicMock()
    settings.gemini_api_key = ""
    with pytest.raises(GeminiError, match="GEMINI_API_KEY is required"):
        GeminiClient(settings)

@patch("requests.Session.post")
def test_generate_success(mock_post, mock_settings):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "candidates": [
            {"content": {"parts": [{"text": "Generated text"}]}}
        ]
    }
    mock_post.return_value = mock_resp
    
    client = GeminiClient(mock_settings)
    result = client.generate("Test prompt")
    assert result == "Generated text"
    mock_post.assert_called_once()

@patch("requests.Session.post")
def test_generate_rate_limit_retry(mock_post, mock_settings):
    # Mock 429 then 200
    mock_429 = MagicMock()
    mock_429.status_code = 429
    mock_429.headers = {"Retry-After": "1"}
    
    mock_200 = MagicMock()
    mock_200.status_code = 200
    mock_200.json.return_value = {
        "candidates": [
            {"content": {"parts": [{"text": "Success after retry"}]}}
        ]
    }
    
    mock_post.side_effect = [mock_429, mock_200]
    
    client = GeminiClient(mock_settings)
    # Patch wait_with_feedback to avoid actual sleeping
    with patch.object(client, "_wait_with_feedback"):
        result = client.generate("Test prompt")
        assert result == "Success after retry"
        assert mock_post.call_count == 2
