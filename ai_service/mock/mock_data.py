"""Mock data for development mode - 4 fictional stocks with complete data."""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import random

# =============================================================================
# MOCK STOCKS DATA (4 stocks across different sectors)
# =============================================================================

MOCK_STOCKS: Dict[str, Dict[str, str]] = {
    "ACME": {
        "symbol": "ACME",
        "name": "ACME Corporation",
        "sector": "Technology",
        "industry": "Software - Infrastructure",
        "business_summary": "ACME Corporation is a leading provider of AI-powered manufacturing solutions. The company's innovative platform combines machine learning with industrial automation to optimize production processes, reduce waste, and improve quality control. Founded in 2015, ACME has grown to serve over 500 enterprise clients globally.",
    },
    "BGNX": {
        "symbol": "BGNX",
        "name": "BioGenX Inc.",
        "sector": "Healthcare",
        "industry": "Biotechnology",
        "business_summary": "BioGenX Inc. is a clinical-stage biotechnology company focused on developing next-generation gene therapies for oncology and rare diseases. The company's proprietary CRISPR-based delivery platform enables precise genetic modifications with minimal off-target effects. BioGenX has three candidates in Phase II trials.",
    },
    "NOVA": {
        "symbol": "NOVA",
        "name": "NovaCraft Energy",
        "sector": "Energy",
        "industry": "Renewable Energy",
        "business_summary": "NovaCraft Energy is a vertically integrated renewable energy company specializing in next-generation solar panel manufacturing and utility-scale battery storage solutions. The company operates 12 solar farms across the Southwest US and Europe, with a total capacity of 2.4 GW. NovaCraft's proprietary perovskite solar cells achieve 28% efficiency, leading the industry.",
    },
    "FINX": {
        "symbol": "FINX",
        "name": "FinanceX Holdings",
        "sector": "Financials",
        "industry": "Fintech",
        "business_summary": "FinanceX Holdings operates a leading digital banking platform serving 15 million customers across North America and Europe. The company offers AI-powered lending, wealth management, and payment solutions. Founded in 2018, FinanceX has achieved profitability with $2.1B in annual revenue and continues to expand its product ecosystem.",
    }
}

# =============================================================================
# MOCK FUNDAMENTALS
# =============================================================================

MOCK_FUNDAMENTALS: Dict[str, Dict[str, Any]] = {
    "ACME": {
        "pe_ratio": 24.5,
        "peg_ratio": 1.8,
        "roe": 18.5,
        "debt_to_equity": 0.45,
        "target_mean_price": 165.00,
        "target_high_price": 190.00,
        "target_low_price": 130.00,
        "recommendation": "buy",
        "executive_summary": "ACME ist ein Strong Buy basierend auf Marktführerschaft, soliden Finanzkennzahlen und klaren Wachstumskatalysatoren.",
        "business_summary": MOCK_STOCKS["ACME"]["business_summary"],
        "sector": "Technology",
        "industry": "Software - Infrastructure",
        "market_cap": 12500000000,
        "beta": 1.15,
        "dividend_yield": 0.0,
        "revenue_growth": 0.28,
        "profit_margin": 0.22,
    },
    "BGNX": {
        "pe_ratio": None,  # Pre-profit biotech
        "peg_ratio": None,
        "roe": -15.2,  # Negative - R&D heavy
        "debt_to_equity": 0.82,
        "target_mean_price": 95.00,
        "target_high_price": 120.00,
        "target_low_price": 55.00,
        "recommendation": "hold",
        "executive_summary": "BioGenX ist ein spekulativer Hold. Die Pipeline zeigt Potenzial, aber hohe Risiken durch fehlende Profitabilität.",
        "business_summary": MOCK_STOCKS["BGNX"]["business_summary"],
        "sector": "Healthcare",
        "industry": "Biotechnology",
        "market_cap": 3200000000,
        "beta": 1.85,
        "dividend_yield": 0.0,
        "revenue_growth": None,
        "profit_margin": None,
    },
    "NOVA": {
        "pe_ratio": 32.1,
        "peg_ratio": 1.4,
        "roe": 12.8,
        "debt_to_equity": 0.95,
        "target_mean_price": 88.00,
        "target_high_price": 110.00,
        "target_low_price": 65.00,
        "recommendation": "buy",
        "executive_summary": "NovaCraft Energy ist ein Buy dank führender Solartechnologie und starkem Wachstum im Bereich erneuerbare Energien.",
        "business_summary": MOCK_STOCKS["NOVA"]["business_summary"],
        "sector": "Energy",
        "industry": "Renewable Energy",
        "market_cap": 8700000000,
        "beta": 1.35,
        "dividend_yield": 0.012,
        "revenue_growth": 0.45,
        "profit_margin": 0.15,
    },
    "FINX": {
        "pe_ratio": 18.2,
        "peg_ratio": 0.9,
        "roe": 22.5,
        "debt_to_equity": 0.65,
        "target_mean_price": 72.00,
        "target_high_price": 85.00,
        "target_low_price": 58.00,
        "recommendation": "strong_buy",
        "executive_summary": "FinanceX ist ein Strong Buy mit hervorragender Bewertung (PEG 0.9), solidem ROE und starkem Kundenwachstum.",
        "business_summary": MOCK_STOCKS["FINX"]["business_summary"],
        "sector": "Financials",
        "industry": "Fintech",
        "market_cap": 15200000000,
        "beta": 1.25,
        "dividend_yield": 0.008,
        "revenue_growth": 0.35,
        "profit_margin": 0.28,
    }
}

# =============================================================================
# MOCK NEWS
# =============================================================================

