import type { Stock, NewsItem, Report, Essay, AnalysisResult, SectorPerformance, SparklineResponse } from '../types';

// ==================== Helper Functions ====================

/**
 * Calculate Levenshtein distance between two strings
 * Used for fuzzy typo matching (e.g., "ROUCHE" → "ROCHE")
 */
function levenshteinDistance(a: string, b: string): number {
    const matrix: number[][] = [];

    for (let i = 0; i <= b.length; i++) {
        matrix[i] = [i];
    }
    for (let j = 0; j <= a.length; j++) {
        matrix[0][j] = j;
    }

    for (let i = 1; i <= b.length; i++) {
        for (let j = 1; j <= a.length; j++) {
            if (b.charAt(i - 1) === a.charAt(j - 1)) {
                matrix[i][j] = matrix[i - 1][j - 1];
            } else {
                matrix[i][j] = Math.min(
                    matrix[i - 1][j - 1] + 1, // substitution
                    matrix[i][j - 1] + 1,     // insertion
                    matrix[i - 1][j] + 1      // deletion
                );
            }
        }
    }

    return matrix[b.length][a.length];
}

// Mock Data Storage
const STOCKS: Stock[] = [
    { symbol: "ACME", name: "ACME Corp", sector: "Industrials", price: 154.20, change: 2.5, history: Array.from({ length: 4000 }, (_, i) => 100 + i * 0.05 + Math.random() * 20) },
    { symbol: "ABSI", name: "Absci Corp", sector: "Healthcare", price: 4.50, change: 2.5, history: Array.from({ length: 4000 }, (_, i) => 10 + i * -0.005 + Math.random() * 2) },
    { symbol: "NVO", name: "Novo Nordisk", sector: "Healthcare", price: 120.50, change: 1.2, history: Array.from({ length: 4000 }, (_, i) => 50 + i * 0.04 + Math.random() * 15) },
    { symbol: "LLY", name: "Eli Lilly", sector: "Healthcare", price: 750.00, change: -0.5, history: Array.from({ length: 4000 }, (_, i) => 200 + i * 0.3 + Math.random() * 20) },
    { symbol: "ROG", name: "Roche Holding", sector: "Healthcare", price: 280.00, change: 0.1, history: Array.from({ length: 4000 }, () => 300 + Math.random() * 50) },
    { symbol: "MBG", name: "Mercedes-Benz Group", sector: "Automotive", price: 62.50, change: 1.5, history: Array.from({ length: 4000 }, (_, i) => 40 + i * 0.01 + Math.random() * 10) }
];

// Alias Map for fuzzy lookup (Simulating Google Search Knowledge Graph)
const ALIASES: Record<string, string> = {
    // Tech / ACME
    "GOOGLE": "ACME", "GOOG": "ACME", "GOOGL": "ACME", "ALPHABET": "ACME",
    "GOGLE": "ACME", "ALFABET": "ACME", // Typos
    // Healthcare / Novo
    "NOVO": "NVO", "NOVO-B": "NVO", "NOVO NORDISK": "NVO", "NOWO": "NVO",
    // Healthcare / Lilly
    "LILLY": "LLY", "ELI LILLY": "LLY", "LILY": "LLY",
    // Healthcare / Roche
    "ROCHE": "ROG", "ROCH": "ROG",
    // Healthcare / Absci
    "ABSCI": "ABSI", "ABSI CORP": "ABSI",
    // Automotive (New Mocks)
    "MERCEDES": "MBG", "DAIMLER": "MBG", "MBG": "MBG",
    "BMW": "BMW", "BAYERISCHE": "BMW",
    "SIEMENS": "SIE", "SIEMENS AG": "SIE"
};

