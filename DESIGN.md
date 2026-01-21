# DESIGN.md — Project Constitution
# Stock News Pro

⚠️ **THIS DOCUMENT IS NORMATIVE AND IMMUTABLE**

This file is the **single source of truth** for:
- UI structure
- architecture
- technology decisions
- layout rules
- component responsibilities
- frontend/backend boundaries

It **overrides and supersedes**:
- README.md
- SYSTEM_REPORT.md
- any other markdown or documentation
- any LLM-generated analysis, suggestions, or refactorings
- all historical design decisions

---

## LLM COMPLIANCE RULES (NON-NEGOTIABLE)

All LLMs (including but not limited to Gemini, Claude, OpenAI, Anthropic models):

MUST:
- read this document in full before producing any output
- follow it **exactly**
- treat every rule as binding law

MUST NOT:
- modify this document
- rewrite, summarize, reorder, or reformat it
- reinterpret rules creatively
- infer missing requirements
- introduce alternative architectural approaches

If requirements are missing or unclear, they MUST be **reported explicitly** and NOT invented.

Violation of this document constitutes a **hard failure**.

---

## DOCUMENT PRIORITY ORDER (BINDING)

1. DESIGN.md (this document) — **binding law**
2. SYSTEM_REPORT.md — descriptive audit report only (non-normative)
3. README.md — informational, non-binding
4. Code comments — non-authoritative

---

## UI LAYOUT & SCALING RULES  
### (JavaFX — Legacy Notes, Non-Extensible)

This section documents **historical constraints** from the JavaFX phase.
It exists for **reference only**.

JavaFX is **deprecated** and must not be extended.

---

## 1. Core Design Principle

> **Function beats appearance. Always.**

The UI must remain:
- stable
- deterministic
- readable
- scalable

at **any window size**.

If a visual or stylistic choice violates layout stability, it is **forbidden**.

---

## 2. Fundamental Constraint

> **Text must NEVER control container width.**

Containers define width.  
Text adapts to containers — **never the other way around**.

Any implementation that allows text to influence layout width is a **bug**.

---

## 3. Text Rules (Strict)

### Allowed
- `TextAlignment.LEFT`
- `setWrapText(true)`
- `setMaxWidth(Double.MAX_VALUE)`

### Forbidden (No Exceptions)
- `TextAlignment.JUSTIFY`
- CSS `-fx-text-alignment: justify`
- Dynamic width bindings on text or labels
- Any attempt to “fill” horizontal space via text alignment

**Reason:**  
Justified text introduces non-linear spacing and breaks responsive layouts.

---

## 4. Scaling Rules