def get_mock_news(ticker: str) -> List[Dict[str, Any]]:
    """Return mock news articles for a ticker."""
    base_date = datetime.now()
    
    news_data = {
        "ACME": [
            {"title": "ACME Corp Announces Record Q4 Revenue", "source": "Reuters", "published": base_date - timedelta(days=1), "summary": "ACME Corporation reported Q4 revenue of $2.3 billion, beating analyst estimates by 12%. The company's AI platform showed strong adoption in the automotive sector."},
            {"title": "ACME Expands AI Platform to European Markets", "source": "TechCrunch", "published": base_date - timedelta(days=2), "summary": "The company opened new data centers in Frankfurt and London to serve growing European demand. CEO expects 40% international revenue by 2027."},
            {"title": "Analysts Upgrade ACME to Strong Buy", "source": "Seeking Alpha", "published": base_date - timedelta(days=3), "summary": "Morgan Stanley upgraded ACME citing strong competitive moat and expanding margins. Price target raised to $180."},
            {"title": "ACME Partners with Major Automaker for Smart Factory", "source": "Bloomberg", "published": base_date - timedelta(days=5), "summary": "Multi-year deal valued at $500M to transform manufacturing operations using ACME's AI platform."},
            {"title": "CEO Interview: ACME's Vision for 2026", "source": "CNBC", "published": base_date - timedelta(days=7), "summary": "CEO Jane Smith discusses expansion plans and new product roadmap including edge AI solutions."},
            {"title": "ACME Stock Hits All-Time High", "source": "MarketWatch", "published": base_date - timedelta(days=8), "summary": "Shares rose 8% following positive earnings guidance and analyst upgrades."},
            {"title": "ACME Acquires Robotics Startup for $120M", "source": "VentureBeat", "published": base_date - timedelta(days=10), "summary": "Acquisition strengthens ACME's autonomous systems capabilities and adds 50 AI engineers."},
            {"title": "Industry Report: AI Manufacturing Market Growing 25% YoY", "source": "Gartner", "published": base_date - timedelta(days=12), "summary": "ACME identified as market leader with 35% share in latest analyst report."},
            {"title": "ACME Opens New R&D Center in Austin", "source": "Austin Chronicle", "published": base_date - timedelta(days=14), "summary": "New facility to create 500 engineering jobs and focus on next-gen AI research."},
            {"title": "Patent Filing Reveals ACME's Next-Gen AI Chip", "source": "The Verge", "published": base_date - timedelta(days=15), "summary": "Company developing custom silicon for edge computing to reduce latency by 80%."},
        ],
        "BGNX": [
            {"title": "BioGenX Phase II Trial Shows Promising Results", "source": "BioPharma Dive", "published": base_date - timedelta(days=1), "summary": "Lead cancer therapy candidate achieved 68% response rate in mid-stage trial, exceeding expectations."},
            {"title": "FDA Grants Fast Track Designation to BGNX-101", "source": "Reuters", "published": base_date - timedelta(days=3), "summary": "Expedited review pathway for rare disease gene therapy could accelerate approval by 18 months."},
            {"title": "BioGenX Raises $200M in Follow-On Offering", "source": "Fierce Biotech", "published": base_date - timedelta(days=5), "summary": "Funds to support Phase III trials and manufacturing scale-up. Minimal dilution at 5%."},
            {"title": "Analyst: BGNX Could Be Acquisition Target", "source": "Seeking Alpha", "published": base_date - timedelta(days=7), "summary": "Large pharma companies reportedly interested in CRISPR technology. Potential premium of 50-80%."},
            {"title": "BioGenX Presents at J.P. Morgan Healthcare Conference", "source": "CNBC", "published": base_date - timedelta(days=10), "summary": "CEO outlined 2026 clinical milestones and partnership strategy."},
            {"title": "Competition Heats Up in Gene Therapy Space", "source": "STAT News", "published": base_date - timedelta(days=12), "summary": "Industry analysis shows crowded pipeline but strong differentiation for BGNX platform."},
            {"title": "BioGenX Expands Manufacturing Partnership", "source": "Contract Pharma", "published": base_date - timedelta(days=14), "summary": "Deal with Lonza to produce commercial-scale gene therapies."},
            {"title": "Insider Buying: BGNX CEO Purchases $500K in Stock", "source": "MarketWatch", "published": base_date - timedelta(days=16), "summary": "Executive confidence signal ahead of Phase III data readout."},
            {"title": "Patent Victory Strengthens BGNX IP Portfolio", "source": "Law360", "published": base_date - timedelta(days=18), "summary": "Key CRISPR patents upheld in European court, blocking competitor challenges."},
            {"title": "BioGenX Hires Former FDA Official as CMO", "source": "Endpoints News", "published": base_date - timedelta(days=20), "summary": "New leadership expected to accelerate regulatory strategy."},
        ],
        "NOVA": [
            {"title": "NovaCraft Energy Breaks Efficiency Record", "source": "CleanTechnica", "published": base_date - timedelta(days=1), "summary": "New perovskite solar cells achieve 28.5% efficiency in lab tests, surpassing silicon limits."},
            {"title": "NOVA Secures $1.2B DOE Loan for Battery Gigafactory", "source": "Reuters", "published": base_date - timedelta(days=2), "summary": "Facility in Nevada will produce 100 GWh of battery storage annually by 2028."},
            {"title": "Major Utility Signs 15-Year PPA with NovaCraft", "source": "Utility Dive", "published": base_date - timedelta(days=4), "summary": "Southern California Edison commits to purchasing 500 MW of solar power at record-low rates."},
            {"title": "NOVA Stock Surges on IRA Tax Credit Extension", "source": "Bloomberg", "published": base_date - timedelta(days=6), "summary": "Inflation Reduction Act benefits extended through 2035, boosting renewable sector outlook."},
            {"title": "NovaCraft Expands into European Market", "source": "PV Magazine", "published": base_date - timedelta(days=8), "summary": "Acquisition of German solar developer adds 800 MW pipeline in EU."},
            {"title": "Analyst Report: NOVA Best Positioned for Energy Transition", "source": "Morgan Stanley", "published": base_date - timedelta(days=10), "summary": "Upgraded to Overweight with $110 price target citing technology leadership."},
            {"title": "NovaCraft Partners with Tesla on Grid Storage", "source": "Electrek", "published": base_date - timedelta(days=12), "summary": "Joint venture to deploy 2 GWh of battery storage in Texas."},
            {"title": "Q3 Results: NOVA Revenue Up 45% YoY", "source": "CNBC", "published": base_date - timedelta(days=14), "summary": "Strong demand for solar panels and storage solutions drives growth."},
            {"title": "NovaCraft CEO Named to White House Climate Council", "source": "The Hill", "published": base_date - timedelta(days=16), "summary": "Sarah Chen to advise on clean energy policy and grid modernization."},
            {"title": "NOVA Announces First Dividend", "source": "MarketWatch", "published": base_date - timedelta(days=18), "summary": "Quarterly dividend of $0.15 signals confidence in sustainable profitability."},
        ],
        "FINX": [
            {"title": "FinanceX Surpasses 15 Million Customers", "source": "TechCrunch", "published": base_date - timedelta(days=1), "summary": "Digital bank growth accelerates with 40% YoY customer acquisition. Average deposit up 25%."},
            {"title": "FINX Launches AI-Powered Wealth Management", "source": "Finextra", "published": base_date - timedelta(days=2), "summary": "New robo-advisor combines AI with human advisors for high-net-worth clients."},
            {"title": "FinanceX Partners with Visa for Instant Payments", "source": "PaymentsSource", "published": base_date - timedelta(days=4), "summary": "Real-time cross-border payments launch in 20 countries by Q2."},
            {"title": "Analysts Rate FINX Strong Buy After Earnings Beat", "source": "Seeking Alpha", "published": base_date - timedelta(days=6), "summary": "Q4 EPS of $1.25 beats estimates by $0.15. Full-year guidance raised."},
            {"title": "FinanceX Receives Full Banking License in UK", "source": "Financial Times", "published": base_date - timedelta(days=8), "summary": "Regulatory approval enables full-service banking in post-Brexit Britain."},
            {"title": "FINX Stock Up 12% on Acquisition Rumors", "source": "Bloomberg", "published": base_date - timedelta(days=10), "summary": "Reports suggest major bank exploring strategic acquisition at premium valuation."},
            {"title": "FinanceX Expands SMB Lending Platform", "source": "Forbes", "published": base_date - timedelta(days=12), "summary": "AI-powered underwriting reduces loan approval time to 24 hours for small businesses."},
            {"title": "Insider Confidence: FINX CFO Increases Stake", "source": "MarketWatch", "published": base_date - timedelta(days=14), "summary": "CFO purchases $750K in shares, citing strong conviction in growth trajectory."},
            {"title": "FinanceX Named Best Digital Bank 2025", "source": "Euromoney", "published": base_date - timedelta(days=16), "summary": "Industry recognition for customer experience and innovation."},
            {"title": "FINX Announces 2-for-1 Stock Split", "source": "CNBC", "published": base_date - timedelta(days=18), "summary": "Split to improve retail investor accessibility, effective next month."},
        ],
    }
    
    return news_data.get(ticker, [])

