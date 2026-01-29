# Changelog

All notable changes to this project are documented in this file.

## [Unreleased] - Phase B: Data Persistence
### Added
- **Persistence Layer:** SQLite database integration via SQLModel in Backend `ai_service`.
- **Backend API:** New endpoints for Portfolio Management (`/portfolio`).
### Changed
- **Docs:** Aligned README repository structure and backend status with current project layout.

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
