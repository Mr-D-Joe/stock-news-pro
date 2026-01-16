from ai_service.models.impact import StockSensitivity, FundamentalData
from ai_service.models.article import ArticleCollection
from typing import Optional

def build_essay_prompt(
    articles: ArticleCollection,
    focus_stocks: list[str],
    focus_sectors: list[str],
    language: str = "English",
    sensitivity_profile: Optional[StockSensitivity] = None,
    fundamentals: Optional[FundamentalData] = None,
) -> str:
    """
    Build a prompt for generating an analytical essay following the DeltaValue methodology.
    
    DeltaValue Methodology (Expert Analysis):
    - Fundamental evaluation (P/E, PEG, ROE, etc.)
    - Qualitative assessment (Moat, Management, Business Model)
    - Expert perspectives (Buffett, Lynch)
    - Margin of Safety & Target Price Range
    """
    # Build article context with citation references
    article_context_parts = []
    for article in articles.articles:
        ref = f"[{article.citation_id}]"
        date_str = article.published.strftime("%Y-%m-%d") if article.published else "n.d."
        
        article_text = article.content[:3000] if article.content else article.title
        
        article_context_parts.append(
            f"{ref} Source: {article.source}\n"
            f"Title: {article.title}\n"
            f"Date: {date_str}\n"
            f"Content: {article_text}\n"
        )
    
    articles_context = "\n---\n".join(article_context_parts)
    
    stocks_str = ", ".join(focus_stocks) if focus_stocks else "various stocks"
    sectors_str = ", ".join(focus_sectors) if focus_sectors else "the market"
    
    prompt = f"""You are a senior financial analyst at DeltaValue. Your task is to write a comprehensive investment research report for {stocks_str} based on {articles.count} recent articles and the provided fundamental data.

## DeltaValue Methodology
Your analysis must strictly follow the DeltaValue systematic approach:
1. **Top-Down & Bottom-Up**: Connect macroeconomic sector trends (Top-Down) with specific company performance (Bottom-Up).
2. **Qualitative Moat Analysis**: Evaluate "Burggraben" (Economic Moats). Does the company have pricing power, high switching costs, or unique brand value?
3. **Expert Synthesis**: Provide perspectives from:
   - **Warren Buffett**: Focus on business quality, ROIC/ROE, durable competitive advantages, and long-term value.
   - **Peter Lynch**: Focus on "Growth at a Reasonable Price" (GARP), utilizing the PEG Ratio.
4. **Margin of Safety**: Weigh recent news against intrinsic value. Is bad news a value opportunity or a long-term risk?
"""
    
    if sensitivity_profile:
        prompt += f"""
## Market Volatility Context
- **Stock**: {sensitivity_profile.symbol}
- **Volatility (Avg. Daily Move)**: {sensitivity_profile.avg_daily_move_pct}%
- **Sensitivity Score**: {sensitivity_profile.sensitivity_score}
- **Instruction**: Interpret large price moves in context—is it a genuine trend change or typical volatility for this specific ticker?
"""

    if fundamentals:
        prompt += f"""
## Company Fundamentals (DeltaValue Matrix)
- **Valuation**: P/E: {fundamentals.trailing_pe}, Forward P/E: {fundamentals.forward_pe}, PEG Ratio: {fundamentals.peg_ratio}, P/S: {fundamentals.price_to_sales}, P/B: {fundamentals.price_to_book}
- **Quality**: ROE: {fundamentals.return_on_equity}, ROA: {fundamentals.return_on_assets}, Profit Margin: {fundamentals.profit_margins}, Operating Margin: {fundamentals.operating_margins}
- **Financial Health**: Debt/Equity: {fundamentals.debt_to_equity}, Current Ratio: {fundamentals.current_ratio}, Free Cashflow: {fundamentals.free_cashflow}
- **Market Growth**: Rev Growth (YoY): {fundamentals.revenue_growth}, Earnings Growth (YoY): {fundamentals.earnings_growth}
- **Analyst Targets**: Mean: {fundamentals.target_mean}, High: {fundamentals.target_high}, Low: {fundamentals.target_low} ({fundamentals.number_of_analysts} analysts)

### Analysis Rules:
- **Lynch Check**: Compute if PEG < 1.0 (Growth opportunity).
- **Buffett Check**: Verify if Margin > 20% and ROE > 15% (Quality/Moat indicators).
- **Graham Check (Safety)**: Compare current price to Intrinsic Value estimates.
"""

    prompt += f"""
## Report Structure (Output in {language})

### 1. Executive Summary (Expert Take)
A 2-3 sentence high-level assessment of the current situation. Is the stock a "Buy", "Hold" or "Watch" based on the news influx?

### 2. Fundamental & News Integration (DeltaValue Matrix)
Synthesize the articles with the fundamentals. 
- How does source [1]'s news impact the ROE/ROA or PEG story?
- Identify if the news supports a "Burggraben" (Moat) or threatens it.

### 3. Expert Perspectives (Buffett vs. Lynch View)
Write dedicated sub-sections for:
- **The Buffett View**: Focus on long-term compound growth and moats.
- **The Lynch View**: Focus on catalysts, growth rates, and GARP.

### 4. SWOT Analysis
- **Strengths**: Intrinsic advantages (e.g., ROIC, Brand).
- **Weaknesses**: Fundamental gaps or negative news.
- **Opportunities**: Growth catalysts from the news.
- **Threats**: Competition, Macro shifts, or Regulatory risks.

### 5. DeltaValue Investment Thesis & Price Roadmap
- **Margin of Safety Assessment**: Is the stock currently "Fair Value", "Undervalued", or "Overvalued"?
- **12mo Price Range Estimate**: Define a potential target range based on the Analyst Targets and Valuation metrics.

### 6. Critical Watch Items & Upcoming Dates
Dates or specific metrics to monitor (e.g., Earnings on [Source X]).

## Formatting & Citation Rules:
- Use `[UP:text]` for positive outlooks (rendered in GREEN).
- Use `[DOWN:text]` for negative risks (rendered in RED).
- **EVERY factual claim must have a citation [1].**
- Language: **{language}**.

## Source Material
{articles_context}

---

Begin the DeltaValue Expert Analysis:"""

    return prompt