# =============================================================================
# MOCK DEEP WEB SOURCES
# =============================================================================

def get_mock_deep_web(ticker: str) -> List[Dict[str, Any]]:
    """Return mock deep web sources for a ticker."""
    deep_web_data = {
        "ACME": [
            {"title": "ACME Corp Deep Dive Analysis", "url": "https://seekingalpha.com/acme-analysis", "summary": "Comprehensive analysis of ACME's competitive position and growth strategy. The company's AI platform has shown consistent improvement in customer retention with 95% renewal rates. Management has a proven track record of execution.", "source": "DeepWeb", "published": datetime.now() - timedelta(days=3)},
            {"title": "Manufacturing AI Market Report 2026", "url": "https://gartner.com/manufacturing-ai", "summary": "Industry report positioning ACME as the clear market leader with 35% share. Competitors include Siemens, Rockwell, and smaller startups. ACME's moat comes from proprietary training data and customer integrations.", "source": "DeepWeb", "published": datetime.now() - timedelta(days=7)},
            {"title": "ACME Valuation Model by ValueInvestorsClub", "url": "https://valueinvestorsclub.com/acme", "summary": "DCF analysis suggests fair value of $175-185, representing 15-23% upside from current levels. Strong free cash flow generation of $450M annually supports premium valuation.", "source": "DeepWeb", "published": datetime.now() - timedelta(days=10)},
        ],
        "BGNX": [
            {"title": "BioGenX Pipeline Analysis", "url": "https://seekingalpha.com/bgnx-pipeline", "summary": "Detailed review of BGNX's three Phase II candidates. Lead asset BGNX-101 has blockbuster potential if trial succeeds. Peak sales estimate of $2-3B for lead indication alone.", "source": "DeepWeb", "published": datetime.now() - timedelta(days=4)},
            {"title": "Gene Therapy Market Forecast 2030", "url": "https://mckinsey.com/gene-therapy-2030", "summary": "Market expected to reach $35B by 2030 (25% CAGR). BGNX well-positioned in oncology segment but faces cash burn concerns. 24-month runway with current cash.", "source": "DeepWeb", "published": datetime.now() - timedelta(days=8)},
            {"title": "BGNX Risk Assessment by Biotech Investor", "url": "https://biotechinvestor.com/bgnx-risks", "summary": "Binary event risk from Phase III readout (Q3 2026). Historical success rate for similar trials is 45%. Partner deal could be catalyst, with Roche and Novartis rumored interested.", "source": "DeepWeb", "published": datetime.now() - timedelta(days=12)},
        ],
        "NOVA": [
            {"title": "NovaCraft Technology Deep Dive", "url": "https://cleantechnica.com/nova-tech", "summary": "Technical analysis of perovskite cell technology. NOVA's 28% efficiency represents significant breakthrough. Manufacturing cost 40% below silicon. Risk: Long-term durability still being proven.", "source": "DeepWeb", "published": datetime.now() - timedelta(days=2)},
            {"title": "Renewable Energy Policy Analysis 2026", "url": "https://bnef.com/renewable-policy", "summary": "IRA extension provides 10-year visibility for solar investments. NOVA's domestic manufacturing qualifies for maximum tax credits. Competitive advantage over Chinese imports.", "source": "DeepWeb", "published": datetime.now() - timedelta(days=6)},
            {"title": "NOVA vs Competitors: Battery Storage Comparison", "url": "https://woodmac.com/storage-comparison", "summary": "NOVA's battery storage costs $85/kWh vs industry average $110/kWh. Vertical integration provides margin advantage. Partnership with Tesla strengthens distribution.", "source": "DeepWeb", "published": datetime.now() - timedelta(days=11)},
        ],
        "FINX": [
            {"title": "FinanceX Business Model Analysis", "url": "https://ark-invest.com/finx-analysis", "summary": "FINX's unit economics show $150 customer acquisition cost with $450 lifetime value. 3x LTV/CAC ratio indicates sustainable growth. AI underwriting reduces default rates by 35% vs traditional banks.", "source": "DeepWeb", "published": datetime.now() - timedelta(days=3)},
            {"title": "Digital Banking Competitive Landscape", "url": "https://forrester.com/digital-banking", "summary": "FINX ranks #2 in customer satisfaction behind Chime. Strong position in millennial/Gen-Z demographic. International expansion adds TAM of $500B.", "source": "DeepWeb", "published": datetime.now() - timedelta(days=7)},
            {"title": "FINX Regulatory Risk Assessment", "url": "https://moodys.com/finx-regulatory", "summary": "Full banking license in US, UK, and EU provides regulatory moat. Capital ratios exceed requirements by 2x. No material regulatory concerns identified.", "source": "DeepWeb", "published": datetime.now() - timedelta(days=14)},
        ],
    }
    
    return deep_web_data.get(ticker, [])