const REPORTS: Record<string, Report> = {
    "ACME": {
        stock: "ACME",
        summary: "ACME ist ein Strong Buy basierend auf Marktführerschaft, soliden Finanzkennzahlen und klaren Wachstumskatalysatoren.",
        deepAnalysis: "## Strategic Position\nACME continues to dominate the industrial AI sector with a 40% market share.\n\n## Operational Efficiency\nMargins have improved by 200bps YoY due to supply chain optimization.\n\n## Risk Assessment\nCompetition from startups is increasing, but ACME's moat remains wide.",
        reviewData: {
            peRatio: 24.50,
            pegRatio: 1.80,
            roe: 18.5,
            debtToEquity: 0.450
        },
        analystRatings: {
            mean: 165.00,
            high: 190.00,
            low: 130.00,
            recommendation: "BUY"
        },
        riskAssessment: {
            level: 'Low',
            description: "Strong balance sheet and diversified revenue streams mitigate sector cyclicality."
        },
        marketSentiment: {
            trend: 'Bullish',
            score: 85
        },
        businessContext: "ACME Corporation is a leading provider of AI-powered manufacturing solutions. The company's innovative platform combines machine learning with industrial automation.",
        generatedAt: new Date().toISOString()
    },
    "ABSI": {
        stock: "ABSI",
        summary: "Absci shows strong potential in generative AI drug creation. Cash burn remains a risk, but recent validation from partnerships creates upside.",
        deepAnalysis: "## Technology Platform\nAbsci's Integrated Drug Creation Platform utilizes zero-shot generative AI to design antibodies.\n\n## Clinical Pipeline\nKey readouts expected in Q4 2025 regarding the detailed phase 1 trial.\n\n## Financial Health\nCash runway extends into 2026, lowering near-term dilution risk.",
        reviewData: {
            peRatio: -15.4,
            pegRatio: -0.5,
            roe: -22.1,
            debtToEquity: 0.1
        },
        analystRatings: {
            mean: 9.00,
            high: 17.00,
            low: 4.00,
            recommendation: "BUY"
        },
        riskAssessment: {
            level: 'High',
            description: "Typical biotech development risks; high volatility expected pending trial data."
        },
        marketSentiment: {
            trend: 'Neutral',
            score: 55
        },
        businessContext: "Absci Corporation is a generative AI drug creation company. It uses deep learning models to design antibodies with specific characteristics.",
        generatedAt: new Date().toISOString()
    },
    // New Generic Reports for Search Hits
    "MBG": {
        stock: "MBG",
        summary: "Mercedes-Benz Group AG focuses on high-end luxury cars and vans. The pivot to EV varies in adoption speed.",
        deepAnalysis: "## Luxury Strategy\nFocus on margins over volume has improved profitability.\n\n## EV Transition\nSlower than expected uptake in key markets creates inventory risks.",
        reviewData: { peRatio: 5.5, pegRatio: 0.8, roe: 14.2, debtToEquity: 0.8 },
        analystRatings: { mean: 75.00, high: 90.00, low: 55.00, recommendation: "HOLD" },
        riskAssessment: { level: 'Medium', description: "Cyclical auto industry exposure and EV execution risks." },
        marketSentiment: { trend: 'Bearish', score: 40 },
        businessContext: "Mercedes-Benz Group AG is one of the world's most successful automotive companies.",
        generatedAt: new Date().toISOString()
    },
    "NVO": {
        stock: "NVO",
        summary: "Novo Nordisk stays dominant in the GLP-1 market despite supply constraints. Demand for Wegovy remains unprecedented.",
        deepAnalysis: "## GLP-1 Market Leader\nNVO captures 55% of the global obesity market value.\n\n## Supply Chain\nInvestments of $6B in manufacturing are underway to alleviate shortages.",
        reviewData: { peRatio: 42.1, pegRatio: 2.3, roe: 86.4, debtToEquity: 0.2 },
        analystRatings: { mean: 135.00, high: 155.00, low: 110.00, recommendation: "BUY" },
        riskAssessment: { level: 'Medium', description: "Valuation perfection priced in; supply chain execution is critical." },
        marketSentiment: { trend: 'Bullish', score: 92 },
        businessContext: "Novo Nordisk is a global healthcare company with more than 95 years of innovation and leadership in diabetes care.",
        generatedAt: new Date().toISOString()
    },
    "LLY": {
        stock: "LLY",
        summary: "Eli Lilly's pipeline specifically Zepbound is outperforming expectations. The company is effectively challenging Novo's dominance.",
        deepAnalysis: "## Pipeline Power\nDonanemab approval provides a new vertical in Alzheimer's treatment.\n\n## Obesity War\nZepbound launch trajectory is steeper than Wegovy's early days.",
        reviewData: { peRatio: 110.5, pegRatio: 3.1, roe: 64.2, debtToEquity: 1.5 },
        analystRatings: { mean: 850.00, high: 950.00, low: 700.00, recommendation: "STRONG_BUY" },
        riskAssessment: { level: 'High', description: "Extremely rich valuation leaves no room for earnings misses." },
        marketSentiment: { trend: 'Bullish', score: 88 },
        businessContext: "Eli Lilly and Company is an American pharmaceutical company headquartered in Indianapolis, Indiana.",
        generatedAt: new Date().toISOString()
    },
    "ROG": {
        stock: "ROG",
        summary: "Roche faces headwinds from biosimilars but maintains a strong diagnostics division. Recent M&A in obesity space (Carmot) signals pivot.",
        deepAnalysis: "## Diagnostics Moat\nDiagnostics division provides stable cash flow to fund Pharma R&D.\n\n## Pivot to Obesity\nCarmot acquisition allows late entry into GLP-1 market with differentiated assets.",
        reviewData: { peRatio: 14.2, pegRatio: 1.5, roe: 32.0, debtToEquity: 0.6 },
        analystRatings: { mean: 310.00, high: 340.00, low: 260.00, recommendation: "HOLD" },
        riskAssessment: { level: 'Low', description: "Defensive profile with high dividend yield and low volatility." },
        marketSentiment: { trend: 'Neutral', score: 50 },
        businessContext: "F. Hoffmann-La Roche AG is a Swiss multinational healthcare company that operates worldwide.",
        generatedAt: new Date().toISOString()
    }
};

