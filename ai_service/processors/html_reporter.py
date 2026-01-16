"""Premium HTML report generator for stock analysis.

Matches the DeltaValue Investment Research template exactly:
- Professional light theme (800px max-width)
- Executive Summary with sentiment badge
- Fundamental metrics grid (P/E, PEG, ROE, D/E)  
- Analyst targets with Business Context
- Dynamic price chart with all timeframes
- Essay content
- News Impact Analysis table with badges
- References section
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional


class HtmlReporter:
    """Generates premium HTML reports matching the original DeltaValue template."""

    def __init__(self, output_dir: str = "exports"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate(self, data: Dict[str, Any], language: str = "German") -> str:
        """Create standalone HTML report matching original template."""
        ticker = data.get("ticker", "UNKNOWN")
        company_name = data.get("company_name", ticker)
        analysis = data.get("analysis", {})
        price_timeframes = data.get("price_data", {})
        historic_events = data.get("historic_events", [])
        fundamentals = data.get("fundamentals", {})
        sector = data.get("sector", "")
        business_context = data.get("business_context", fundamentals.get("business_summary", ""))
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Report_{ticker}_{timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)

        chart_data_json = json.dumps(price_timeframes)
        events_json = json.dumps(historic_events)

        sentiment = analysis.get("sentiment", "neutral").lower()
        sentiment_class = "positive" if "positiv" in sentiment or "bullish" in sentiment else (
            "negative" if "negativ" in sentiment or "bearish" in sentiment else "neutral"
        )
        sentiment_label = "positive outlook" if sentiment_class == "positive" else (
            "negative outlook" if sentiment_class == "negative" else "neutral outlook"
        )

        # Build sections
        fundamentals_html = self._build_fundamentals_section(fundamentals, business_context)
        impact_table_html = self._build_impact_table(historic_events)
        references_html = self._build_references(data.get("references", []))

        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stock News Analysis: {company_name}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}

        .container {{
            background: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}

        .header {{
            border-bottom: 3px solid #2563eb;
            padding-bottom: 15px;
            margin-bottom: 25px;
        }}

        .header h1 {{
            color: #1e3a5f;
            margin: 0;
            font-size: 24px;
        }}

        .header .date {{
            color: #666;
            font-size: 14px;
            margin-top: 5px;
        }}

        .summary-box {{
            background: #f0f7ff;
            border-left: 4px solid #2563eb;
            padding: 15px 20px;
            margin: 20px 0;
            border-radius: 0 4px 4px 0;
        }}

        .summary-box h2 {{
            color: #1e3a5f;
            margin: 0 0 10px 0;
            font-size: 16px;
        }}

        .essay-content {{
            margin: 25px 0;
        }}

        .essay-content h2 {{
            color: #1e3a5f;
            font-size: 18px;
            margin-top: 25px;
        }}

        .sentiment {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .sentiment.positive {{ background: #dcfce7; color: #166534; }}
        .sentiment.negative {{ background: #fee2e2; color: #991b1b; }}
        .sentiment.neutral {{ background: #f3f4f6; color: #4b5563; }}

        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
            text-align: center;
            font-size: 12px;
            color: #9ca3af;
        }}

        /* Impact Section */
        .impact-section {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 20px;
            margin: 25px 0;
        }}

        .impact-section h2 {{
            color: #1e3a5f;
            font-size: 18px;
            margin-top: 0;
        }}

        /* Fundamental Grid */
        .fundamental-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}

        .fundamental-card {{
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 12px;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }}

        .fundamental-card .label {{
            display: block;
            font-size: 10px;
            color: #64748b;
            text-transform: uppercase;
            font-weight: 600;
            margin-bottom: 4px;
            letter-spacing: 0.5px;
        }}

        .fundamental-card .value {{
            display: block;
            font-weight: 700;
            color: #1e3a5f;
            font-size: 18px;
        }}

        /* Impact Table */
        .impact-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            font-size: 13px;
        }}

        .impact-table th {{
            text-align: left;
            padding: 10px;
            background: #f1f5f9;
            color: #475569;
            border-bottom: 2px solid #e2e8f0;
        }}

        .impact-table td {{
            padding: 10px;
            border-bottom: 1px solid #e2e8f0;
        }}

        .impact-badge {{
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: 600;
            font-size: 11px;
            text-transform: uppercase;
        }}

        .impact-very-high {{ background: #fee2e2; color: #991b1b; }}
        .impact-high {{ background: #ffedd5; color: #9a3412; }}
        .impact-medium {{ background: #fef9c3; color: #854d0e; }}
        .impact-low {{ background: #f1f5f9; color: #475569; }}

        .price-change {{ font-weight: 600; }}
        .price-up {{ color: #166534; }}
        .price-down {{ color: #991b1b; }}

        /* Chart Styles */
        .timeframe-selector {{
            display: flex;
            gap: 8px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }}

        .timeframe-btn {{
            background: #e2e8f0;
            border: none;
            color: #475569;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            font-size: 13px;
            transition: all 0.2s;
        }}

        .timeframe-btn:hover {{ background: #cbd5e1; }}
        .timeframe-btn.active {{ background: #2563eb; color: white; }}

        .chart-container {{
            height: 300px;
            margin-bottom: 10px;
        }}

        /* References */
        .references {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
        }}

        .references h3 {{
            color: #6b7280;
            font-size: 14px;
        }}

        .reference-item {{
            font-size: 12px;
            color: #6b7280;
            margin: 8px 0;
            padding-left: 25px;
            text-indent: -25px;
        }}

        .reference-item a {{
            color: #2563eb;
            word-break: break-all;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Stock News Analysis: {company_name}</h1>
            <div class="date">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}</div>
            <div class="date">
                Stocks: {ticker}
                {f" | Sectors: {sector}" if sector else ""}
            </div>
            <span class="sentiment {sentiment_class}">{sentiment_label}</span>
        </div>

        <div class="summary-box">
            <h2>📌 Executive Summary</h2>
            <p>{analysis.get('summary', 'Analysis in progress...')}</p>
        </div>

        {fundamentals_html}

        <div class="impact-section">
            <h2>📈 Price Performance Overview</h2>
            <div class="timeframe-selector">
                <button class="timeframe-btn" onclick="updateChart('1d')">1d</button>
                <button class="timeframe-btn" onclick="updateChart('1wk')">1w</button>
                <button class="timeframe-btn" onclick="updateChart('1mo')">1m</button>
                <button class="timeframe-btn" onclick="updateChart('3mo')">3m</button>
                <button class="timeframe-btn" onclick="updateChart('1y')">1y</button>
                <button class="timeframe-btn active" onclick="updateChart('10y')">10y</button>
            </div>
            <div class="chart-container">
                <canvas id="mainChart"></canvas>
            </div>
            <div style="font-size: 13px; color: #475569; background: #f1f5f9; padding: 10px; border-radius: 4px; margin-top: 20px;">
                <strong>Stock Profile:</strong> Dynamic price chart with news event markers (🔶).
            </div>
        </div>

        <div class="essay-content">
            {analysis.get('essay', '<p>Analysis pending...</p>')}
        </div>

        {impact_table_html}
        {references_html}

        <div class="footer">
            <p>© 2026 DeltaValue Investment Research | Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
        </div>
    </div>

    <script>
        const chartData = {chart_data_json};
        const allEvents = {events_json};
        let myChart = null;

        function updateChart(timeframe) {{
            document.querySelectorAll('.timeframe-btn').forEach(btn => {{
                btn.classList.toggle('active', btn.innerText === timeframe);
            }});

            const data = chartData[timeframe];
            if (!data || !data.data || data.data.length === 0) {{
                if (myChart) myChart.destroy();
                const ctx = document.getElementById('mainChart').getContext('2d');
                ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
                ctx.font = '14px -apple-system, sans-serif';
                ctx.fillStyle = '#64748b';
                ctx.textAlign = 'center';
                ctx.fillText('No data available for ' + timeframe, ctx.canvas.width / 2, 150);
                return;
            }}

            const labels = data.data.map(d => d.date);
            const prices = data.data.map(d => d.close);
            
            // Find nearest points for events
            const firstDate = new Date(labels[0]);
            const lastDate = new Date(labels[labels.length - 1]);
            const filteredEvents = allEvents.filter(e => {{
                if (!e.date) return false;
                const eDate = new Date(e.date);
                return eDate >= firstDate && eDate <= lastDate;
            }});

            const eventPoints = labels.map(() => null);
            const eventMeta = labels.map(() => null);
            
            filteredEvents.forEach(event => {{
                const eventDate = new Date(event.date);
                let nearestIdx = 0, minDiff = Infinity;
                labels.forEach((label, idx) => {{
                    const diff = Math.abs(new Date(label) - eventDate);
                    if (diff < minDiff) {{ minDiff = diff; nearestIdx = idx; }}
                }});
                eventPoints[nearestIdx] = prices[nearestIdx];
                eventMeta[nearestIdx] = event;
            }});

            if (myChart) myChart.destroy();

            myChart = new Chart(document.getElementById('mainChart').getContext('2d'), {{
                type: 'line',
                data: {{
                    labels: labels,
                    datasets: [{{
                        label: 'Price',
                        data: prices,
                        borderColor: '#2563eb',
                        backgroundColor: 'rgba(37, 99, 235, 0.1)',
                        borderWidth: 2,
                        pointRadius: 0,
                        fill: true,
                        tension: 0.1,
                        order: 2
                    }}, {{
                        label: 'Events',
                        data: eventPoints,
                        pointStyle: 'triangle',
                        pointRadius: 10,
                        pointHoverRadius: 14,
                        pointBackgroundColor: '#f59e0b',
                        pointBorderColor: '#dc2626',
                        pointBorderWidth: 2,
                        showLine: false,
                        order: 1
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {{ intersect: false, mode: 'nearest' }},
                    plugins: {{
                        legend: {{ display: false }},
                        tooltip: {{
                            backgroundColor: 'rgba(30, 58, 95, 0.95)',
                            padding: 12,
                            cornerRadius: 8,
                            displayColors: false,
                            callbacks: {{
                                title: ctx => {{
                                    if (ctx[0].datasetIndex === 1 && ctx[0].parsed.y !== null) {{
                                        const e = eventMeta[ctx[0].dataIndex];
                                        return e ? '📰 ' + e.title : '';
                                    }}
                                    return 'Price: $' + ctx[0].parsed.y.toFixed(2);
                                }},
                                label: ctx => {{
                                    if (ctx.datasetIndex === 1 && ctx.parsed.y !== null) {{
                                        const e = eventMeta[ctx.dataIndex];
                                        if (e) return ['📅 ' + e.date, '📰 ' + (e.source || ''), e.summary ? e.summary.substring(0, 80) + '...' : ''];
                                    }}
                                    return null;
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        x: {{ 
                            display: true, 
                            grid: {{ display: false }}, 
                            ticks: {{ 
                                maxTicksLimit: 8, 
                                font: {{ size: 11, weight: data.is_historical ? 'bold' : 'normal' }}, 
                                color: data.is_historical ? '#dc2626' : '#64748b'
                            }},
                            title: {{
                                display: data.is_historical === true,
                                text: '⚠️ Historical: ' + (data.trading_date || 'Last trading day'),
                                color: '#dc2626',
                                font: {{ size: 12, weight: 'bold' }}
                            }}
                        }},
                        y: {{ display: true, grid: {{ color: 'rgba(0,0,0,0.05)' }}, ticks: {{ font: {{ size: 11 }}, color: '#64748b', callback: v => '$' + v.toFixed(0) }} }}
                    }}
                }}
            }});
        }}

        updateChart('10y');
    </script>
</body>
</html>
'''

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        return filepath

    def _build_fundamentals_section(self, fundamentals: Dict, business_context: str = "") -> str:
        """Build fundamentals section matching original template strictly."""
        # Use empty dict if None to ensure section is built with defaults
        fundamentals = fundamentals or {}
        
        pe = fundamentals.get("pe_ratio", fundamentals.get("P/E Ratio", "N/A"))
        peg = fundamentals.get("peg_ratio", fundamentals.get("PEG Ratio", "N/A"))
        roe = fundamentals.get("roe", fundamentals.get("ROE", "N/A"))
        de = fundamentals.get("debt_to_equity", fundamentals.get("Debt/Equity", "N/A"))
        
        pe_str = f"{pe:.2f}" if isinstance(pe, (int, float)) else str(pe)
        peg_str = f"{peg:.2f}" if isinstance(peg, (int, float)) else str(peg)
        roe_str = f"{roe:.1f}%" if isinstance(roe, (int, float)) else str(roe)
        de_str = f"{de:.3f}" if isinstance(de, (int, float)) else str(de)

        target_mean = fundamentals.get("target_mean_price")
        target_high = fundamentals.get("target_high_price")
        target_low = fundamentals.get("target_low_price")
        recommendation = fundamentals.get("recommendation", "N/A")

        mean_str = f"${target_mean:.2f}" if isinstance(target_mean, (int, float)) else "N/A"
        high_str = f"${target_high:.2f}" if isinstance(target_high, (int, float)) else "N/A"
        low_str = f"${target_low:.2f}" if isinstance(target_low, (int, float)) else "N/A"

        # Always render analyst section to preserve layout
        analyst_section = f'''
        <div class="fundamental-grid" style="margin-top: 10px; background: #fff; padding: 10px; border-radius: 6px; border: 1px dashed #cbd5e1;">
            <div class="fundamental-card" style="border: none; box-shadow: none;">
                <span class="label">Analyst Target (Mean)</span>
                <span class="value">{mean_str}</span>
            </div>
            <div class="fundamental-card" style="border: none; box-shadow: none;">
                <span class="label">Analyst High</span>
                <span class="value" style="color: #166534;">{high_str}</span>
            </div>
            <div class="fundamental-card" style="border: none; box-shadow: none;">
                <span class="label">Analyst Low</span>
                <span class="value" style="color: #991b1b;">{low_str}</span>
            </div>
            <div class="fundamental-card" style="border: none; box-shadow: none;">
                <span class="label">Recommendation</span>
                <span class="value" style="font-size: 14px; text-transform: uppercase;">{recommendation}</span>
            </div>
        </div>
        '''

        context_section = ""
        if business_context:
            truncated = business_context[:500] + "..." if len(business_context) > 500 else business_context
            context_section = f'''
            <div style="font-size: 12px; line-height: 1.4; color: #475569; border-top: 1px solid #e2e8f0; padding-top: 12px; margin-top: 15px;">
                <strong>Business Context:</strong> {truncated}
            </div>
            '''

        return f'''
        <div class="impact-section">
            <h2>💎 Quality & Valuation Metrics (Buffett/Lynch Style)</h2>
            <div class="fundamental-grid">
                <div class="fundamental-card">
                    <span class="label">Valuation: P/E Ratio</span>
                    <span class="value">{pe_str}</span>
                </div>
                <div class="fundamental-card" title="Peter Lynch's favorite metric: Growth at Reasonable Price">
                    <span class="label">Growth: PEG Ratio</span>
                    <span class="value">{peg_str}</span>
                </div>
                <div class="fundamental-card" title="Warren Buffett's core quality indicator">
                    <span class="label">Quality: ROE</span>
                    <span class="value">{roe_str}</span>
                </div>
                <div class="fundamental-card">
                    <span class="label">Health: Debt/Equity</span>
                    <span class="value">{de_str}</span>
                </div>
            </div>
            {analyst_section}
            {context_section}
        </div>
        '''

    def _build_impact_table(self, events: List[Dict]) -> str:
        """Build news impact analysis table matching original template."""
        if not events:
            return ""
        
        rows = []
        for e in events[:15]:
            title = e.get("title", "Unknown")
            if len(title) > 70:
                title = title[:67] + "..."
            
            category = e.get("category", "News")
            impact = e.get("impact", "medium").lower()
            price_change = e.get("price_change", 0)
            url = e.get("url", "")
            
            impact_class = f"impact-{impact.replace(' ', '-')}"
            impact_label = impact.replace("-", " ").title()
            
            if isinstance(price_change, (int, float)):
                price_class = "price-up" if price_change >= 0 else "price-down"
                price_str = f"+{price_change:.2f}%" if price_change >= 0 else f"{price_change:.2f}%"
            else:
                price_class = ""
                price_str = "N/A"

            title_html = f'<a href="{url}" target="_blank">{title}</a>' if url else title
            
            rows.append(f'''
                <tr>
                    <td style="max-width: 300px; font-weight: 500;">{title_html}</td>
                    <td>{category}</td>
                    <td><span class="impact-badge {impact_class}">{impact_label}</span></td>
                    <td><span class="price-change {price_class}">{price_str}</span></td>
                </tr>
            ''')
        
        return f'''
        <div class="impact-section">
            <h2>📈 News Impact Analysis (10y History)</h2>
            <p style="font-size: 14px; color: #64748b; margin-bottom: 15px;">
                Correlating news types with historical price movements to identify high-signal events.
            </p>
            <table class="impact-table">
                <thead>
                    <tr>
                        <th>Article / Event</th>
                        <th>Category</th>
                        <th>Historical Impact</th>
                        <th>Price Correl.</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(rows)}
                </tbody>
            </table>
        </div>
        '''

    def _build_references(self, references: List[Dict]) -> str:
        """Build references section."""
        if not references:
            return ""
        
        items = []
        for i, ref in enumerate(references[:30], 1):
            title = ref.get("title", "Source")
            url = ref.get("url", "#")
            source = ref.get("source", "")
            date = ref.get("date", "")
            
            items.append(f'''
                <div class="reference-item" id="ref-{i}">
                    [{i}] {title}. {source}. {date}. <a href="{url}" target="_blank">{url[:80]}{"..." if len(url) > 80 else ""}</a>
                </div>
            ''')
        
        return f'''
        <div class="references">
            <h3>📚 References</h3>
            {''.join(items)}
        </div>
        '''
