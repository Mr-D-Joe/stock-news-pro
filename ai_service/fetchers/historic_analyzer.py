"""Historical analysis of price data and pivotal news events."""

import logging
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import yfinance as yf
import json

from ai_service.config import Settings
from ai_service.analyzers.provider_factory import ProviderFactory

logger = logging.getLogger(__name__)

class HistoricAnalyzer:
    """Fetches historical price data and identifies pivotal stock-moving events."""
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = ProviderFactory.get_client("gemini", self.settings)
        return self._client

    async def get_fundamentals(self, ticker: str) -> Dict[str, Any]:
        """Fetch fundamental data (P/E, PEG, Analysts, etc.) with fallbacks."""
        import asyncio
        import os
        import requests
        from datetime import datetime
        
        # Simple file-based cache to avoid Rate Limits (429)
        cache_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache")
        os.makedirs(cache_dir, exist_ok=True)
        date_str = datetime.now().strftime("%Y-%m-%d")
        cache_file = os.path.join(cache_dir, f"fundamentals_{ticker}_{date_str}.json")

        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r") as f:
                    data = json.load(f)
                    # Only use cache if it has actual data
                    if data.get("pe_ratio") or data.get("business_summary"):
                        logger.info(f"Loaded fundamentals from cache for {ticker}")
                        return data
            except Exception as e:
                logger.warning(f"Cache read failed, ignoring: {e}")

        loop = asyncio.get_event_loop()
        fundamentals = {}
        
        # Try 1: yfinance with retry
        for attempt in range(3):
            try:
                def fetch_info():
                    stock = yf.Ticker(ticker)
                    return stock.info

                info = await loop.run_in_executor(None, fetch_info)
                
                if info and len(info) > 5:  # Valid response
                    fundamentals = {
                        "pe_ratio": info.get("forwardPE") or info.get("trailingPE"),
                        "peg_ratio": info.get("pegRatio"),
                        "roe": (info.get("returnOnEquity", 0) or 0) * 100,
                        "debt_to_equity": info.get("debtToEquity"),
                        "target_mean_price": info.get("targetMeanPrice"),
                        "target_high_price": info.get("targetHighPrice"),
                        "target_low_price": info.get("targetLowPrice"),
                        "recommendation": info.get("recommendationKey"),
                        "business_summary": info.get("longBusinessSummary"),
                        "sector": info.get("sector")
                    }
                    logger.info(f"Fetched fundamentals via yfinance for {ticker}")
                    break
            except Exception as e:
                if "429" in str(e) or "Too Many" in str(e):
                    wait_time = (attempt + 1) * 5
                    logger.warning(f"yfinance rate limited, waiting {wait_time}s (attempt {attempt+1}/3)")
                    await asyncio.sleep(wait_time)
                else:
                    logger.warning(f"yfinance attempt {attempt+1} failed: {e}")
                    break
        
        # Try 2: Direct Yahoo Quote API if yfinance failed
        if not fundamentals.get("pe_ratio"):
            try:
                url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={ticker}"
                resp = await loop.run_in_executor(None, lambda: requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"}))
                if resp.status_code == 200:
                    data = resp.json()
                    quote = data.get("quoteResponse", {}).get("result", [{}])[0]
                    if quote:
                        fundamentals.update({
                            "pe_ratio": fundamentals.get("pe_ratio") or quote.get("forwardPE") or quote.get("trailingPE"),
                            "target_mean_price": fundamentals.get("target_mean_price") or quote.get("targetMeanPrice"),
                            "recommendation": fundamentals.get("recommendation") or quote.get("recommendationKey"),
                        })
                        logger.info(f"Supplemented fundamentals via Yahoo Quote API for {ticker}")
            except Exception as e:
                logger.warning(f"Yahoo Quote API failed: {e}")

        # Try 3: Financial Modeling Prep (FMP) - better structured data
        if not fundamentals.get("pe_ratio") and self.settings.fmp_api_key:
            try:
                fmp_key = self.settings.fmp_api_key
                # Use /stable/ endpoint (v3 is legacy and no longer works for new users)
                url = f"https://financialmodelingprep.com/stable/profile?symbol={ticker}&apikey={fmp_key}"
                resp = await loop.run_in_executor(None, lambda: requests.get(url, timeout=10))
                if resp.status_code == 200:
                    data = resp.json()
                    if data and len(data) > 0:
                        profile = data[0]
                        # FMP stable endpoint has slightly different field names
                        fundamentals.update({
                            "pe_ratio": fundamentals.get("pe_ratio") or profile.get("pe"),
                            "market_cap": profile.get("marketCap"),
                            "beta": profile.get("beta"),
                            "business_summary": fundamentals.get("business_summary") or profile.get("description"),
                            "sector": fundamentals.get("sector") or profile.get("industry"),
                            "company_name": profile.get("companyName"),
                        })
                        logger.info(f"Fetched fundamentals via FMP for {ticker}: P/E={profile.get('pe')}")
                else:
                    logger.warning(f"FMP API returned status {resp.status_code}: {resp.text[:200]}")
                
                # Also get price target consensus from FMP
                target_url = f"https://financialmodelingprep.com/stable/price-target-consensus?symbol={ticker}&apikey={fmp_key}"
                resp2 = await loop.run_in_executor(None, lambda: requests.get(target_url, timeout=10))
                if resp2.status_code == 200:
                    targets = resp2.json()
                    if targets and len(targets) > 0:
                        target = targets[0]
                        fundamentals["target_mean_price"] = target.get("targetConsensus")
                        fundamentals["target_high_price"] = target.get("targetHigh")
                        fundamentals["target_low_price"] = target.get("targetLow")
                        logger.info(f"Added FMP price targets for {ticker}")
                        
            except Exception as e:
                logger.warning(f"FMP API failed: {e}")

        # Try 4: Finnhub API - has P/E, ROE, Debt/Equity in free tier
        if not fundamentals.get("pe_ratio") and self.settings.finnhub_api_key:
            try:
                fh_key = self.settings.finnhub_api_key
                url = f"https://finnhub.io/api/v1/stock/metric?symbol={ticker}&metric=all&token={fh_key}"
                resp = await loop.run_in_executor(None, lambda: requests.get(url, timeout=10))
                if resp.status_code == 200:
                    data = resp.json()
                    metric = data.get("metric", {})
                    if metric:
                        fundamentals.update({
                            "pe_ratio": fundamentals.get("pe_ratio") or metric.get("peBasicTTM") or metric.get("peExclExtraTTM"),
                            "peg_ratio": fundamentals.get("peg_ratio") or metric.get("pegRatio"),
                            "roe": fundamentals.get("roe") or metric.get("roeTTM"),
                            "debt_to_equity": fundamentals.get("debt_to_equity") or metric.get("currentDebtToEquityAnnual"),
                        })
                        if metric.get("peBasicTTM"):
                            logger.info(f"Fetched fundamentals via Finnhub for {ticker}: P/E={metric.get('peBasicTTM')}")
                else:
                    logger.warning(f"Finnhub API returned status {resp.status_code}")
            except Exception as e:
                logger.warning(f"Finnhub API failed: {e}")

        # Save to cache if we got data
        if fundamentals.get("pe_ratio") or fundamentals.get("business_summary"):
            try:
                with open(cache_file, "w") as f:
                    json.dump(fundamentals, f)
            except Exception as e:
                logger.warning(f"Failed to write cache: {e}")
                
        return fundamentals


    async def get_price_data(self, ticker: str, period: str = "10y") -> Dict[str, Any]:
        """
        Fetch historical price data with fallback providers.
        
        Tries in order:
        1. Yahoo Finance Chart API (direct, more reliable)
        2. yfinance library
        3. Finnhub (if API key available)
        """
        # Try Yahoo Chart API first (direct access, more reliable)
        result = await self._fetch_yahoo_chart(ticker, period)
        if result and "data" in result and result["data"]:
            logger.info(f"Yahoo Chart API: Got {len(result['data'])} points for {ticker}")
            return result
        
        # Fallback to yfinance library
        result = await self._fetch_yfinance(ticker, period)
        if result and "data" in result and result["data"]:
            logger.info(f"yfinance: Got {len(result['data'])} points for {ticker}")
            return result
        
        # Last resort: Finnhub (requires API key)
        result = await self._fetch_finnhub(ticker, period)
        if result and "data" in result and result["data"]:
            logger.info(f"Finnhub: Got {len(result['data'])} points for {ticker}")
            return result
        
        return {"error": "All providers failed", "ticker": ticker, "data": []}

    async def _fetch_yahoo_chart(self, ticker: str, period: str) -> Dict[str, Any]:
        """Direct Yahoo Finance Chart API call (more reliable than yfinance lib)."""
        
        period_map = {
            "10y": ("10y", "1wk"),
            "1y": ("1y", "1d"),
            "6mo": ("6mo", "1d"),
            "3mo": ("3mo", "1d"),
            "1mo": ("1mo", "1d"),
            "1wk": ("5d", "1h"),
            "1d": ("5d", "5m"),    # Fetch 5 days to ensure we get last trading day
            "24h": ("5d", "5m")    # Same - will filter to last trading day
        }
        
        range_val, interval = period_map.get(period, ("1y", "1d"))
        
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
            params = {"range": range_val, "interval": interval}
            headers = {"User-Agent": "Mozilla/5.0 StockNewsPro/1.0"}
            
            response = await self._run_request(url, params, headers)
            chart_data = response.json()
            result = chart_data.get("chart", {}).get("result", [])
            
            if not result:
                return {"error": "No data", "ticker": ticker}
            
            timestamps = result[0].get("timestamp", [])
            quotes = result[0].get("indicators", {}).get("quote", [{}])[0]
            
            closes = quotes.get("close", [])
            highs = quotes.get("high", [])
            lows = quotes.get("low", [])
            volumes = quotes.get("volume", [])
            
            data = []
            for i, ts in enumerate(timestamps):
                if closes[i] is not None:
                    # Keep native types for JSON serialization
                    data.append({
                        "date": datetime.fromtimestamp(ts).isoformat(),
                        "close": closes[i],
                        "high": highs[i] if highs else None,
                        "low": lows[i] if lows else None,
                        "volume": volumes[i] if volumes else 0
                    })
            
            last_price = data[-1]["close"] if data else 0
            
            return {
                "ticker": ticker, 
                "period": period,
                "data": data,
                "last_price": last_price,
                "source": "yahoo_chart"
            }
            
        except Exception as e:
            logger.warning(f"Yahoo Chart API failed for {ticker}: {e}")
            return {}

    async def _run_request(self, url, params, headers):
        """Async wrapper for requests."""
        import requests
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: requests.get(url, params=params, headers=headers, timeout=10))

    async def _fetch_yfinance(self, ticker: str, period: str) -> Dict[str, Any]:
        """Fallback to yfinance library."""
        try:
            # Run in executor to avoid blocking
            import asyncio
            loop = asyncio.get_event_loop()
            
            def get_hist():
                stock = yf.Ticker(ticker)
                return stock.history(period=period)
                
            hist = await loop.run_in_executor(None, get_hist)
            
            if hist.empty:
                return {}
                
            data = []
            for date, row in hist.iterrows():
                data.append({
                    "date": date.isoformat(),
                    "close": row["Close"],
                    "high": row["High"],
                    "low": row["Low"],
                    "volume": row["Volume"]
                })
            
            return {
                "ticker": ticker, 
                "period": period,
                "data": data,
                "last_price": data[-1]["close"] if data else 0,
                "source": "yfinance_lib"
            }
        except Exception as e:
            logger.warning(f"yfinance lib failed: {e}")
            return {}

    async def _fetch_finnhub(self, ticker: str, period: str) -> Dict[str, Any]:
        """Fetch from Finnhub (stub)."""
        # Implementation would go here if API key available
        return {}

    def slice_periods(self, full_data: Dict[str, Any], periods: List[str]) -> Dict[str, Dict]:
        """
        Slice full historical data (e.g. 10y) into smaller periods locally.
        Avoids multiple API calls by filtering data client-side.
        
        Args:
            full_data: Complete price data from a single API call
            periods: List of periods to slice ["10y", "1y", "6mo", etc.]
            
        Returns:
            Dict mapping period -> price_data
        """
        from datetime import datetime
        
        result = {}
        data = full_data.get("data", [])
        
        if not data:
            return {p: {"data": [], "ticker": full_data.get("ticker", "")} for p in periods}
        
        # Define period durations
        period_days = {
            "10y": 3650,
            "5y": 1825,
            "1y": 365,
            "6mo": 180,
            "3mo": 90,
            "1mo": 30,
            "1wk": 7,
            "1d": 1,
            "24h": 1
        }
        
        now = datetime.now()
        
        for period in periods:
            days = period_days.get(period, 365)
            cutoff = now - timedelta(days=days)
            
            filtered = [
                d for d in data 
                if datetime.fromisoformat(d["date"].replace("Z", "")) >= cutoff
            ]
            
            result[period] = {
                "ticker": full_data.get("ticker", ""),
                "period": period,
                "data": filtered,
                "last_price": filtered[-1]["close"] if filtered else 0,
                "source": full_data.get("source", "sliced")
            }
        
        return result

    async def identify_pivotal_events(self, ticker: str, company_name: str) -> List[Dict]:
        """
        Use AI to identify pivotal events from news/price data context.
        This is a placeholder for the advanced 'History + News' analysis.
        """
        # logic to correlate price jumps with news
        # For now, return empty list or mock events
        return []