const ESSAYS: Record<string, Essay> = {
    "ACME": {
        stock: "ACME",
        text: "## ACME's Market Dominance\nACME has established itself as the standard for AI manufacturing. Their proprietary algorithms allow for predictive maintenance that saves clients millions annually.\n\n### Future Outlook\nExpansion into aerospace and defense sectors provides significant TAM expansion. The recent contract with the DoD validates their security protocols and reliability standards."
    },
    "ABSI": {
        stock: "ABSI",
        text: "## The AI Revolution in Biology\nAbsci is pioneering the use of generative AI to design antibodies from scratch. Unlike traditional screening, this 'zero-shot' approach could drastically reduce lead optimization time.\n\n### Generative vs Discriminative\nTraditional logic screens existing libraries. Absci creates new sequences de novo, accessing a chemical space previously unreachable."
    },
    "MBG": {
        stock: "MBG",
        text: "## Luxury Defined\nMercedes continues to set the standard for automotive luxury.\n\n### The Chinese Market\nKey to future growth but facing stiff local competition."
    },
    "NVO": {
        stock: "NVO",
        text: "## The Obesity Gold Rush\nNovo Nordisk has effectively created the modern obesity market with semaglutide. The brand equity of Ozempic has effectively become a household name.\n\n### Capacity Constraints\nThe primary limiter on NVO's growth is not demand, but manufacturing capacity. The $6B investment in new facilities demonstrates commitment to solving this bottleneck."
    },
    "LLY": {
        stock: "LLY",
        text: "## Challenging the Throne\nEli Lilly's Zepbound (tirzepatide) has shown superior efficacy in head-to-head trials against semaglutide. This dual-agonist approach represents the next generation of weight loss drugs.\n\n### Alzheimer's Catalyst\nBeyond obesity, donanemab represents a massive potential blockbuster if approval hurdles are cleared and reimbursement is secured."
    },
    "ROG": {
        stock: "ROG",
        text: "## A Strategic Pivot\nRoche has long been dominant in Oncology and Diagnostics. The recent acquisition of Carmot Therapeutics signals a decisive entry into the metabolic disease space.\n\n### Defensive Posture\nWith a strong dividend and lower volatility, Roche serves as a ballast in healthcare portfolios compared to the high-beta obesity pure plays."
    }
};