# =============================================================================
# MOCK PRICE HISTORY
# =============================================================================

def get_mock_price_data(ticker: str, period: str = "1y") -> Dict[str, Any]:
    """Generate realistic mock price history.
    
    Supports periods: 24h, 1wk, 1mo, 3mo, 1y, 10y
    For 24h: Returns intraday data points (15-minute intervals)
    For others: Returns daily OHLCV data
    """
    base_prices = {"ACME": 142.50, "BGNX": 78.30, "NOVA": 75.40, "FINX": 62.80}
    volatility = {"ACME": 0.018, "BGNX": 0.035, "NOVA": 0.025, "FINX": 0.020}
    trend = {"ACME": 0.0008, "BGNX": 0.0002, "NOVA": 0.0010, "FINX": 0.0012}
    
    base_price = base_prices.get(ticker, 100.0)
    vol = volatility.get(ticker, 0.02)
    daily_trend = trend.get(ticker, 0.0005)
    
    random.seed(hash(ticker + period))  # Reproducible randomness per ticker+period
    
    prices = []
    
    # Special handling for 24h intraday data
    if period == "24h":
        # Simulate last trading day (yesterday or today if market open)
        now = datetime.now()
        # If weekend or before 9:30 AM, use previous trading day
        if now.weekday() >= 5:  # Saturday or Sunday
            days_back = now.weekday() - 4  # Go back to Friday
            trading_date = now - timedelta(days=days_back)
        elif now.hour < 9 or (now.hour == 9 and now.minute < 30):
            # Before market open, show yesterday (or Friday if Monday)
            if now.weekday() == 0:  # Monday
                trading_date = now - timedelta(days=3)
            else:
                trading_date = now - timedelta(days=1)
        else:
            trading_date = now
        
        # Generate 15-minute intervals from 9:30 AM to 4:00 PM (26 data points)
        market_open = trading_date.replace(hour=9, minute=30, second=0, microsecond=0)
        current_price = base_price * (1 + random.gauss(0, vol * 2))  # Slight daily variation
        
        for i in range(26):  # 6.5 hours in 15-min intervals
            time_point = market_open + timedelta(minutes=15 * i)
            change = random.gauss(0, vol * 0.3)  # Lower intraday volatility
            current_price *= (1 + change)
            current_price = max(current_price, base_price * 0.9)  # Tighter floor for intraday
            
            intraday_vol = abs(random.gauss(0, vol * 0.2))
            prices.append({
                "date": time_point.strftime("%Y-%m-%dT%H:%M:%S"),
                "time": time_point.strftime("%H:%M"),
                "open": round(current_price * (1 - intraday_vol/2), 2),
                "high": round(current_price * (1 + intraday_vol), 2),
                "low": round(current_price * (1 - intraday_vol), 2),
                "close": round(current_price, 2),
                "volume": random.randint(100000, 500000)
            })
        
        date_label = trading_date.strftime("%Y-%m-%d")
        is_historical = trading_date.date() < now.date()
        
        return {
            "prices": prices,
            "data": prices,
            "ticker": ticker,
            "period": period,
            "last_price": prices[-1]["close"] if prices else 0,
            "trading_date": date_label,
            "is_historical_day": is_historical,
            "source": "mock"
        }
    
    # Daily data for other periods
    days_map = {"1wk": 7, "1mo": 30, "3mo": 90, "1y": 365, "10y": 3650}
    num_days = days_map.get(period, 365)
    
    current_price = base_price * 0.75  # Start lower for upward trend
    
    for i in range(num_days):
        date = datetime.now() - timedelta(days=num_days - i)
        # Skip weekends for realism
        if date.weekday() >= 5:
            continue
        # Random walk with trend
        change = random.gauss(daily_trend, vol)
        current_price *= (1 + change)
        current_price = max(current_price, base_price * 0.3)  # Floor at 30% of base
        
        daily_vol = abs(random.gauss(0, vol * 0.8))
        prices.append({
            "date": date.strftime("%Y-%m-%d"),
            "open": round(current_price * (1 - daily_vol/2), 2),
            "high": round(current_price * (1 + daily_vol), 2),
            "low": round(current_price * (1 - daily_vol), 2),
            "close": round(current_price, 2),
            "volume": random.randint(1000000, 8000000)
        })
    
    return {
        "prices": prices,
        "data": prices,
        "ticker": ticker, 
        "period": period,
        "last_price": prices[-1]["close"] if prices else 0,
        "source": "mock"
    }


# =============================================================================
# MOCK SECTOR NEWS
# =============================================================================