### 4.1 Font Scaling (Allowed)
- Applied **only** at root node
- Via CSS only:
  ```css
  -fx-font-size: <scaled-value>px;

	•	Optional dampening (e.g. sqrt(width))

4.2 Padding & Spacing (Forbidden to Scale)
	•	Padding and spacing MUST be fixed values
	•	No bindings
	•	No heuristics
	•	No proportional scaling

Reason:
Scaled padding causes container growth and layout instability when text wraps.

⸻

5. Width Management Rules

Allowed
	•	setMaxWidth(<reasonable value>)
	•	Editorial / readable widths (760–900px)
	•	Centering via parent containers

Forbidden
	•	prefWidthProperty().bind(...)
	•	layoutBoundsProperty() feedback loops
	•	Width calculations based on text metrics
	•	Scale transforms (ScaleX, ScaleY)

⸻

6. Centering Strategy (Mandatory Pattern)

Center content by constraining width, not by stretching text.

Canonical pattern:
	•	Outer container expands freely
	•	Inner container has a defined maxWidth
	•	No width bindings
	•	No scale transforms

⸻

7. Approved Layout Utility (Legacy)

CenteredContentPane

Characteristics:
	•	Outer container expands freely
	•	Inner container has a max readable width
	•	No width bindings
	•	No scale transforms
	•	Stable across all screen sizes

If content grows infinitely, the class is misused.

⸻

8. Known Anti-Patterns (Hard Fail)

The following patterns are forbidden:
	•	Justified text in responsive layouts
	•	Binding padding or spacing to window size
	•	Binding width to font size
	•	Using scale transforms for responsiveness
	•	Allowing labels or text nodes to define container width
	•	Mixing linear layout logic with non-linear scaling math

If detected → remove immediately.

⸻

9. Definition of “Done”

A UI change is correct only if:
	•	No container grows without explicit max width
	•	Text wrapping does not increase container width
	•	Window resizing causes no jitter
	•	UI remains readable from small laptops to large monitors

⸻

10. Final Rule

Unexpected growth = bug, not styling issue.
Fix the layout, not the symptom.

⸻

GUI STRATEGY — EFFECTIVE 2026

Decision

The JavaFX / HBox / VBox approach is officially abandoned.

Reasons
	•	Instability on resize
	•	Poor maintainability
	•	Not future-proof
	•	Non-component-based

⸻

New Standard Architecture

Frontend
	•	React + TypeScript
	•	TailwindCSS (utility-first)
	•	ShadCN/UI for tested components
	•	Strict component-based architecture

Each Card, Chart, News-Ticker, Input, etc.:
	•	isolated
	•	reusable
	•	independently testable

⸻

Backend
	•	JSON API (REST or WebSocket)
	•	Provides:
	•	charts
	•	sector news
	•	metrics
	•	AI reports
	•	Fully decoupled from frontend

⸻

Desktop Integration (Optional)
	•	Tauri (preferred) or Electron
	•	Native menus
	•	File system access
	•	Auto-updates

⸻

Design Principles
	•	Responsive by default
	•	No pixel micromanagement
	•	Backend changes propagate automatically
	•	Centralized theme & styling
	•	SaaS-grade professional UI

⸻

LLM COMPLIANCE RULES — GUI BUILD
	•	JavaFX layout must not be reused
	•	GUI must be rebuilt from scratch
	•	React + Tailwind + ShadCN only
	•	Backend remains unchanged
	•	Focus:
	•	stability
	•	maintainability
	•	scalability
	•	future-proof design

⸻

GUI LAYOUT — VISUAL SCHEMA

┌───────────────────────────────────────────────┐
│                 Top-Bar                       │
│ ┌────────┐ ┌─────────┐ ┌─────────┐ ┌───────┐ │
│ │Ticker  │ │Sector   │ │Language │ │Action │ │
│ │Input   │ │Dropdown │ │Dropdown │ │Buttons│ │
│ └────────┘ └─────────┘ └─────────┘ └───────┘ │
└───────────────────────────────────────────────┘

┌───────────────────────────────┬───────────────────────────────┐
│         Market Overview       │         Event Monitor         │
│ ┌─────────────────────────┐  │ ┌─────────────────────────┐  │
│ │ Executive Summary       │  │ │ Price Chart             │  │
│ │ - Key Metrics           │  │ │ - LineChart (responsive)│  │
│ │ - Summary Text          │  │ │ - Period Selector       │  │
│ └─────────────────────────┘  │ │ - Chart Footer (Date)    │  │
│ ┌─────────────────────────┐  │ └─────────────────────────┘  │
│ │ Quality & Valuation     │  │ ┌─────────────────────────┐  │
│ │ Metrics (Rows)          │  │ │ Sector News Ticker       │  │
│ └─────────────────────────┘  │ │ - Scrollable Headlines   │ │
└───────────────────────────────┴───────────────────────────────┘

┌───────────────────────────────────────────────┐
│                 Status-Bar                    │
│ ┌───────────────┐             ┌─────────────┐ │
│ │Status Message │             │Version Info │ │
│ └───────────────┘             └─────────────┘ │
└───────────────────────────────────────────────┘


⸻

Component Structure / Folder Hierarchy

/frontend
  /components
    TopBar.tsx
    Dashboard/
      MarketOverviewCard.tsx
      EventMonitorCard.tsx
    StatusBar.tsx
  /layouts
    MainLayout.tsx
  /services
    ApiService.ts
  /utils
    formatters.ts


⸻

Props / State Conventions
	•	Components receive only required data
	•	No global DOM access
	•	Charts, metrics, news via props/state/context

⸻

Testing & Tooling
	•	Component tests for Cards, TopBar, StatusBar
	•	Optional Storybook
	•	CI: render-level regression tests

⸻

Performance & Theme
	•	Charts: Canvas or SVG
	•	News-Ticker: CSS animation only
	•	Flexbox + Tailwind (no width bindings)
	•	Centralized Tailwind theme (tailwind.config.js)

---