const ALL_NEWS: NewsItem[] = [
    { title: "ACME Signs Defense Contract", sector: "Industrials", source: "Bloomberg", timestamp: "10:05 AM" },
    { title: "Breakthrough in AI Drug Discovery", sector: "Healthcare", source: "DeepWeb", timestamp: "09:30 AM" },
    { title: "Mercedes Unveils New EQ Concept", sector: "Automotive", source: "AutoNews", timestamp: "09:15 AM" }, // New
    { title: "Tech Sector Rallies on Earnings", sector: "Technology", source: "Reuters", timestamp: "09:15 AM" },
    { title: "Novo Nordisk Supply Chain Update", sector: "Healthcare", source: "Company PR", timestamp: "08:45 AM" },
    { title: "Lilly's Zepbound Sales Beat Targets", sector: "Healthcare", source: "Bloomberg", timestamp: "08:30 AM" },
    { title: "Roche Diagnostics receives FDA clearance", sector: "Healthcare", source: "FDA Watch", timestamp: "08:15 AM" },
    { title: "European Pharma Index Hits All-Time High", sector: "Healthcare", source: "Reuters", timestamp: "08:10 AM" },
    { title: "Global Markets Brace for Rate Hikes", sector: "General", source: "WSJ", timestamp: "08:00 AM" },
    { title: "Semiconductor Shortage Eases", sector: "Technology", source: "TechCrunch", timestamp: "07:45 AM" },
];

const SECTOR_PERFORMANCE: SectorPerformance[] = [
    {
        id: "Technology",
        name: "Technology",
        performance: 1.25,
        market_cap: 15600000000000,
        top_stocks: [
            { symbol: "AAPL", name: "Apple Inc.", performance: 1.10, market_cap: 3400000000000 },
            { symbol: "MSFT", name: "Microsoft", performance: 0.85, market_cap: 3100000000000 },
            { symbol: "NVDA", name: "NVIDIA", performance: 2.40, market_cap: 2800000000000 }
        ]
    },
    {
        id: "Healthcare",
        name: "Healthcare",
        performance: -0.45,
        market_cap: 8400000000000,
        top_stocks: [
            { symbol: "LLY", name: "Eli Lilly", performance: -0.20, market_cap: 850000000000 },
            { symbol: "UNH", name: "UnitedHealth", performance: -0.60, market_cap: 520000000000 },
            { symbol: "JNJ", name: "J&J", performance: 0.15, market_cap: 380000000000 }
        ]
    },
    {
        id: "Financials",
        name: "Financials",
        performance: 0.35,
        market_cap: 9200000000000,
        top_stocks: [
            { symbol: "JPM", name: "JPMorgan", performance: 0.45, market_cap: 580000000000 },
            { symbol: "V", name: "Visa", performance: 0.20, market_cap: 540000000000 },
            { symbol: "MA", name: "Mastercard", performance: 0.30, market_cap: 420000000000 }
        ]
    },
    {
        id: "Energy",
        name: "Energy",
        performance: -1.10,
        market_cap: 3800000000000,
        top_stocks: [
            { symbol: "XOM", name: "ExxonMobil", performance: -1.25, market_cap: 480000000000 },
            { symbol: "CVX", name: "Chevron", performance: -0.95, market_cap: 290000000000 },
            { symbol: "TTE", name: "TotalEnergies", performance: -1.40, market_cap: 160000000000 }
        ]
    }
];

