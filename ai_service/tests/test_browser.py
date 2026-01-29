import pytest
from unittest.mock import AsyncMock, patch
from ai_service.processors.browser_extractor import BrowserExtractor
from ai_service.models.article import Article, ArticleCollection

@pytest.fixture
def mock_playwright():
    with patch("ai_service.processors.browser_extractor.async_playwright") as mock_p:
        mock_context_manager = AsyncMock()
        mock_p.return_value = mock_context_manager
        
        mock_playwright_obj = AsyncMock()
        mock_context_manager.__aenter__.return_value = mock_playwright_obj
        
        mock_browser = AsyncMock()
        mock_playwright_obj.chromium.launch.return_value = mock_browser
        
        mock_browser_context = AsyncMock()
        mock_browser.new_context.return_value = mock_browser_context
        
        mock_page = AsyncMock()
        mock_browser_context.new_page.return_value = mock_page
        
        # Mock evaluate logic
        mock_page.evaluate.return_value = "Full article content extracted from browser."
        
        yield mock_page

@pytest.mark.asyncio
async def test_browser_extraction(mock_playwright):
    extractor = BrowserExtractor(max_concurrent=1)
    
    collection = ArticleCollection(
        articles=[
            Article(title="Test", link="http://example.com", source="Example", published="2024-01-01"),
        ],
        query_stocks=["ABSI"]
    )
    
    # We call _process_async directly to avoid asyncio.run conflict in test loop
    result = await extractor._process_async(collection)
    
    assert result.articles[0].content == "Full article content extracted from browser."
    mock_playwright.goto.assert_called_with("http://example.com", timeout=30000, wait_until="domcontentloaded")