def build_anomaly_detection_prompt(articles: ArticleCollection) -> str:
    """Build prompt for detecting news anomalies and patterns."""
    
    # Group articles by date
    date_counts: dict[str, int] = {}
    for article in articles.articles:
        if article.published:
            date_key = article.published.strftime("%Y-%m-%d")
            date_counts[date_key] = date_counts.get(date_key, 0) + 1
    
    date_distribution = "\n".join(f"- {date}: {count} articles" for date, count in sorted(date_counts.items()))
    
    # Get article titles for pattern analysis
    titles = [f"[{a.citation_id}] {a.title}" for a in articles.articles[:50]]
    titles_text = "\n".join(titles)
    
    prompt = f"""Analyze the following news collection for anomalies and patterns:

## News Publication Distribution
{date_distribution}

## Article Titles
{titles_text}

## Analysis Tasks
1. **Frequency Analysis**: Are there unusual spikes in news volume on specific dates?
2. **Theme Clustering**: What are the main themes/topics across these articles?
3. **Sentiment Indicators**: Based on titles, what's the overall sentiment trend?
4. **Rumor Detection**: Are there any speculative or unconfirmed reports?
5. **Source Diversity**: How diverse are the information sources?

Provide your analysis in a structured format with clear sections."""

    return prompt


def build_impact_relevance_prompt(
    articles: list[dict], 
    stock_symbol: str, 
    language: str = "German"
) -> str:
    """
    Build a prompt for evaluating news relevance and generating explanations.
    
    Args:
        articles: List of dicts with 'title' and 'summary'
        stock_symbol: Target stock ticker
        language: Output language for explanations
    """
    articles_text = ""
    for i, a in enumerate(articles):
        articles_text += f"ID: {i}\nTitle: {a['title']}\nContent: {a['summary']}\n---\n"
        
    return f"""Analyze the following news articles and evaluate their specific relevance to the stock symbol '{stock_symbol}'.

For each article, determine:
1. **Relevance Score**: A value from 0.0 to 1.0 (1.0 = highly specific to {stock_symbol}, 0.0 = completely unrelated).
2. **Relevance Explanation**: A very concise sentence (max 150 characters) explaining WHY this is relevant to {stock_symbol}.
   - E.g., "Positive earnings report exceeds analyst expectations for {stock_symbol}."
   - E.g., "Reported layoffs in the same sector could indicate broader industry headwinds for {stock_symbol}."

The explanation MUST be written in {language}.

Return your analysis as a JSON array of objects, one for each article ID:
[
  {{"id": 0, "relevance_score": 0.95, "explanation": "..."}},
  ...
]

Articles:
{articles_text}

JSON Response:"""


def build_summary_prompt(text: str, max_words: int = 100) -> str:
    """Build prompt for summarizing a single article."""
    return f"""Summarize the following article in approximately {max_words} words. 
Focus on the key facts, figures, and implications.

Article:
{text}

Summary:"""


SYSTEM_INSTRUCTION_ANALYST = """You are an expert financial analyst specializing in market intelligence and stock analysis. 
Your analysis is:
- Factual and evidence-based
- Clear and professional
- Properly cited with references
- Balanced in perspective
- Focused on actionable insights

You never fabricate information and always distinguish between confirmed facts and speculation."""