def get_mock_sector_news(sector: str) -> List[Dict[str, Any]]:
    """Return mock sector-wide news (not stock-specific).
    
    Used for the sector news ticker in the GUI.
    """
    base_date = datetime.now()
    
    sector_news = {
        "Technology": [
            {"title": "Tech-Sektor reagiert auf neue KI-Regulierung der EU", "source": "Reuters", "published": base_date - timedelta(hours=2), "summary": "Neue Richtlinien für KI-Entwicklung beeinflussen Marktbewertungen."},
            {"title": "Halbleiter-Aktien steigen nach Chip-Nachfrage-Prognose", "source": "Bloomberg", "published": base_date - timedelta(hours=5), "summary": "Analysten erhöhen Kursziele für führende Chip-Hersteller."},
            {"title": "Cloud-Computing Wachstum übertrifft Erwartungen", "source": "CNBC", "published": base_date - timedelta(hours=8), "summary": "Branchenwachstum von 28% im Q4 signalisiert anhaltende Digitalisierung."},
            {"title": "Cybersecurity-Ausgaben erreichen Rekordniveau", "source": "TechCrunch", "published": base_date - timedelta(hours=12), "summary": "Unternehmen investieren verstärkt in IT-Sicherheit nach Hackerangriffen."},
            {"title": "Software-as-a-Service Konsolidierung erwartet", "source": "Handelsblatt", "published": base_date - timedelta(hours=18), "summary": "Analysten prognostizieren M&A-Welle im SaaS-Sektor."},
        ],
        "Healthcare": [
            {"title": "FDA beschleunigt Zulassungsverfahren für Gentherapien", "source": "BioPharma Dive", "published": base_date - timedelta(hours=1), "summary": "Neue Fast-Track-Richtlinien verkürzen Entwicklungszeiten."},
            {"title": "Biotech-Index steigt auf Jahreshoch", "source": "MarketWatch", "published": base_date - timedelta(hours=4), "summary": "Positive Studiendaten treiben Sektor-Rally."},
            {"title": "Krankenhaus-Aktien profitieren von Gesundheitsreform", "source": "Reuters", "published": base_date - timedelta(hours=7), "summary": "Erweiterte Versicherungsdeckung stärkt Umsatzprognosen."},
            {"title": "Pharma-Riesen erhöhen F&E-Investitionen", "source": "Fierce Pharma", "published": base_date - timedelta(hours=11), "summary": "Fokus auf seltene Krankheiten und personalisierte Medizin."},
            {"title": "Medizintechnik-Sektor vor Konsolidierungswelle", "source": "Handelsblatt", "published": base_date - timedelta(hours=16), "summary": "Große Player suchen Übernahmeziele im Mittelstand."},
        ],
        "Energy": [
            {"title": "Erneuerbare Energien überholen fossile Stromerzeugung", "source": "CleanTechnica", "published": base_date - timedelta(hours=1), "summary": "Wind und Solar decken erstmals über 50% des EU-Strombedarfs."},
            {"title": "Solar-Aktien profitieren von IRA-Verlängerung", "source": "Bloomberg", "published": base_date - timedelta(hours=3), "summary": "Steuervorteile bis 2035 stärken Investitionssicherheit."},
            {"title": "Batteriespeicher-Nachfrage verdreifacht sich", "source": "Reuters", "published": base_date - timedelta(hours=6), "summary": "Grid-Scale Speicher werden zum Milliardenmarkt."},
            {"title": "Ölpreis fällt auf 2-Jahres-Tief", "source": "CNBC", "published": base_date - timedelta(hours=10), "summary": "Nachfragerückgang in China belastet traditionelle Energiewerte."},
            {"title": "Wasserstoff-Aktien im Fokus nach EU-Förderprogramm", "source": "Handelsblatt", "published": base_date - timedelta(hours=14), "summary": "€50 Mrd. für grüne Wasserstoff-Infrastruktur angekündigt."},
        ],
        "Financials": [
            {"title": "Fintech-Sektor profitiert von Zinssenkungen", "source": "Financial Times", "published": base_date - timedelta(hours=2), "summary": "Niedrigere Refinanzierungskosten stärken Margen."},
            {"title": "Digitalbanken gewinnen Marktanteile von Großbanken", "source": "Forbes", "published": base_date - timedelta(hours=5), "summary": "30% der Neukunden wählen reine Online-Anbieter."},
            {"title": "Krypto-Regulierung schafft Rechtssicherheit", "source": "Bloomberg", "published": base_date - timedelta(hours=9), "summary": "Neue EU-Regeln ermöglichen institutionelle Investments."},
            {"title": "Versicherungsaktien steigen nach Prämienerhöhungen", "source": "Reuters", "published": base_date - timedelta(hours=13), "summary": "Klimarisiken führen zu höheren Versicherungskosten."},
            {"title": "Zahlungsdienstleister melden Rekord-Transaktionsvolumen", "source": "PaymentsSource", "published": base_date - timedelta(hours=17), "summary": "E-Commerce Boom treibt digitale Zahlungen."},
        ],
        "Biotechnology": [
            {"title": "CRISPR-Therapien nähern sich Marktreife", "source": "STAT News", "published": base_date - timedelta(hours=1), "summary": "Erste Gentherapien erhalten Zulassungsempfehlung."},
            {"title": "Onkologie-Pipeline zeigt vielversprechende Daten", "source": "Endpoints News", "published": base_date - timedelta(hours=4), "summary": "Phase-III-Erfolge in mehreren Krebsindikationen."},
            {"title": "Biotech-IPO-Aktivität nimmt wieder zu", "source": "BioCentury", "published": base_date - timedelta(hours=8), "summary": "Investoren kehren nach Flaute in den Sektor zurück."},
            {"title": "Partnerschaften zwischen Pharma und Biotech beschleunigen", "source": "Fierce Biotech", "published": base_date - timedelta(hours=12), "summary": "Deal-Volumen übertrifft Vorjahr um 40%."},
            {"title": "Seltene Krankheiten werden zum Wachstumsmarkt", "source": "Reuters", "published": base_date - timedelta(hours=16), "summary": "Orphan Drug Status bietet attraktive Entwicklungsanreize."},
        ],
    }
    
    # Default fallback for unknown sectors
    default_news = [
        {"title": f"{sector}-Sektor zeigt gemischte Entwicklung", "source": "Reuters", "published": base_date - timedelta(hours=2), "summary": "Analysten bleiben vorsichtig optimistisch für den Sektor."},
        {"title": f"Anleger bewerten {sector}-Aktien neu", "source": "Bloomberg", "published": base_date - timedelta(hours=6), "summary": "Marktbedingungen führen zu Neubewertungen im Sektor."},
        {"title": f"{sector}: Quartalszahlen im Fokus", "source": "CNBC", "published": base_date - timedelta(hours=12), "summary": "Earnings Season bringt wichtige Impulse für den Sektor."},
    ]
    
    return sector_news.get(sector, default_news)

