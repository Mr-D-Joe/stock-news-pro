import pytest
import json
from unittest.mock import MagicMock, AsyncMock, patch
from datetime import datetime

from ai_service.models.article import Article, ArticleCollection
from ai_service.pipeline.base import PipelineContext, PipelineConfig
from ai_service.processors.browser_extractor import BrowserExtractor
from ai_service.analyzers.essay_generator import EssayGenerator
from ai_service.main import analyze_essay

@pytest.mark.asyncio
async def test_end_to_end_pipeline():
    """
    Simulates the full flow:
    1. Input Articles (Headlines only)
    2. Browser Extraction (Simulated) -> Full Text
    3. Essay Generation (Simulated AI) -> Report
    """
    
    # 1. Setup Mock Browser
    with patch("ai_service.processors.browser_extractor.BrowserExtractor._extract_text_from_url", new_callable=AsyncMock) as mock_extract:
        mock_extract.return_value = "This is the full text content extracted from the website. It contains specific details about the stock performance."
        
        # 2. Setup Mock AI Provider - return valid JSON
        with patch("ai_service.analyzers.provider_factory.ProviderFactory.get_client") as mock_get_client:
            mock_ai_client = MagicMock()
            mock_ai_client.generate.return_value = json.dumps({
                "essay": "Integration Report: This confirms that the pipeline successfully integrated browser content with AI analysis.",
                "summary": "Pipeline integration successful.",
                "swot": {
                    "strengths": ["Good integration"],
                    "weaknesses": ["None identified"],
                    "opportunities": ["Expansion"],
                    "threats": ["Competition"]
                },
                "key_findings": ["Finding 1: Browser extraction worked.", "Finding 2: AI processing worked."],
                "watch_items": ["Monitor performance"],
                "buffett_view": "Solid fundamentals.",
                "lynch_view": "PEG is favorable.",
                "outlook": "Positive outlook."
            })
            mock_get_client.return_value = mock_ai_client
            
            # 3. Create Input Data
            input_collection = ArticleCollection(
                articles=[
                    Article(
                        title="Stock Market Update",
                        link="http://example.com/news",
                        source="TechCrunch",
                        published=datetime.now(),
                        summary="Short summary..."
                    )
                ],
                query_stocks=["AAPL"],
                query_sectors=["Tech"]
            )
            
            # 4. Run the Pipeline Endpoint Logic
            result = await analyze_essay(request=input_collection, use_browser=True)
            
            # 5. Verify Results
            
            # Verify Browser was called
            assert mock_extract.called, "Browser extractor should have been called"
            
            # Verify AI Output structure (updated for JSON-based response)
            assert "Integration Report" in result.essay
            assert len(result.key_findings) > 0
            assert "AnalysisResult" in str(type(result))

