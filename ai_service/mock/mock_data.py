"""Mock data for development mode - 2 fictional stocks with complete data."""

from datetime import datetime, timedelta
import random

# =============================================================================
# MOCK STOCKS DATA
# =============================================================================

MOCK_STOCKS = {
    "ACME": {
        "symbol": "ACME",
        "name": "ACME Corporation",
        "sector": "Technology",
        "business_summary": "ACME Corporation is a leading provider of AI-powered manufacturing solutions. The company's innovative platform combines machine learning with industrial automation to optimize production processes, reduce waste, and improve quality control. Founded in 2015, ACME has grown to serve over 500 enterprise clients globally.",
    },
    "BGNX": {
        "symbol": "BGNX",
        "name": "BioGenX Inc.",
        "sector": "Biotechnology",
        "business_summary": "BioGenX Inc. is a clinical-stage biotechnology company focused on developing next-generation gene therapies for oncology and rare diseases. The company's proprietary CRISPR-based delivery platform enables precise genetic modifications with minimal off-target effects. BioGenX has three candidates in Phase II trials.",
    }
}

# =============================================================================
# MOCK FUNDAMENTALS
# =============================================================================

MOCK_FUNDAMENTALS = {
    "ACME": {
        "pe_ratio": 24.5,
        "peg_ratio": 1.8,
        "roe": 18.5,
        "debt_to_equity": 0.45,
        "target_mean_price": 165.00,
        "target_high_price": 190.00,
        "target_low_price": 130.00,
        "recommendation": "buy",
        "business_summary": MOCK_STOCKS["ACME"]["business_summary"],
        "sector": "Technology",
        "market_cap": 12500000000,
        "beta": 1.15,
    },
    "BGNX": {
        "pe_ratio": 45.2,
        "peg_ratio": 2.1,
        "roe": 8.2,
        "debt_to_equity": 0.82,
        "target_mean_price": 95.00,
        "target_high_price": 120.00,
        "target_low_price": 55.00,
        "recommendation": "hold",
        "business_summary": MOCK_STOCKS["BGNX"]["business_summary"],
        "sector": "Biotechnology",
        "market_cap": 3200000000,
        "beta": 1.85,
    }
}

# =============================================================================
# MOCK NEWS
# =============================================================================

def get_mock_news(ticker: str):
    """Return mock news articles for a ticker."""
    base_date = datetime.now()
    
    if ticker == "ACME":
        return [
            {"title": "ACME Corp Announces Record Q4 Revenue", "source": "Reuters", "published": base_date - timedelta(days=1), "summary": "ACME Corporation reported Q4 revenue of $2.3 billion, beating analyst estimates by 12%."},
            {"title": "ACME Expands AI Platform to European Markets", "source": "TechCrunch", "published": base_date - timedelta(days=2), "summary": "The company opened new data centers in Frankfurt and London to serve growing European demand."},
            {"title": "Analysts Upgrade ACME to Strong Buy", "source": "Seeking Alpha", "published": base_date - timedelta(days=3), "summary": "Morgan Stanley upgraded ACME citing strong competitive moat and expanding margins."},
            {"title": "ACME Partners with Major Automaker for Smart Factory", "source": "Bloomberg", "published": base_date - timedelta(days=5), "summary": "Multi-year deal valued at $500M to transform manufacturing operations."},
            {"title": "CEO Interview: ACME's Vision for 2025", "source": "CNBC", "published": base_date - timedelta(days=7), "summary": "CEO Jane Smith discusses expansion plans and new product roadmap."},
            {"title": "ACME Stock Hits All-Time High", "source": "MarketWatch", "published": base_date - timedelta(days=8), "summary": "Shares rose 8% following positive earnings guidance."},
            {"title": "ACME Acquires Robotics Startup for $120M", "source": "VentureBeat", "published": base_date - timedelta(days=10), "summary": "Acquisition strengthens ACME's autonomous systems capabilities."},
            {"title": "Industry Report: AI Manufacturing Market Growing 25% YoY", "source": "Gartner", "published": base_date - timedelta(days=12), "summary": "ACME identified as market leader in latest analyst report."},
            {"title": "ACME Opens New R&D Center in Austin", "source": "Austin Chronicle", "published": base_date - timedelta(days=14), "summary": "New facility to create 500 engineering jobs."},
            {"title": "Patent Filing Reveals ACME's Next-Gen AI Chip", "source": "The Verge", "published": base_date - timedelta(days=15), "summary": "Company developing custom silicon for edge computing."},
        ]
    elif ticker == "BGNX":
        return [
            {"title": "BioGenX Phase II Trial Shows Promising Results", "source": "BioPharma Dive", "published": base_date - timedelta(days=1), "summary": "Lead cancer therapy candidate achieved 68% response rate in mid-stage trial."},
            {"title": "FDA Grants Fast Track Designation to BGNX-101", "source": "Reuters", "published": base_date - timedelta(days=3), "summary": "Expedited review pathway for rare disease gene therapy."},
            {"title": "BioGenX Raises $200M in Follow-On Offering", "source": "Fierce Biotech", "published": base_date - timedelta(days=5), "summary": "Funds to support Phase III trials and manufacturing scale-up."},
            {"title": "Analyst: BGNX Could Be Acquisition Target", "source": "Seeking Alpha", "published": base_date - timedelta(days=7), "summary": "Large pharma companies reportedly interested in CRISPR technology."},
            {"title": "BioGenX Presents at J.P. Morgan Healthcare Conference", "source": "CNBC", "published": base_date - timedelta(days=10), "summary": "CEO outlined 2025 clinical milestones and partnership strategy."},
            {"title": "Competition Heats Up in Gene Therapy Space", "source": "STAT News", "published": base_date - timedelta(days=12), "summary": "Industry analysis shows crowded pipeline but strong differentiation for BGNX."},
            {"title": "BioGenX Expands Manufacturing Partnership", "source": "Contract Pharma", "published": base_date - timedelta(days=14), "summary": "Deal with Lonza to produce commercial-scale gene therapies."},
            {"title": "Insider Buying: BGNX CEO Purchases $500K in Stock", "source": "MarketWatch", "published": base_date - timedelta(days=16), "summary": "Executive confidence signal ahead of data readout."},
            {"title": "Patent Victory Strengthens BGNX IP Portfolio", "source": "Law360", "published": base_date - timedelta(days=18), "summary": "Key CRISPR patents upheld in European court."},
            {"title": "BioGenX Hires Former FDA Official as CMO", "source": "Endpoints News", "published": base_date - timedelta(days=20), "summary": "New leadership expected to accelerate regulatory strategy."},
        ]
    else:
        return []

