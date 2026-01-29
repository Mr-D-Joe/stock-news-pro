# IDEAS — Strategic Backlog & Roadmap

> **Status:** Informal Collection  
> **Purpose:** Storage for feature ideas before they are formalized into `LASTENHEFT.md`.

## 1. Thematic Analysis (Schlagwortsuche)
**Concept:** Instead of searching for a stock, the user searches for a trend (e.g., "AI", "Obesity", "War").
**Goal:** Identify winners/losers and provide a thematic report.

### Draft Requirements
- **Theme Input:** Free text input for global themes.
- **Winner/Loser Identification:** Logic to map themes to specific sectors or stocks.
    - *Challenge:* Requires broad knowledge integration (LLM perfect fit).
- **Thematic Essay:** A dedicated report type focusing on the *theme's impact* rather than a single stock.
- **Risk/Chance Mapping:** Explicit list of "Tailwinds" (Chances) and "Headwinds" (Risks) for affected industries.

---

## 2. Portfolio Management (Depotübersicht)
**Concept:** User enters their actual holdings to get a personalized risk/value analysis.
**Goal:** "My Wealth at a Glance" with actionable insights.

### Draft Requirements
- **Persistence:** Local storage (JSON/SQLite) of user holdings (Symbol, Amount, Buy Price?).
- **Portfolio Dashboard:** A new view mode showing:
    - Total Value (Real-time approx).
    - Allocation (Pie Chart).
    - Aggregate Risk Score.
- **Asset Breakdown:** List view with mini-analysis per position.
- **Privacy:** Data must stay local (Desktop App strength!).

---

## 3. Personalized Start Screen
**Concept:** Allow the user to choose their entry point.
**Goal:** High-frequency users want their Portfolio immediately, not a generic search.

### Draft Requirements
- **Configuration:** New setting `default_view` (Enum: `HERO`, `PORTFOLIO`).
- **Startup Logic:** Router checks config before rendering initial layout.

---

## 4. Next Tasks (Proposed Priority)
1. **Refine Keyword Search:** Low tech risk, high AI value. Fits current "Search -> Analyze" flow well.
2. **Portfolio Data Layer:** Needs new persistence layer (Local DB/File). Higher architectural impact.
3. **Portfolio UI:** Dependent on Data Layer.
