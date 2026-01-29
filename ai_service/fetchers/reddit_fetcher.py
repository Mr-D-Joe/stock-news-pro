"""Reddit news fetcher for stock-related posts and rumors."""

import logging
from datetime import datetime
from typing import List, Optional, Union
from dataclasses import dataclass
import requests

logger = logging.getLogger(__name__)

@dataclass
class RedditPost:
    """Represents a Reddit post about a stock."""
    ticker: str
    title: str
    subreddit: str
    score: int
    url: str
    published: Optional[datetime] = None
    selftext: Optional[str] = None
    num_comments: int = 0
    is_rumor: bool = True  # Community posts are flagged as potential rumors


class RedditFetcher:
    """Fetches stock-related posts from Reddit using the public JSON API."""
    
    SUBREDDITS = ["stocks", "investing", "wallstreetbets", "stockmarket"]
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "StockNewsPro/1.0 (Reddit News Aggregator)"
        })

    async def fetch_for_ticker(self, ticker: str, max_items: int = 10) -> List[RedditPost]:
        """
        Search Reddit for posts mentioning the ticker.
        Uses Reddit's public JSON API (no auth required for read).
        """
        posts = []
        
        for subreddit in self.SUBREDDITS:
            try:
                # Reddit JSON API: search within subreddit
                url = f"https://www.reddit.com/r/{subreddit}/search.json"
                params: dict[str, Union[str, int]] = {
                    "q": ticker,
                    "restrict_sr": "on",
                    "sort": "new",
                    "limit": max_items,
                    "t": "week"  # Last week
                }
                
                response = self.session.get(url, params=params, timeout=self.timeout)
                
                if response.status_code == 429:
                    logger.warning(f"Reddit rate limit hit for r/{subreddit}")
                    continue
                    
                response.raise_for_status()
                data = response.json()
                
                for child in data.get("data", {}).get("children", []):
                    post_data = child.get("data", {})
                    
                    # Parse timestamp
                    created = post_data.get("created_utc")
                    published = datetime.fromtimestamp(created) if created else None
                    
                    posts.append(RedditPost(
                        ticker=ticker,
                        title=post_data.get("title", "No title"),
                        subreddit=subreddit,
                        score=post_data.get("score", 0),
                        url=f"https://reddit.com{post_data.get('permalink', '')}",
                        published=published,
                        selftext=post_data.get("selftext", "")[:500] if post_data.get("selftext") else None,
                        num_comments=post_data.get("num_comments", 0),
                        is_rumor=True
                    ))
                    
                logger.info(f"Reddit r/{subreddit}: {len([p for p in posts if p.subreddit == subreddit])} posts for {ticker}")
                
            except Exception as e:
                logger.warning(f"Reddit fetch failed for r/{subreddit}: {e}")
        
        # Sort by score (popularity)
        posts.sort(key=lambda x: x.score, reverse=True)
        
        return posts[:max_items]


# Singleton
_reddit_fetcher: Optional[RedditFetcher] = None

def get_reddit_fetcher() -> RedditFetcher:
    global _reddit_fetcher
    if _reddit_fetcher is None:
        _reddit_fetcher = RedditFetcher()
    return _reddit_fetcher
