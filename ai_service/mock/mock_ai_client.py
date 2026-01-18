"""Mock AI client for development mode - complete implementation."""

import json
import logging
from typing import Optional, Callable

from ai_service.mock.mock_data import get_mock_analysis, MOCK_STOCKS

logger = logging.getLogger(__name__)


class MockAIClient:
    """Mock AI client that returns pre-defined responses without API calls.
    
    Implements the same interface as GeminiClient, OpenAIClient, etc.
    All responses are deterministic and based on mock data.
    """
    
    def __init__(self, settings=None, model: str = "mock-ai-v1"):
        self.settings = settings
        self.model = model
        self._callback = None
        self._on_wait_start: Optional[Callable] = None
        self._on_wait_tick: Optional[Callable] = None
        logger.info("MockAIClient initialized - NO external API calls will be made")
    
    @property
    def status_callback(self):
        """Status callback for progress updates."""
        return self._callback
    
    @status_callback.setter
    def status_callback(self, callback):
        self._callback = callback
    
    @property
    def on_wait_start(self) -> Optional[Callable]:
        """Callback when waiting starts."""
        return self._on_wait_start
    
    @on_wait_start.setter
    def on_wait_start(self, value: Callable):
        self._on_wait_start = value
    
    @property
    def on_wait_tick(self) -> Optional[Callable]:
        """Callback for each second of waiting."""
        return self._on_wait_tick
    
    @on_wait_tick.setter
    def on_wait_tick(self, value: Callable):
        self._on_wait_tick = value
    
    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
        max_output_tokens: int = 8192,
        max_retries: int = 3,
        model: Optional[str] = None,
    ) -> str:
        """Generate mock response based on prompt content.
        
        Detects ticker from prompt and returns corresponding mock analysis.
        Returns JSON string matching the expected EssayGenerator format.
        
        Args:
            prompt: The generation prompt
            system_instruction: Optional system instruction (ignored in mock)
            temperature: Generation temperature (ignored in mock)
            max_output_tokens: Max tokens (ignored in mock)
            max_retries: Retry count (ignored in mock)
            model: Model override (ignored in mock)
            
        Returns:
            JSON string with mock analysis
        """
        logger.info(f"MockAI: Generating response (prompt length: {len(prompt)} chars)")
        
        # Detect ticker from prompt
        ticker = self._detect_ticker(prompt)
        logger.info(f"MockAI: Detected ticker: {ticker}")
        
        # Get mock analysis for ticker
        analysis = get_mock_analysis(ticker)
        
        # Return as JSON string (matching real AI behavior)
        return json.dumps(analysis, ensure_ascii=False)
    
    def _detect_ticker(self, text: str) -> str:
        """Detect stock ticker from text.
        
        Args:
            text: Text to search for ticker
            
        Returns:
            Detected ticker or default "ACME"
        """
        text_upper = text.upper()
        
        # Check for known mock tickers
        for ticker in MOCK_STOCKS.keys():
            if ticker in text_upper:
                return ticker
        
        # Check for company names
        for ticker, info in MOCK_STOCKS.items():
            if info["name"].upper() in text_upper:
                return ticker
        
        # Default fallback
        return "ACME"
    
    def analyze_text(self, text: str, analysis_type: str = "summarize") -> str:
        """Mock text analysis.
        
        Args:
            text: Text to analyze
            analysis_type: Type of analysis (summarize, sentiment, etc.)
            
        Returns:
            Mock analysis result
        """
        logger.info(f"MockAI: Analyzing text ({len(text)} chars, type: {analysis_type})")
        
        if analysis_type == "summarize":
            # Return truncated text as summary
            if len(text) > 300:
                return text[:300] + "... [Mock AI Summary]"
            return text + " [Mock AI Summary]"
        
        elif analysis_type == "sentiment":
            return "positive"  # Default mock sentiment
        
        else:
            return f"Mock {analysis_type} analysis of {len(text)} characters."
    
    def summarize_article(
        self, title: str, text: str, max_words: int = 100
    ) -> str:
        """Mock article summarization.
        
        Args:
            title: Article title
            text: Article content
            max_words: Maximum words in summary
            
        Returns:
            Mock summary
        """
        logger.info(f"MockAI: Summarizing article: {title[:50]}...")
        
        # Create mock summary from title and truncated text
        summary_text = text[:500] if len(text) > 500 else text
        return f"{title}: {summary_text[:200]}... [Mock Summary]"
    
    def extract_entities(self, text: str) -> dict:
        """Mock entity extraction.
        
        Args:
            text: Text to extract entities from
            
        Returns:
            Dictionary with mock entities
        """
        logger.info(f"MockAI: Extracting entities from {len(text)} chars")
        
        # Find any mock tickers mentioned
        tickers_found = []
        text_upper = text.upper()
        for ticker in MOCK_STOCKS.keys():
            if ticker in text_upper:
                tickers_found.append(ticker)
        
        return {
            "tickers": tickers_found or ["ACME"],
            "companies": [MOCK_STOCKS.get(t, {}).get("name", t) for t in tickers_found],
            "sectors": list(set(MOCK_STOCKS.get(t, {}).get("sector", "Unknown") for t in tickers_found))
        }
