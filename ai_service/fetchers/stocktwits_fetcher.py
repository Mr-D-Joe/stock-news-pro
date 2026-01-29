"""StockTwits fetcher for real-time trader sentiment."""

import logging
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass
import requests

logger = logging.getLogger(__name__)

@dataclass
class StockTwit:
    """Represents a StockTwits message."""
    ticker: str
    body: str
    username: str
    sentiment: Optional[str]  # "Bullish", "Bearish", or None
    url: str
    published: Optional[datetime] = None
    likes: int = 0
    is_rumor: bool = True


class StockTwitsFetcher:
    """Fetches messages from StockTwits public API."""
    
    BASE_URL = "https://api.stocktwits.com/api/2/streams/symbol"
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "StockNewsPro/1.0"
        })

    async def fetch_for_ticker(self, ticker: str, max_items: int = 15) -> List[StockTwit]:
        """
        Fetch messages for a ticker from StockTwits.
        Uses the free public API (no auth needed).
        """
        messages = []
        
        try:
            url = f"{self.BASE_URL}/{ticker}.json"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 404:
                logger.info(f"StockTwits: No stream for {ticker}")
                return []
                
            if response.status_code == 429:
                logger.warning("StockTwits rate limit hit")
                return []
                
            response.raise_for_status()
            data = response.json()
            
            for msg in data.get("messages", [])[:max_items]:
                # Parse timestamp
                created = msg.get("created_at")
                published = None
                if created:
                    try:
                        published = datetime.strptime(created, "%Y-%m-%dT%H:%M:%SZ")
                    except Exception as e:
                        logger.debug(f"Failed to parse StockTwits date: {e}")
                
                # Extract sentiment
                entities = msg.get("entities", {})
                sentiment_data = entities.get("sentiment")
                sentiment = sentiment_data.get("basic") if sentiment_data else None
                
                messages.append(StockTwit(
                    ticker=ticker,
                    body=msg.get("body", ""),
                    username=msg.get("user", {}).get("username", "anonymous"),
                    sentiment=sentiment,
                    url=f"https://stocktwits.com/{msg.get('user', {}).get('username', '')}/message/{msg.get('id', '')}",
                    published=published,
                    likes=msg.get("likes", {}).get("total", 0),
                    is_rumor=True
                ))
            
            logger.info(f"StockTwits: {len(messages)} messages for {ticker}")
            
        except Exception as e:
            logger.warning(f"StockTwits fetch failed for {ticker}: {e}")
        
        return messages


# Singleton
_stocktwits_fetcher: Optional[StockTwitsFetcher] = None

def get_stocktwits_fetcher() -> StockTwitsFetcher:
    global _stocktwits_fetcher
    if _stocktwits_fetcher is None:
        _stocktwits_fetcher = StockTwitsFetcher()
    return _stocktwits_fetcher