# =============================================================================
# MOCK AI ANALYSIS RESPONSES
# =============================================================================

MOCK_ANALYSIS: Dict[str, Dict[str, Any]] = {
    "ACME": {
        "essay": """ACME Corporation präsentiert sich als überzeugende Investmentmöglichkeit im schnell wachsenden Markt für KI-gestützte Fertigungslösungen. Mit einem Marktanteil von 35% hat sich das Unternehmen als klarer Branchenführer etabliert und baut seinen Wettbewerbsvorsprung durch strategische Akquisitionen und signifikante F&E-Investitionen kontinuierlich aus.

Aus finanzieller Perspektive zeigt ACME solide Fundamentaldaten mit einem KGV von 24,5x und einer Eigenkapitalrendite von 18,5%, was auf eine effiziente Kapitalallokation hindeutet. Die Verschuldungsquote von 0,45 signalisiert eine konservative Bilanz mit ausreichend Spielraum für Wachstumsinvestitionen. Die jüngsten Quartalsergebnisse übertrafen die Analystenerwartungen um 12%.

Das Konsens-Kursziel von $165 deutet auf signifikantes Aufwärtspotenzial hin. Die Expansion in europäische Märkte, die Partnerschaft mit führenden Automobilherstellern und die Entwicklung eigener KI-Chips bieten klare Wachstumstreiber für die kommenden Jahre.""",
        "summary": "ACME ist ein Strong Buy basierend auf Marktführerschaft, soliden Finanzkennzahlen und klaren Wachstumskatalysatoren.",
        "swot": {
            "strengths": ["Marktführer mit 35% Marktanteil", "Starke F&E-Pipeline mit 500+ Patenten", "Solide Bilanz mit niedriger Verschuldung", "95% Kundenbindungsrate"],
            "weaknesses": ["Premium-Bewertung vs. Wettbewerb", "Kundenkonzentration bei Top-10 Kunden", "Abhängigkeit von Schlüsselpersonal"],
            "opportunities": ["Europäische Marktexpansion", "Partnerschaften mit Automobilherstellern", "Edge-KI und Custom-Chip-Entwicklung", "M&A für Technologie-Akquisition"],
            "threats": ["Neue Markteintritte von Tech-Giganten", "Konjunkturabschwächung im Fertigungssektor", "Lieferkettenrisiken", "Regulatorische Änderungen für KI"]
        },
        "buffett_view": "ACME verfügt über einen klaren Wettbewerbsgraben durch proprietäre Technologie und hohe Wechselkosten. Das Management hat disziplinierte Kapitalallokation und Fokus auf langfristigen Wert demonstriert.",
        "lynch_view": "Dies ist eine klassische Growth-at-Reasonable-Price Story. Das PEG von 1,8 ist attraktiv für einen Marktführer mit 28% Umsatzwachstum.",
        "outlook": "Bullischer 12-Monats-Ausblick mit Schlüsselkatalysatoren: Europäische Expansion, Automobilpartnerschaften und Custom-Chip-Tape-Out. Kursziel $175-180.",
        "key_findings": [
            "Q4-Umsatz übertraf Erwartungen um 12% mit $2,3 Mrd.",
            "Neue europäische Rechenzentren in Frankfurt und London operativ",
            "Morgan Stanley Upgrade auf Strong Buy mit Kursziel $180",
            "$500M Partnerschaft mit führendem Automobilhersteller unterzeichnet",
            "[Deep Web] DCF-Analyse zeigt fairen Wert von $175-185"
        ],
        "watch_items": ["Q1-Ergebnisse am 15. Februar", "Europäischer Umsatzanteil-Entwicklung", "Chip-Tape-Out Timing Q3"]
    },
    "BGNX": {
        "essay": """BioGenX Inc. bietet eine Chance mit höherem Risiko, aber auch höherem Renditepotenzial im Gentherapie-Bereich. Die CRISPR-basierte Plattform des Unternehmens hat vielversprechende klinische Ergebnisse gezeigt, jedoch müssen Investoren mit binären Ereignisrisiken durch bevorstehende Phase-III-Auswertungen umgehen können.

Das fehlende KGV reflektiert die prä-profitable Phase typischer Biotech-Unternehmen. Die erhöhte Verschuldungsquote von 0,82 erfordert Beobachtung, obwohl die kürzliche $200M-Kapitalerhöhung eine ausreichende Finanzierungsreichweite von 24 Monaten sichert. Die 68% Ansprechrate in Phase II übertraf die Erwartungen deutlich.

Die FDA Fast-Track-Designation für BGNX-101 ist ein positives Signal für beschleunigte Zulassung. Das Analysten-Kursziel von $95 deutet auf erhebliches Aufwärtspotenzial hin. Eine Positionsgröße sollte jedoch die inhärente Volatilität klinischer Biotechs berücksichtigen.""",
        "summary": "BGNX ist ein Hold für risikotolerante Investoren - hohes Aufwärtspotenzial, aber signifikantes binäres Risiko durch Phase-III-Daten.",
        "swot": {
            "strengths": ["Differenzierte CRISPR-Plattform mit 68% Ansprechrate", "FDA Fast-Track Status beschleunigt Zulassung", "Starkes IP-Portfolio mit Patentsieg in Europa"],
            "weaknesses": ["Hohe Cash-Burn-Rate von $40M/Quartal", "Keine zugelassenen Produkte am Markt", "Konzentrierte Pipeline auf drei Kandidaten"],
            "opportunities": ["$35 Mrd. Gentherapie-Markt bis 2030", "Partnerschaft oder Übernahme durch Big Pharma", "Label-Erweiterung bei Erfolg"],
            "threats": ["Binäres Trial-Versagensrisiko (45% historische Erfolgsrate)", "Wettbewerb von Vertex und CRISPR Therapeutics", "Preisdruck und Erstattungsunsicherheit"]
        },
        "buffett_view": "Biotech-Investments sind von Natur aus spekulativ. Die Wissenschaft ist vielversprechend, aber die binären Ergebnisse machen dies für konservative Portfolios ungeeignet.",
        "lynch_view": "Hochriskantes spekulatives Investment. Nur investieren, was man verlieren kann, aber die Auszahlung könnte 3-5x betragen bei Erfolg.",
        "outlook": "Gemischter Ausblick - signifikantes Aufwärtspotenzial bei Phase-III-Erfolg (Q3), aber 50%+ Abwärtsrisiko bei Versagen. Position entsprechend dimensionieren.",
        "key_findings": [
            "68% Ansprechrate in Phase II übertrifft 45% Benchmark",
            "FDA Fast-Track gewährt - beschleunigt Zulassung um 18 Monate",
            "$200M Kapitalerhöhung mit nur 5% Verwässerung",
            "CEO-Insiderkauf signalisiert Managementvertrauen",
            "[Deep Web] Roche und Novartis als potenzielle Partner im Gespräch"
        ],
        "watch_items": ["Phase-III-Daten Q3 2026", "Cash-Runway Monitoring (24 Monate)", "Partnerschaftsankündigungen"]
    },
    "NOVA": {
        "essay": """NovaCraft Energy positioniert sich als führender Profiteur der globalen Energiewende. Mit bahnbrechender Perowskit-Solarzellen-Technologie, die 28% Wirkungsgrad erreicht, und einer vertikal integrierten Wertschöpfungskette bietet das Unternehmen eine überzeugende Kombination aus Technologieführerschaft und Skalenvorteilen.

Die Finanzkennzahlen zeigen ein KGV von 32,1x bei 45% Umsatzwachstum, was ein attraktives PEG von 1,4 ergibt. Der $1,2 Mrd. DOE-Kredit für die Batterie-Gigafabrik in Nevada unterstreicht die strategische Bedeutung und reduziert das Finanzierungsrisiko erheblich. Die Verschuldung (D/E 0,95) liegt im Branchenrahmen.

Die Verlängerung der IRA-Steuergutschriften bis 2035 bietet langfristige Planungssicherheit. Die Partnerschaft mit Tesla für Netzspeicher und der 15-jährige PPA mit Southern California Edison sichern wiederkehrende Umsätze. Das Kursziel $110 bietet 30%+ Aufwärtspotenzial.""",
        "summary": "NOVA ist ein Buy - Technologieführer im Renewables-Sektor mit starker Policy-Rückenwind und exzellentem Management.",
        "swot": {
            "strengths": ["28% Effizienz bei Perowskit-Zellen (Branchenführend)", "40% niedrigere Produktionskosten als Silicon", "Vertikale Integration von Zelle bis Speicher", "$1,2 Mrd. DOE-Kredit sichert Finanzierung"],
            "weaknesses": ["Perowskit-Langzeithaltbarkeit noch in Prüfung", "Kapitalintensives Geschäftsmodell", "Abhängigkeit von Regierungssubventionen"],
            "opportunities": ["IRA-Verlängerung bis 2035 bietet 10-Jahr-Visibilität", "Europäische Expansion mit 800 MW Pipeline", "Batterie-Speicher als Wachstumstreiber"],
            "threats": ["Chinesische Konkurrenz bei Preisdruck", "Zinsänderungsrisiko bei Projektfinanzierung", "Technologiewechselrisiko", "Politische Policy-Änderungen"]
        },
        "buffett_view": "NOVA verfügt über einen Technologie-Moat und Kostenvorteile. Die langfristigen PPAs bieten stabile Cashflows. Subventionsabhängigkeit erfordert Monitoring.",
        "lynch_view": "Sektor mit strukturellem Rückenwind. Das PEG von 1,4 ist attraktiv für 45% Wachstum. Erste Dividende signalisiert Reife.",
        "outlook": "Bullischer 12-Monats-Ausblick. Schlüsselkatalysatoren: Gigafabrik-Grundsteinlegung, weitere PPA-Abschlüsse, und europäische Expansion. Kursziel $100-110.",
        "key_findings": [
            "Perowskit-Effizienz von 28,5% bricht Industrierekord",
            "$1,2 Mrd. DOE-Kredit für Nevada Batterie-Gigafabrik gesichert",
            "15-jähriger PPA mit SCE über 500 MW zu Rekord-niedrigen Raten",
            "Erste Dividende von $0,15/Quartal angekündigt",
            "[Deep Web] Produktionskosten $85/kWh vs. Branchenschnitt $110/kWh"
        ],
        "watch_items": ["Gigafabrik-Meilensteine und Zeitplan", "Europäische Pipeline-Entwicklung", "Perowskit-Langzeitstudien-Ergebnisse"]
    },
    "FINX": {
        "essay": """FinanceX Holdings etabliert sich als führende Neobank mit beeindruckenden Unit Economics und stetigem Kundenwachstum. Mit 15 Millionen Kunden und $2,1 Mrd. Jahresumsatz hat das Unternehmen die Skalierungsschwelle überschritten und nachhaltige Profitabilität erreicht.

Die Finanzkennzahlen sind exzellent: KGV 18,2x, ROE 22,5%, und PEG 0,9 bei 35% Wachstum - eine seltene Kombination aus Wert und Wachstum. Die KI-gestützte Kreditvergabe reduziert Ausfallraten um 35% gegenüber traditionellen Banken, was überlegene Risikomargen ermöglicht. Die vollständigen Banklizenzen in USA, UK und EU schaffen regulatorische Barriers-to-Entry.

Die Übernahmegerüchte und der angekündigte Aktiensplit unterstreichen die positive Marktstimmung. Das Konsens-Kursziel von $72 bietet 15% Aufwärtspotenzial, mit Übernahmeprämie möglicherweise deutlich höher.""",
        "summary": "FINX ist ein Strong Buy - führende Neobank mit exzellenten Unit Economics, profitablem Wachstum und M&A-Fantasie.",
        "swot": {
            "strengths": ["3x LTV/CAC Ratio (nachhaltige Unit Economics)", "22,5% ROE übertrifft traditionelle Banken deutlich", "KI-Underwriting reduziert Ausfälle um 35%", "Vollständige Banklizenzen in 3 Jurisdiktionen"],
            "weaknesses": ["Noch keine physischen Filialen", "Abhängigkeit von Tech-Infrastruktur", "Premium-Bewertung vs. traditionelle Banken"],
            "opportunities": ["$500 Mrd. internationaler TAM", "Wealth Management für High-Net-Worth", "SMB-Lending Platform Expansion", "Potenzielle Übernahme zu Premium"],
            "threats": ["Big-Tech-Konkurrenz (Apple, Google)", "Regulatorische Verschärfung im Fintech-Bereich", "Kreditzyklusrisiko bei Rezession", "Cybersecurity-Risiken"]
        },
        "buffett_view": "FINX zeigt nachhaltige Wettbewerbsvorteile durch Technologie und regulatorische Lizenzen. Die Profitabilität und Kapitalallokation sind vorbildlich für ein Wachstumsunternehmen.",
        "lynch_view": "Growth-at-Reasonable-Price par excellence. Das PEG von 0,9 bei einem Marktführer ist selten. CFO-Insiderkauf bestätigt Conviction.",
        "outlook": "Stark bullischer 12-Monats-Ausblick. Übernahmegerüchte bieten Upside-Potenzial. Organisch Kursziel $80-85, bei M&A möglicherweise $90+.",
        "key_findings": [
            "15 Millionen Kunden-Meilenstein erreicht (+40% YoY)",
            "Q4-EPS $1,25 übertrifft Schätzungen um $0,15",
            "UK-Vollbanklizenz ermöglicht europäische Skalierung",
            "2-für-1 Aktiensplit angekündigt",
            "[Deep Web] LTV/CAC von 3x validiert nachhaltige Unit Economics"
        ],
        "watch_items": ["Übernahme-Entwicklungen", "UK-Launch und Kundenwachstum", "Kreditqualität bei Makro-Abschwächung"]
    }
}