export const MockApiService = {
    getStocks: async (): Promise<Stock[]> => {
        return new Promise(resolve => setTimeout(() => resolve(STOCKS), 100));
    },

    // Old method for compatibility (deprecated internally)
    resolveSymbol: (input: string): string | null => {
        const up = input.toUpperCase().trim();
        const exact = STOCKS.find(s => s.symbol === up);
        if (exact) return exact.symbol;
        return ALIASES[up] || null;
    },

    // NEW: Search Method
    searchStock: async (query: string): Promise<{ symbol: string, sector: string, confidence: number } | null> => {
        // Simulate Network Delay
        await new Promise(r => setTimeout(r, 300));

        const up = query.toUpperCase().trim();

        // 1. Direct or Alias Match
        if (ALIASES[up]) {
            const resolvedSymbol = ALIASES[up];
            // Lookup real sector
            const stock = STOCKS.find(s => s.symbol === resolvedSymbol);
            return {
                symbol: resolvedSymbol,
                sector: stock ? stock.sector : "General",
                confidence: 0.95
            };
        }

        // 2. Mock "Google Search" fuzzy logic
        // Check keys for partial match
        const aliasMatch = Object.keys(ALIASES).find(key => key.includes(up) || up.includes(key));
        if (aliasMatch) {
            const resolvedSymbol = ALIASES[aliasMatch];
            const stock = STOCKS.find(s => s.symbol === resolvedSymbol);
            return {
                symbol: resolvedSymbol,
                sector: stock ? stock.sector : "General",
                confidence: 0.85
            };
        }

        // 3. Fuzzy typo tolerance (simple Levenshtein-like)
        // Check if input is within 1-2 character edits of a known alias
        const fuzzyMatch = Object.keys(ALIASES).find(key => {
            const distance = levenshteinDistance(up, key);
            return distance <= 2; // Allow up to 2 typos
        });
        if (fuzzyMatch) {
            const resolvedSymbol = ALIASES[fuzzyMatch];
            const stock = STOCKS.find(s => s.symbol === resolvedSymbol);
            console.log(`[Fuzzy Match] ${query} → ${fuzzyMatch} → ${resolvedSymbol}`);
            return {
                symbol: resolvedSymbol,
                sector: stock ? stock.sector : "General",
                confidence: 0.75
            };
        }

        return null;
    },

    // Fuzzy Language Resolution
    resolveLanguage: (input: string): string => {
        const lower = input.toLowerCase().trim();
        if (["de", "ger", "german", "deutsch"].some(x => lower.includes(x))) return "German";
        if (["en", "eng", "english", "englisch"].some(x => lower.includes(x))) return "English";
        if (["fr", "fra", "french", "französisch"].some(x => lower.includes(x))) return "French";
        if (["tr", "tur", "turkish", "türkisch"].some(x => lower.includes(x))) return "Turkish";
        return "English"; // Default
    },

    runAnalysis: async (ticker: string, _sector: string, language: string = "English"): Promise<AnalysisResult> => {
        return new Promise(resolve => {
            setTimeout(() => {
                // Find stock or fallback to ACME
                let cleanTicker = ticker.toUpperCase();
                if (ALIASES[cleanTicker]) cleanTicker = ALIASES[cleanTicker];
                const stock = STOCKS.find(s => s.symbol === cleanTicker) || STOCKS[0];

                // --- Multilingual Mock Content Generation ---
                let baseReport = REPORTS[cleanTicker] ? { ...REPORTS[cleanTicker] } : null;
                let baseEssay = ESSAYS[cleanTicker] ? { ...ESSAYS[cleanTicker] } : null;

                // Fallback Generator if no specific mock data exists
                if (!baseReport) {
                    baseReport = {
                        stock: cleanTicker,
                        summary: `${cleanTicker} (${stock.name}) is a key player in the ${stock.sector} sector. Current market conditions show mixed signals.`,
                        deepAnalysis: `## Market Position\n${stock.name} maintains a stable position in ${stock.sector}.\n\n## Financials\nRecent price action around $${stock.price} suggests consolidation.`,
                        reviewData: { peRatio: 20.0, pegRatio: 1.5, roe: 15.0, debtToEquity: 1.0 },
                        analystRatings: { mean: stock.price * 1.1, high: stock.price * 1.3, low: stock.price * 0.9, recommendation: "HOLD" },
                        riskAssessment: { level: 'Medium', description: "Standard sector risks apply." },
                        marketSentiment: { trend: 'Neutral', score: 50 },
                        businessContext: `${stock.name} operates primarily in the ${stock.sector} industry.`,
                        generatedAt: new Date().toISOString()
                    };
                }

                if (!baseEssay) {
                    baseEssay = {
                        stock: cleanTicker,
                        text: `## Analysis of ${stock.name}\n\n### Sector Context\nThe ${stock.sector} sector is currently navigating macroeconomic headwinds. ${stock.name} is positioned to adapt to these changes.\n\n### Outlook\nInvestors should monitor upcoming earnings reports for ${cleanTicker} to gauge future performance.`
                    };
                }

                // Simple German Translation Override for Demo
                if (language === "German") {
                    if (cleanTicker === "ACME") {
                        baseReport.summary = "ACME bleibt ein starker Kauf aufgrund der Marktführerschaft und solider Finanzdaten.";
                        baseReport.riskAssessment = { level: 'Low', description: "Starke Bilanz und diversifizierte Einnahmen mindern zyklische Risiken." };
                        baseReport.marketSentiment = { trend: 'Bullish', score: 85 };
                        baseEssay.text = "## ACMEs Marktdominanz\nACME hat sich als Standard für KI-Fertigung etabliert.\n\n### Zukunftsaussichten\nDie Expansion in Luft- und Raumfahrt bietet erhebliches Wachstumspotenzial.";
                    } else if (cleanTicker === "MBG") {
                        baseReport.summary = "Mercedes-Benz Group AG fokussiert sich auf Luxusautos. Die EV-Strategie variiert in der Geschwindigkeit.";
                        baseReport.riskAssessment = { level: 'Medium', description: "Zyklische Autoindustrie und Ausführungsrisiken bei EVs." };
                        baseEssay.text = "## Luxus Definiert\nMercedes setzt weiterhin den Standard für automobilen Luxus.\n\n### Der Chinesische Markt\nSchlüssel für zukünftiges Wachstum, aber mit starker lokaler Konkurrenz.";
                    } else {
                        // Generic Fallback for other stocks in German
                        baseReport.summary = `(DE) ${baseReport.summary}`;
                        baseEssay.text = `## (DE) Analyse für ${stock.name}\n\n${baseEssay.text}`;
                    }
                } else if (language !== "English") {
                    // Universal Simulator for other languages (Turkish, French, etc.)
                    const langPrefix = `(${language.toUpperCase().substring(0, 2)})`;
                    baseReport.summary = `${langPrefix} ${baseReport.summary}`;
                    baseEssay.text = `## ${langPrefix} Analysis of ${stock.name}\n\n${baseEssay.text}`;
                }

                const result: AnalysisResult = {
                    report: { ...baseReport, generatedAt: new Date().toISOString() },
                    stockNews: ALL_NEWS.filter(n => n.title.toUpperCase().includes(cleanTicker) || n.title.toUpperCase().includes(stock.name.toUpperCase())),
                    sectorNews: ALL_NEWS.filter(n => n.sector === stock.sector || n.sector === "General"),
                    essay: baseEssay.text,
                    chartData: stock.history.map((val: number, i: number) => {
                        // Generate relative dates from "Full History"
                        const daysAgo = stock.history.length - 1 - i;
                        return {
                            date: new Date(Date.now() - daysAgo * 86400000).toISOString().split('T')[0],
                            value: val
                        };
                    }),
                    // [NEW] 48h Hourly Volume Data
                    volumeData: Array.from({ length: 48 }, (_, i) => {
                        const hoursAgo = 47 - i;
                        const date = new Date(Date.now() - hoursAgo * 3600000);
                        // Simulate higher volume during market hours (9-16)
                        const hour = date.getHours();
                        const isMarketOpen = hour >= 9 && hour <= 16;
                        const baseVol = isMarketOpen ? Math.random() * 500000 + 100000 : Math.random() * 50000 + 10000;

                        return {
                            date: date.toISOString(), // ISO timestamp for hour
                            value: stock.price + (Math.random() - 0.5), // Price at that hour (approx)
                            volume: Math.floor(baseVol)
                        };
                    })
                };
                resolve(result);
            }, 1000);
        });
    },

    getSectorPerformance: async (period: string = '1d'): Promise<SectorPerformance[]> => {
        return new Promise(resolve => {
            setTimeout(() => {
                // Return a modified version of SECTOR_PERFORMANCE based on period for realism
                const multiplier = period === '1y' ? 15 : period === '1m' ? 3 : period === '1w' ? 1.5 : 1;
                resolve(SECTOR_PERFORMANCE.map(s => ({
                    ...s,
                    performance: s.performance * multiplier,
                    top_stocks: s.top_stocks.map(ts => ({
                        ...ts,
                        performance: ts.performance * multiplier
                    }))
                })));
            }, 300);
        });
    },

    getSparklineData: async (ticker: string, period: string = '1w'): Promise<SparklineResponse> => {
        return new Promise(resolve => {
            setTimeout(() => {
                // Generate random walk data for sparkline
                const points = 24;
                const data = [100];
                for (let i = 1; i < points; i++) {
                    const prev = data[i - 1];
                    const change = (Math.random() - 0.5) * 4;
                    data.push(Number((prev + change).toFixed(2)));
                }
                resolve({
                    ticker: ticker.toUpperCase(),
                    period,
                    data,
                    source: 'browser.mock'
                });
            }, 150);
        });
    }
};
