"""Unit tests for EssayGenerator."""

import pytest
import json
from unittest.mock import MagicMock, patch
from ai_service.analyzers.essay_generator import EssayGenerator
from ai_service.models.article import ArticleCollection, Article
from ai_service.pipeline.base import PipelineContext, PipelineConfig
from datetime import datetime

@pytest.fixture
def mock_settings():
    settings = MagicMock()
    settings.gemini_api_key = "test_key"
    settings.openai_api_key = "test_openai_key"
    settings.default_language = "German"
    settings.enable_anomaly_detection = False
    settings.max_articles_for_ai = 20
    return settings

@pytest.fixture
def sample_json_response():
    """Sample JSON response matching the new essay_generator structure."""
    return json.dumps({
        "essay": "This is a test executive summary covering main points of the biotech sector analysis.",
        "summary": "Growth is stable with minimal risks.",
        "swot": {
            "strengths": ["Strong R&D pipeline"],
            "weaknesses": ["High burn rate"],
            "opportunities": ["Market expansion"],
            "threats": ["Regulatory hurdles"]
        },
        "buffett_view": "A good long-term investment.",
        "lynch_view": "PEG ratio is favorable.",
        "outlook": "Positive 12-month outlook.",
        "key_findings": ["Finding 1: Growth is stable.", "Finding 2: Risks are minimal."],
        "watch_items": ["FDA decision on drug X"]
    })

@patch("ai_service.analyzers.provider_factory.ProviderFactory.get_client")
def test_essay_extraction(mock_get_client, mock_settings, sample_json_response):
    mock_client = MagicMock()
    mock_client.generate.return_value = sample_json_response
    mock_get_client.return_value = mock_client
    
    generator = EssayGenerator(settings=mock_settings)
    
    # Mock data
    articles = ArticleCollection(
        articles=[Article(title="Test", link="http://test.com", source="Test", published=datetime.now(), summary="Test summary")],
        query_stocks=["ABSI"]
    )
    
    # Use real context object
    config = PipelineConfig(
        stocks=["ABSI"],
        sectors=["biotech"],
        language="German"
    )
    context = PipelineContext(config=config)
    
    result = generator.process(articles, context)
    
    # Updated assertions for JSON-based output
    assert "executive summary" in result.essay.lower() or "biotech" in result.essay.lower()
    assert len(result.key_findings) == 2
    assert "Finding 1" in result.key_findings[0]
    assert "strengths" in result.swot
    assert "Strong R&D pipeline" in result.swot["strengths"][0]
    assert len(result.watch_items) == 1