def get_mock_analysis(ticker: str) -> Dict[str, Any]:
    """Get mock analysis response for ticker."""
    return MOCK_ANALYSIS.get(ticker.upper(), MOCK_ANALYSIS["ACME"])

# =============================================================================
# MOCK EVENTS (NEWS + AI IDENTIFIED)
# =============================================================================

def get_mock_events(ticker: str) -> List[Dict[str, Any]]:
    """Get mock pivotal events for a ticker."""
    base_date = datetime.now()
    
    events_data = {
        "ACME": [
            {"title": "Record Q4 Earnings Release", "date": (base_date - timedelta(days=30)).strftime("%Y-%m-%d"), "category": "Earnings", "impact": "high", "summary": "Revenue beat by 12%"},
            {"title": "European Expansion Announcement", "date": (base_date - timedelta(days=60)).strftime("%Y-%m-%d"), "category": "Expansion", "impact": "medium", "summary": "New data centers in Frankfurt and London"},
            {"title": "Major Automaker Partnership", "date": (base_date - timedelta(days=90)).strftime("%Y-%m-%d"), "category": "Partnership", "impact": "high", "summary": "$500M multi-year deal"},
        ],
        "BGNX": [
            {"title": "FDA Fast Track Designation", "date": (base_date - timedelta(days=20)).strftime("%Y-%m-%d"), "category": "Regulatory", "impact": "high", "summary": "Expedited review for BGNX-101"},
            {"title": "Phase II Results Announced", "date": (base_date - timedelta(days=45)).strftime("%Y-%m-%d"), "category": "Clinical", "impact": "high", "summary": "68% response rate achieved"},
            {"title": "$200M Follow-On Offering", "date": (base_date - timedelta(days=75)).strftime("%Y-%m-%d"), "category": "Financing", "impact": "medium", "summary": "Runway extended to 24 months"},
        ],
        "NOVA": [
            {"title": "$1.2B DOE Loan Secured", "date": (base_date - timedelta(days=15)).strftime("%Y-%m-%d"), "category": "Financing", "impact": "high", "summary": "Gigafactory financing complete"},
            {"title": "Efficiency Record Broken", "date": (base_date - timedelta(days=40)).strftime("%Y-%m-%d"), "category": "Technology", "impact": "high", "summary": "28.5% perovskite efficiency"},
            {"title": "Tesla Partnership Announced", "date": (base_date - timedelta(days=70)).strftime("%Y-%m-%d"), "category": "Partnership", "impact": "medium", "summary": "2 GWh storage JV in Texas"},
        ],
        "FINX": [
            {"title": "15M Customer Milestone", "date": (base_date - timedelta(days=10)).strftime("%Y-%m-%d"), "category": "Growth", "impact": "medium", "summary": "40% YoY customer growth"},
            {"title": "UK Banking License Granted", "date": (base_date - timedelta(days=35)).strftime("%Y-%m-%d"), "category": "Regulatory", "impact": "high", "summary": "Full-service banking in UK"},
            {"title": "Stock Split Announced", "date": (base_date - timedelta(days=55)).strftime("%Y-%m-%d"), "category": "Corporate", "impact": "low", "summary": "2-for-1 split for accessibility"},
        ],
    }
    
    return events_data.get(ticker, [])