# =============================================================================
# MOCK DEEP WEB
# =============================================================================

def get_mock_deep_web(ticker: str):
    """Return mock deep web sources for a ticker."""
    if ticker == "ACME":
        return [
            {"title": "ACME Corp Deep Dive Analysis", "url": "https://seekingalpha.com/acme-analysis", "summary": "Comprehensive analysis of ACME's competitive position and growth strategy. The company's AI platform has shown consistent improvement in customer retention.", "source": "DeepWeb"},
            {"title": "Manufacturing AI Market Report 2025", "url": "https://fool.com/manufacturing-ai", "summary": "Industry report positioning ACME as the clear market leader with 35% share. Competitors struggling to match technology stack.", "source": "DeepWeb"},
            {"title": "ACME Valuation Model", "url": "https://zacks.com/acme-valuation", "summary": "DCF analysis suggests fair value of $175, representing 23% upside from current levels. Strong free cash flow generation.", "source": "DeepWeb"},
        ]
    elif ticker == "BGNX":
        return [
            {"title": "BioGenX Pipeline Analysis", "url": "https://seekingalpha.com/bgnx-pipeline", "summary": "Detailed review of BGNX's three Phase II candidates. Lead asset BGNX-101 has blockbuster potential if trial succeeds.", "source": "DeepWeb"},
            {"title": "Gene Therapy Market Forecast", "url": "https://fool.com/gene-therapy-2025", "summary": "Market expected to reach $15B by 2028. BGNX well-positioned but faces cash burn concerns.", "source": "DeepWeb"},
            {"title": "BGNX Risk Assessment", "url": "https://zacks.com/bgnx-risks", "summary": "Binary event risk from Phase III readout. Dilution risk if additional capital needed. Partner deal could be catalyst.", "source": "DeepWeb"},
        ]
    else:
        return []

# =============================================================================
# MOCK PRICE HISTORY
# =============================================================================

def get_mock_price_data(ticker: str, period: str = "1y"):
    """Generate realistic mock price history."""
    days = {"1d": 1, "1wk": 7, "1mo": 30, "3mo": 90, "6mo": 180, "1y": 365, "10y": 365}
    num_days = days.get(period, 365)
    
    base_prices = {"ACME": 142.50, "BGNX": 78.30}
    base_price = base_prices.get(ticker, 100.0)
    
    prices = []
    current_price = base_price * 0.85  # Start 15% lower
    
    for i in range(num_days):
        date = datetime.now() - timedelta(days=num_days - i)
        # Random walk with slight upward bias
        change = random.gauss(0.001, 0.02)
        current_price *= (1 + change)
        
        prices.append({
            "date": date.strftime("%Y-%m-%d"),
            "open": round(current_price * 0.998, 2),
            "high": round(current_price * 1.015, 2),
            "low": round(current_price * 0.985, 2),
            "close": round(current_price, 2),
            "volume": random.randint(1000000, 5000000)
        })
    
    return {"prices": prices, "ticker": ticker, "period": period}

