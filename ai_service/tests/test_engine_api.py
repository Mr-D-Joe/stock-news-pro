"""Tests for Engine API endpoints."""

import pytest
from fastapi.testclient import TestClient

from ai_service.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_caches():
    """Clear caches before each test."""
    global _news_cache, _analysis_cache
    from ai_service.api import engine
    engine._news_cache = []
    engine._analysis_cache = {}
    yield
    engine._news_cache = []
    engine._analysis_cache = {}


class TestNewsEndpoints:
    """Test news submission and retrieval."""
    
    def test_submit_news_success(self, client):
        """Test submitting news items."""
        payload = {
            "items": [
                {
                    "ticker": "AAPL",
                    "title": "Apple Reports Strong Earnings",
                    "source": "Reuters"
                },
                {
                    "ticker": "GOOGL",
                    "title": "Google AI Announcement",
                    "source": "TechCrunch"
                }
            ],
            "request_analysis": False
        }
        
        response = client.post("/api/engine/news", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["processed"] == 2
        assert data["analysis_triggered"] is False
        assert "Successfully processed" in data["message"]
    
    def test_submit_news_with_analysis_trigger(self, client):
        """Test submitting news with analysis request."""
        payload = {
            "items": [
                {
                    "ticker": "TSLA",
                    "title": "Tesla Production Update",
                    "source": "Bloomberg"
                }
            ],
            "request_analysis": True
        }
        
        response = client.post("/api/engine/news", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["analysis_triggered"] is True
    
    def test_get_cached_news(self, client):
        """Test retrieving cached news."""
        # First submit some news
        payload = {
            "items": [
                {"ticker": "MSFT", "title": "Microsoft News", "source": "CNN"}
            ],
            "request_analysis": False
        }
        client.post("/api/engine/news", json=payload)
        
        # Then retrieve
        response = client.get("/api/engine/news")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total"] == 1
        assert len(data["items"]) == 1
    
    def test_get_cached_news_by_ticker(self, client):
        """Test filtering news by ticker."""
        # Submit mixed tickers
        payload = {
            "items": [
                {"ticker": "AAPL", "title": "Apple News", "source": "A"},
                {"ticker": "GOOGL", "title": "Google News", "source": "B"},
                {"ticker": "AAPL", "title": "More Apple News", "source": "C"}
            ],
            "request_analysis": False
        }
        client.post("/api/engine/news", json=payload)
        
        # Filter by AAPL
        response = client.get("/api/engine/news?ticker=AAPL")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["items"]) == 2  # Only AAPL items


class TestAnalysisEndpoints:
    """Test analysis request and caching."""
    
    @pytest.mark.integration
    def test_request_analysis_success(self, client):
        """Test requesting AI analysis (integration test - uses real AI)."""
        # First submit news for the ticker
        news_payload = {
            "items": [
                {"ticker": "ABSI", "title": "Absci News", "source": "Test", "url": "http://example.com"}
            ],
            "request_analysis": False
        }
        client.post("/api/engine/news", json=news_payload)
        
        # Then request analysis
        analysis_payload = {
            "tickers": ["ABSI"],
            "language": "German"
        }
        
        response = client.post("/api/engine/analyze", json=analysis_payload)
        assert response.status_code == 200
        
        data = response.json()
        # Verify structure, not exact content (AI responses vary)
        assert "essay" in data and len(data["essay"]) > 0
        assert "sentiment" in data
        assert "generated_at" in data
    
    def test_request_analysis_no_cached_news(self, client):
        """Test analysis with no cached news."""
        analysis_payload = {
            "tickers": ["UNKNOWN"],
            "language": "German"
        }
        
        response = client.post("/api/engine/analyze", json=analysis_payload)
        assert response.status_code == 404
        assert "No cached news" in response.json()["detail"]
    
    def test_get_cached_analysis_not_found(self, client):
        """Test retrieving non-existent cached analysis."""
        response = client.get("/api/engine/analyze/NOTCACHED")
        assert response.status_code == 404


class TestCacheManagement:
    """Test cache management endpoints."""
    
    def test_clear_cache(self, client):
        """Test clearing all caches."""
        # Add some data
        payload = {
            "items": [
                {"ticker": "TEST", "title": "Test", "source": "Test"}
            ],
            "request_analysis": False
        }
        client.post("/api/engine/news", json=payload)
        
        # Clear
        response = client.delete("/api/engine/cache")
        assert response.status_code == 200
        assert response.json()["cleared"] is True
        
        # Verify cleared
        response = client.get("/api/engine/news")
        assert response.json()["total"] == 0


class TestDBEndpoints:
    """Test database endpoints."""
    
    def test_store_record(self, client):
        """Test storing a record."""
        payload = {
            "ticker": "ABSI",
            "title": "Test Record",
            "category": "Biotech",
            "relevance": 0.85
        }
        
        response = client.post("/api/engine/db/store", json=payload)
        assert response.status_code == 200
        assert response.json()["stored"] is True
