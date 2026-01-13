from stock_news_ai.models.impact import StockSensitivity, FundamentalData
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
    Build a prompt for generating an analytical essay.
    
    The prompt instructs the AI to:
    - Analyze all provided articles
    - Generate a comprehensive essay with inline citations [1], [2], etc.
    - Identify key trends, anomalies, and patterns
    - Provide an executive summary
    """
    # Build article context with citation references
    article_context_parts = []
    for article in articles.articles:
        ref = f"[{article.citation_id}]"
        date_str = article.published.strftime("%Y-%m-%d") if article.published else "n.d."
        
        article_text = article.text[:2000] if article.text else article.title
        
        article_context_parts.append(
            f"{ref} Source: {article.source}\n"
            f"Title: {article.title}\n"
            f"Date: {date_str}\n"
            f"Content: {article_text}\n"
        )
    
    articles_context = "\n---\n".join(article_context_parts)
    
    stocks_str = ", ".join(focus_stocks) if focus_stocks else "various stocks"
    sectors_str = ", ".join(focus_sectors) if focus_sectors else "the market"
    
    prompt = f"""You are a financial analyst writing a comprehensive market intelligence report.
"""
    
    if sensitivity_profile:
        prompt += f"""
## Stock Historical Context
- **Stock**: {sensitivity_profile.symbol}
- **Volatility Level**: {sensitivity_profile.avg_daily_move_pct}% avg daily move
- **Sensitivity Score**: {sensitivity_profile.sensitivity_score} (relative to baseline)
- **Insight**: Use this to weigh news. A {sensitivity_profile.avg_daily_move_pct*2}% move for this stock might be more "normal" than for other companies.
"""

    if fundamentals:
        prompt += f"""
## Stock Fundamentals (Expert Analysis Context)
- **Valuation**: P/E: {fundamentals.trailing_pe}, Forward P/E: {fundamentals.forward_pe}, PEG Ratio: {fundamentals.peg_ratio}
- **Quality (Buffett/Lynch)**: ROE: {fundamentals.return_on_equity}, ROA: {fundamentals.return_on_assets}, Profit Margin: {fundamentals.profit_margins}
- **Financial Health**: Debt/Equity: {fundamentals.debt_to_equity}, Free Cashflow: {fundamentals.free_cashflow}
- **Analyst Targets**: Mean: {fundamentals.target_mean}, High: {fundamentals.target_high}, Low: {fundamentals.target_low} ({fundamentals.number_of_analysts} analysts)
- **Business**: Sector: {fundamentals.sector}, Industry: {fundamentals.industry}
- **Description**: {fundamentals.long_business_summary[:500] if fundamentals.long_business_summary else "N/A"}

### Expert Analysis Rules (DeltaValue Guidelines):
1. **Peter Lynch (GARP)**: Interpret news in context of the **PEG Ratio**. If PEG < 1, the stock might be underpriced growth.
2. **Warren Buffett (Moat)**: Look for "Economic Moats" in the news—competitive advantages, pricing power, or brand strength. Relate news to **ROE/ROA** and **High Margins**.
3. **Margin of Safety**: Assess if negative news is "priced in" or if it creates a value opportunity below intrinsic value.
4. **Top-Down/Bottom-Up**: Connect macroeconomic sector news (Top-Down) with these specific company fundamentals (Bottom-Up).
5. **Future Outlook (Price Range)**: Integrate a potential future stock price target range (e.g., for the next 12 months). Use the Analyst Targets and Valuation metrics to justify this.

## Formatting Rules
- Use `[UP:text]` for positive outlooks or gains (will be rendered in GREEN).
- Use `[DOWN:text]` for negative outlooks or risks (will be rendered in RED).
- Every claim must have a citation [1].
"""

    prompt += f"""
## Task
Analyze the following {articles.count} news articles about {stocks_str} in {sectors_str} and write a professional analytical essay.

## Requirements
1. **Executive Summary** (2-3 sentences): Key takeaways for busy readers
2. **Main Analysis** (3-5 paragraphs):
   - Synthesize information across all sources
   - Identify trends, patterns, and notable developments
   - Use inline citations [1], [2], etc. to reference specific articles
   - Highlight any anomalies or unusual news frequency
3. **Key Findings**: Bullet points of the most important insights
4. **SWOT Analysis**: A dedicated section for Strengths, Weaknesses, Opportunities, and Threats for the target stock(s)
5. **Critical Watch Items**: Specific events, metrics, or dates the reader should pay extremely close attention to in the near future
6. **Risk Assessment**: Potential risks or concerns identified
7. **Upcoming Calendar Events**: Identify specific dates and events (earnings call, product launches, shareholder meetings, court dates) that will take place in the future.
8. **Outlook**: Forward-looking assessment based on the news

## Citation Rules
- Every factual claim must have a citation reference like [1], [2]
- Use multiple citations [1][3] when information appears in multiple sources
- Do not fabricate information not present in the sources

## Language
Write the report in {language}.

## Articles to Analyze

{articles_context}

---

Now write the analytical essay:"""

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
