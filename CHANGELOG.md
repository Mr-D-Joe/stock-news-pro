# Changelog

All notable changes to this project are documented in this file.

## [Unreleased] - Phase B: Data Persistence
### Added
- **Persistence Layer:** SQLite database integration via SQLModel in Backend `ai_service`.
- **Backend API:** New endpoints for Portfolio Management (`/portfolio`).
- **API v1:** Versioned endpoints with status/error envelopes for engine/theme/portfolio.
- **CI Gates:** GitHub Actions workflow with frontend lint/typecheck and backend lint/typecheck/tests.
- **Sanitization Trace:** UI metadata for sanitization status/version.
### Changed
- **Heatmap:** Timeframe sync + tooltip improvements + nested top-stocks support.
- **Sparklines:** Fixed-scale comparison in watchlists and search-result sparkline integration.
- **Persistence:** SQLite path moved to OS-appropriate app data directory.
- **Docs:** Updated README, SYSTEM_REPORT, and TECHNICAL_SPEC for current architecture/tooling.
- **CI:** Backend lint scope adjusted to avoid false failures; frontend lint fixes applied.
- **CI:** Removed remaining frontend lint violations (typed guards, unused symbols, react-refresh export warning).
- **CI:** Cleared backend ruff lint violations (imports, exceptions, typevars, prompt context).
- **CI:** Fixed frontend typecheck issues (portfolio API guards, heatmap treemap typing).
- **CI:** Fixed backend mypy typecheck issues (typing cleanup, Optional fixes, import typing).
- **CI:** Removed remaining Python typing.Any usages by introducing precise contracts (TypedDicts).
- **CI:** Typed OpenRouter message payloads (removed arg-type ignore).
- **CI:** Validated DDG deep-web results (removed trust-cast).
- **CI:** Replaced ticker resolution cast with validated TypeGuard.
- **CI:** Fixed ReportData typing import in HTML reporter (ruff F821).
- **CI:** Added types-requests to dev requirements for mypy CI.
- **CI:** Fixed pytest module import path via tests conftest.
- **CI:** Exported Transaction model in ai_service.models to fix test imports.
- **CI:** Added transaction model module to resolve ai_service.models import in tests.
- **CI:** Added Playwright fallback in browser extractor to keep tests running when browsers are unavailable.
- **CI:** Added explicit task typing in browser extractor to satisfy mypy.

## [1.7.0] - 2026-01-29 - Phase A: Thematic Analysis
### Added
- **Theme Search:** Dedicated input field in TopBar for searching trends (e.g., "AI").
- **Analysis Engine:** New `/analyze/theme` endpoint providing structural Winners/Losers.
- **UI Component:** `ThematicReport.tsx` for visualizing theme ecosystems and strategic context essays.
- **Architecture:** Mutual exclusivity logic between Stock and Theme contexts.

## [1.6.0] - 2026-01-287

### Added
- Introduced Chapter 7 “Non-Functional Requirements” with atomic NFR-REQ-01 through NFR-REQ-07 aligned to DESIGN.md.

---

## [v1.3] — 2026-01-27

### Added
- Introduced Chapter 7 “Non-Functional Requirements” with atomic NFR-REQ-01 through NFR-REQ-07 aligned to DESIGN.md.

### Changed
- Lastenheft now contains functional requirements only; governance, architecture, and LLM rules fully moved to DESIGN.md.
- Standardized UI terminology (“Benutzeroberfläche”) across all frontend requirements.
- Distinguished user-controlled context values from system-controlled runtime states.
- Refined AI metadata responsibility from Backend to System.
- Harmonized wording for analysis_scope, analysis_status, error_state, data_origin, generated_flag, fetched_at, and stock_resolution_status.

### Removed
- Sections 1.4–1.7 (meta, governance, documentation artifacts) from Lastenheft; normative authority relocated to DESIGN.md.

---
