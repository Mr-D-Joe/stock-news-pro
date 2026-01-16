
import asyncio
import yfinance as yf
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def debug_absi_fetch():
    ticker = "ABSI"
    print(f"--- Debugging Data Fetch for {ticker} ---")
    
    # 1. Test standard yfinance fetch
    print("\n1. Testing yfinance.Ticker.info...")
    try:
        def fetch_info():
            stock = yf.Ticker(ticker)
            return stock.info
            
        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(None, fetch_info)
        
        if not info:
            print("❌ stock.info returned empty dict or None")
        else:
            print("✅ stock.info fetched successfully")
            print(f"   Sector: {info.get('sector')}")
            print(f"   P/E: {info.get('forwardPE')} / {info.get('trailingPE')}")
            print(f"   PEG: {info.get('pegRatio')}")
            print(f"   ROE: {info.get('returnOnEquity')}")
            print(f"   Target Mean: {info.get('targetMeanPrice')}")
            print(f"   Rec: {info.get('recommendationKey')}")
            
    except Exception as e:
        print(f"❌ Standard fetch failed: {e}")

    # 2. Test HistoricAnalyzer.get_fundamentals logic
    print("\n2. Testing HistoricAnalyzer logic...")
    try:
        from ai_service.analyzers.historic_analyzer import HistoricAnalyzer
        analyzer = HistoricAnalyzer()
        fundamentals = await analyzer.get_fundamentals(ticker)
        print(f"✅ Analyzer result: {fundamentals}")
    except Exception as e:
        print(f"❌ HistoricAnalyzer logic failed: {e}")

if __name__ == "__main__":
    asyncio.run(debug_absi_fetch())