# =============================================================================
# MOCK AI RESPONSES
# =============================================================================

MOCK_ESSAYS = {
    "ACME": {
        "essay": """ACME Corporation represents a compelling investment opportunity in the rapidly growing AI-powered manufacturing space. The company has established itself as the market leader with a 35% market share and continues to expand its competitive moat through strategic acquisitions and R&D investments.

From a financial perspective, ACME demonstrates strong fundamentals with a P/E ratio of 24.5x and ROE of 18.5%, indicating efficient capital allocation. The debt-to-equity ratio of 0.45 suggests a conservative balance sheet with ample capacity for growth investments.

Looking ahead, the consensus analyst target of $165 represents meaningful upside from current levels. The company's expansion into European markets and partnerships with major automakers provide clear catalysts for continued growth.""",
        "summary": "ACME is a Strong Buy based on market leadership, solid financials, and clear growth catalysts.",
        "swot": {
            "strengths": ["Market leader with 35% share", "Strong R&D pipeline", "Robust balance sheet"],
            "weaknesses": ["Premium valuation", "Customer concentration risk", "Talent competition"],
            "opportunities": ["European expansion", "Automotive partnerships", "Edge AI"],
            "threats": ["New entrants", "Economic slowdown", "Supply chain disruption"]
        },
        "key_findings": [
            "Q4 revenue beat estimates by 12%",
            "New European data centers operational",
            "Morgan Stanley upgrade to Strong Buy",
            "$500M automaker partnership signed",
            "Custom AI chip in development"
        ],
        "watch_items": ["Q1 earnings on Feb 15", "European revenue ramp", "Chip tape-out timing"],
        "buffett_view": "ACME has a clear competitive moat and strong pricing power. The management team has demonstrated disciplined capital allocation.",
        "lynch_view": "This is a classic growth-at-reasonable-price story. The PEG of 1.8 is attractive for a market leader.",
        "outlook": "Bullish 12-month outlook with key catalysts including European expansion and automotive deals."
    },
    "BGNX": {
        "essay": """BioGenX Inc. presents a higher-risk, higher-reward opportunity in the gene therapy space. The company's CRISPR-based platform has shown promising clinical results, but investors must be comfortable with binary event risk from upcoming Phase III readouts.

The premium P/E of 45.2x reflects the speculative nature of biotech investing and potential blockbuster revenue if trials succeed. The elevated debt-to-equity of 0.82 requires monitoring, though the recent $200M raise provides adequate runway.

The FDA Fast Track designation for BGNX-101 is a positive signal, and the analyst target of $95 suggests significant upside potential. However, position sizing should reflect the inherent volatility of clinical-stage biotech.""",
        "summary": "BGNX is a Hold for risk-tolerant investors - high upside but significant binary risk.",
        "swot": {
            "strengths": ["Differentiated CRISPR platform", "FDA Fast Track status", "Strong IP portfolio"],
            "weaknesses": ["Cash burn rate", "No approved products", "Concentrated pipeline"],
            "opportunities": ["$15B gene therapy market", "Partnership/acquisition", "Label expansion"],
            "threats": ["Trial failure risk", "Competition from Vertex/CRISPR Tx", "Pricing pressure"]
        },
        "key_findings": [
            "68% response rate in Phase II",
            "FDA Fast Track granted",
            "$200M raised at minimal dilution",
            "CEO insider buying signals confidence",
            "Lonza manufacturing deal secured"
        ],
        "watch_items": ["Phase III data readout Q3", "Cash runway monitoring", "Partnership announcements"],
        "buffett_view": "Biotech investments are inherently speculative. The science is promising but the binary outcomes make this unsuitable for conservative portfolios.",
        "lynch_view": "High-risk speculative play. Only invest what you can afford to lose, but the payoff could be 3-5x.",
        "outlook": "Mixed outlook - significant upside if Phase III succeeds, but 50%+ downside risk on failure."
    }
}

def get_mock_analysis(ticker: str):
    """Get mock analysis response."""
    return MOCK_ESSAYS.get(ticker, MOCK_ESSAYS["ACME"])
