"""Mock AI client for development mode."""

import logging
from typing import Optional
from ai_service.mock.mock_data import get_mock_analysis, MOCK_STOCKS

logger = logging.getLogger(__name__)


class MockAIClient:
    """Mock AI client that returns pre-defined responses without API calls."""
    
    def __init__(self, settings=None):
        self.settings = settings
        self._callback = None
        logger.info("MockAIClient initialized - NO external API calls will be made")
    
    @property
    def status_callback(self):
        return self._callback
    
    @status_callback.setter
    def status_callback(self, callback):
        self._callback = callback
    
    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate mock response based on prompt content."""
        logger.info(f"MockAI: Generating response (prompt length: {len(prompt)} chars)")
        
        # Detect ticker from prompt
        ticker = None
        for t in MOCK_STOCKS.keys():
            if t in prompt.upper():
                ticker = t
                break
        
        if not ticker:
            ticker = "ACME"  # Default
        
        analysis = get_mock_analysis(ticker)
        
        # Return JSON-formatted response for essay generator
        import json
        return json.dumps(analysis, ensure_ascii=False)
    
    def analyze_text(self, text: str, instruction: str) -> str:
        """Mock text analysis."""
        return f"Mock analysis of text ({len(text)} chars). Key points identified."
    
    def summarize_article(self, content: str, max_length: int = 200) -> str:
        """Mock article summarization."""
        if len(content) > max_length:
            return content[:max_length] + "..."
        return content
