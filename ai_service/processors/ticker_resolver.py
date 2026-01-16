"""Ticker and Sector resolver using AI for fuzzy matching."""

import logging
import os
from typing import Optional, Dict, List
import json
import re
from pathlib import Path

from ai_service.analyzers.gemini_client import GeminiClient
from ai_service.config import Settings
from ai_service.analyzers.provider_factory import ProviderFactory

logger = logging.getLogger(__name__)

# Cache file path (stores dynamically resolved tickers)
CACHE_FILE = Path(__file__).parent.parent / "data" / "ticker_cache.json"

class TickerResolver:
    """Resolves fuzzy names or partial inputs to stock tickers and industries."""
    
    # Class-level dynamic cache (shared across instances, persists in memory)
    _DYNAMIC_CACHE: Dict[str, tuple] = {}
    _CACHE_LOADED = False
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self._client = None
        
        # Load cached tickers from file on first use
        if not TickerResolver._CACHE_LOADED:
            self._load_cache()
            TickerResolver._CACHE_LOADED = True
    
    def _load_cache(self):
        """Load cached tickers from JSON file."""
        try:
            if CACHE_FILE.exists():
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for key, value in data.items():
                        # Store as tuple (symbol, name, sector)
                        TickerResolver._DYNAMIC_CACHE[key.lower()] = (
                            value.get("symbol", ""),
                            value.get("name", ""),
                            value.get("sector", "")
                        )
                logger.info(f"Loaded {len(TickerResolver._DYNAMIC_CACHE)} cached tickers from file")
        except Exception as e:
            logger.warning(f"Failed to load ticker cache: {e}")
    
    def _save_to_cache(self, query: str, symbol: str, name: str, sector: str):
        """Add a resolved ticker to the dynamic cache and save to file."""
        if not symbol:  # Don't cache failed resolutions
            return
            
        clean_query = query.lower().strip()
        TickerResolver._DYNAMIC_CACHE[clean_query] = (symbol, name, sector)
        logger.info(f"Cached ticker: '{clean_query}' → {symbol} ({sector})")
        
        # Save to file for persistence
        try:
            CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
            # Convert cache to JSON-serializable format
            cache_data = {
                key: {"symbol": val[0], "name": val[1], "sector": val[2]}
                for key, val in TickerResolver._DYNAMIC_CACHE.items()
            }
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.warning(f"Failed to save ticker cache: {e}")

    @property
    def client(self):
        if self._client is None:
            # Use fallback client for automatic Gemini → OpenAI switching
            self._client = ProviderFactory.get_client("fallback", self.settings)
        return self._client

    # Common company name -> (ticker, name, sector) mappings
    COMMON_NAMES = {
        # Technology
        "apple": ("AAPL", "Apple Inc.", "Technology"),
        "google": ("GOOGL", "Alphabet Inc.", "Technology"),
        "microsoft": ("MSFT", "Microsoft Corporation", "Technology"),
        "amazon": ("AMZN", "Amazon.com Inc.", "E-Commerce"),
        "meta": ("META", "Meta Platforms Inc.", "Technology"),
        "facebook": ("META", "Meta Platforms Inc.", "Technology"),
        "nvidia": ("NVDA", "NVIDIA Corporation", "Semiconductors"),
        "netflix": ("NFLX", "Netflix Inc.", "Entertainment"),
        "intel": ("INTC", "Intel Corporation", "Semiconductors"),
        "amd": ("AMD", "Advanced Micro Devices Inc.", "Semiconductors"),
        "ibm": ("IBM", "International Business Machines", "Technology"),
        "oracle": ("ORCL", "Oracle Corporation", "Technology"),
        "salesforce": ("CRM", "Salesforce Inc.", "Technology"),
        "adobe": ("ADBE", "Adobe Inc.", "Technology"),
        "sap": ("SAP", "SAP SE", "Technology"),
        
        # Automotive
        "tesla": ("TSLA", "Tesla Inc.", "Automotive"),
        "mercedes": ("MBG.DE", "Mercedes-Benz Group AG", "Automotive"),
        "volkswagen": ("VOW3.DE", "Volkswagen AG", "Automotive"),
        "vw": ("VOW3.DE", "Volkswagen AG", "Automotive"),
        "bmw": ("BMW.DE", "Bayerische Motoren Werke AG", "Automotive"),
        "porsche": ("P911.DE", "Porsche AG", "Automotive"),
        
        # German Industrial / DAX
        "siemens": ("SIE.DE", "Siemens AG", "Industrial Conglomerate"),
        "basf": ("BAS.DE", "BASF SE", "Chemicals"),
        "bayer": ("BAYN.DE", "Bayer AG", "Healthcare"),
        "allianz": ("ALV.DE", "Allianz SE", "Insurance"),
        "deutsche bank": ("DBK.DE", "Deutsche Bank AG", "Financial Services"),
        "db": ("DBK.DE", "Deutsche Bank AG", "Financial Services"),
        "rheinmetall": ("RHM.DE", "Rheinmetall AG", "Defense"),
        "thyssenkrupp": ("TKA.DE", "ThyssenKrupp AG", "Industrial"),
        "henkel": ("HEN3.DE", "Henkel AG", "Consumer Goods"),
        "adidas": ("ADS.DE", "Adidas AG", "Consumer Goods"),
        "zalando": ("ZAL.DE", "Zalando SE", "E-Commerce"),
        "delivery hero": ("DHER.DE", "Delivery Hero SE", "E-Commerce"),
        "infineon": ("IFX.DE", "Infineon Technologies AG", "Semiconductors"),
        "deutsche telekom": ("DTE.DE", "Deutsche Telekom AG", "Telecommunications"),
        "telekom": ("DTE.DE", "Deutsche Telekom AG", "Telecommunications"),
        "eon": ("EOAN.DE", "E.ON SE", "Energy"),
        "rwe": ("RWE.DE", "RWE AG", "Energy"),
        
        # Healthcare / Pharma
        "eli lilly": ("LLY", "Eli Lilly and Company", "Healthcare"),
        "lilly": ("LLY", "Eli Lilly and Company", "Healthcare"),
        "johnson": ("JNJ", "Johnson & Johnson", "Healthcare"),
        "pfizer": ("PFE", "Pfizer Inc.", "Healthcare"),
        "moderna": ("MRNA", "Moderna Inc.", "Biotechnology"),
        "biontech": ("BNTX", "BioNTech SE", "Biotechnology"),
        "absci": ("ABSI", "Absci Corporation", "Biotechnology"),
        "novo nordisk": ("NVO", "Novo Nordisk A/S", "Healthcare"),
        "roche": ("ROG.SW", "Roche Holding AG", "Healthcare"),
        "novartis": ("NOVN.SW", "Novartis AG", "Healthcare"),
        
        # Consumer
        "disney": ("DIS", "The Walt Disney Company", "Entertainment"),
        "coca cola": ("KO", "The Coca-Cola Company", "Consumer Goods"),
        "coke": ("KO", "The Coca-Cola Company", "Consumer Goods"),
        "pepsi": ("PEP", "PepsiCo Inc.", "Consumer Goods"),
        "walmart": ("WMT", "Walmart Inc.", "Retail"),
        "costco": ("COST", "Costco Wholesale Corporation", "Retail"),
        
        # Financial
        "jpmorgan": ("JPM", "JPMorgan Chase & Co.", "Financial Services"),
        "goldman": ("GS", "Goldman Sachs Group Inc.", "Financial Services"),
        "berkshire": ("BRK-B", "Berkshire Hathaway Inc.", "Financial Services"),
        "visa": ("V", "Visa Inc.", "Financial Services"),
        "mastercard": ("MA", "Mastercard Inc.", "Financial Services"),
        "paypal": ("PYPL", "PayPal Holdings Inc.", "Financial Services"),
    }

    def _fuzzy_match(self, query: str, threshold: float = 0.8) -> Optional[str]:
        """Find the best fuzzy match for a query in COMMON_NAMES."""
        query_lower = query.lower().strip()
        best_match = None
        best_score = 0.0
        
        for name in self.COMMON_NAMES.keys():
            # Calculate similarity using simple character comparison
            score = self._similarity(query_lower, name)
            if score > best_score and score >= threshold:
                best_score = score
                best_match = name
        
        if best_match:
            logger.info(f"Fuzzy matched '{query}' to '{best_match}' (score: {best_score:.2f})")
        return best_match
    
    def _similarity(self, s1: str, s2: str) -> float:
        """Calculate similarity between two strings (Levenshtein-based ratio)."""
        if not s1 or not s2:
            return 0.0
        if s1 == s2:
            return 1.0
        
        # Simple Levenshtein distance calculation
        len1, len2 = len(s1), len(s2)
        if len1 < len2:
            s1, s2 = s2, s1
            len1, len2 = len2, len1
        
        # Use the shorter string iterations
        current_row = list(range(len2 + 1))
        for i in range(1, len1 + 1):
            previous_row = current_row
            current_row = [i] + [0] * len2
            for j in range(1, len2 + 1):
                add = previous_row[j] + 1
                delete = current_row[j - 1] + 1
                change = previous_row[j - 1] + (0 if s1[i - 1] == s2[j - 1] else 1)
                current_row[j] = min(add, delete, change)
        
        distance = current_row[len2]
        max_len = max(len1, len2)
        return 1.0 - (distance / max_len)

    async def resolve_stock(self, query: str) -> Dict[str, str]:
        """
        Map a fuzzy string (e.g. 'Mercedes', 'Google', 'Lilly') to a ticker, name, and sector.
        Includes fuzzy matching for spelling errors and dynamic caching of AI results.
        
        Returns:
            Dict with 'symbol', 'name', 'sector', and 'is_resolved'
        """
        if not query or len(query) < 2:
            return {"symbol": "", "name": query, "sector": "", "is_resolved": False}

        clean_query = query.lower().strip()
        
        # 1. Check predefined common names first (exact match)
        if clean_query in self.COMMON_NAMES:
            mapping = self.COMMON_NAMES[clean_query]
            symbol, name = mapping[0], mapping[1]
            sector = mapping[2] if len(mapping) > 2 else ""
            logger.info(f"Resolved '{query}' via exact mapping: {symbol} ({sector})")
            return {"symbol": symbol, "name": name, "sector": sector, "is_resolved": True}

        # 2. Check dynamic cache (previously AI-resolved companies)
        if clean_query in TickerResolver._DYNAMIC_CACHE:
            cached = TickerResolver._DYNAMIC_CACHE[clean_query]
            logger.info(f"Resolved '{query}' from dynamic cache: {cached[0]} ({cached[2]})")
            return {"symbol": cached[0], "name": cached[1], "sector": cached[2], "is_resolved": True}

        # 3. Try fuzzy matching for spelling errors (searches both static and dynamic)
        fuzzy_match = self._fuzzy_match(query)
        if fuzzy_match:
            mapping = self.COMMON_NAMES[fuzzy_match]
            symbol, name = mapping[0], mapping[1]
            sector = mapping[2] if len(mapping) > 2 else ""
            logger.info(f"Resolved '{query}' via fuzzy match to '{fuzzy_match}': {symbol} ({sector})")
            return {"symbol": symbol, "name": name, "sector": sector, "is_resolved": True}

        # Check for direct Ticker match (Alpha-only, 1-5 chars, ALL CAPS in input)
        if re.match(r"^[A-Z]{1,5}$", query):  # Only if already uppercase
            return {"symbol": query, "name": query, "sector": "", "is_resolved": True}

        prompt = f"""You are a stock market expert. Identify the stock ticker symbol (Yahoo Finance format), official company name, and industry sector for: "{query}".

Return ONLY a valid JSON object with this exact format:
{{
    "symbol": "TICKER",
    "name": "Official Company Name",
    "sector": "Industry Sector (e.g. Technology, Healthcare, Automotive, Financial Services, Biotechnology, Consumer Goods, Energy, etc.)",
    "is_resolved": true
}}

If this is not a known public company or you're unsure, return:
{{
    "symbol": "",
    "name": "{query}",
    "sector": "",
    "is_resolved": false
}}

Important:
- Use Yahoo Finance ticker format (e.g., AAPL for Apple, MBG.DE for Mercedes-Benz Germany)
- For German stocks, append .DE or .F suffix
- Be specific with sector (not just "Other")
"""

        try:
            response = self.client.generate(prompt, temperature=0.0)
            # Find JSON in response
            match = re.search(r"\{.*\}", response.replace("\n", " "), re.DOTALL)
            if match:
                data = json.loads(match.group(0))
                # Ensure sector key exists
                if "sector" not in data:
                    data["sector"] = ""
                    
                # Cache the result for future lookups (only if successfully resolved)
                if data.get("is_resolved") and data.get("symbol"):
                    self._save_to_cache(
                        query=query,
                        symbol=data["symbol"],
                        name=data.get("name", query),
                        sector=data.get("sector", "")
                    )
                    
                logger.info(f"AI resolved '{query}' to {data.get('symbol')} ({data.get('sector')})")
                return data
        except Exception as e:
            logger.error(f"Ticker resolution failed for '{query}': {e}")
            
        return {"symbol": "", "name": query, "sector": "", "is_resolved": False}

    async def resolve_sector(self, query: str) -> str:
        """Map fuzzy sector (e.g. 'auto') to official industry term."""
        mapping = {
            "auto": "Automotive",
            "tech": "Technology",
            "it": "Technology",
            "health": "Healthcare",
            "med": "Healthcare",
            "pharma": "Healthcare",
            "finance": "Financial Services",
            "bank": "Financial Services",
            "energie": "Energy",
            "energy": "Energy",
            "bio": "Biotechnology",
            "biotech": "Biotechnology"
        }
        
        clean_query = query.lower().strip()
        if clean_query in mapping:
            return mapping[clean_query]
            
        # Fallback to AI if not in common mapping
        prompt = f"Map the term '{query}' to a standard financial sector/industry name. Return ONLY the category name (1-3 words)."
        try:
            response = self.client.generate(prompt, temperature=0.0)
            return response.strip()
        except:
            return query.capitalize()
