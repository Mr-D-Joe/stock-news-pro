# TECHNICAL_SPEC — Stock News Pro
## Implementation-Level Specification

Version: 1.0  
Datum: 2026-01-24  
Status: Active

---

## 1. Mock Data Strategy (Demo Mode)

### 1.1 Predefined Equity Entities
To ensure a consistent user experience in `DEV_MODE=True`, the following stocks MUST be implemented with high-fidelity mock data:

| Symbol | Name | Sector | Industry |
| :--- | :--- | :--- | :--- |
| **ACME** | ACME Corp | Technology | Software |
| **BGNX** | BioGenix | Healthcare | Biotechnology |
| **NVO** | Novo Nordisk | Healthcare | Pharmaceuticals |
| **LLY** | Eli Lilly | Healthcare | Pharmaceuticals |

### 1.2 Fallback Generator Logic
If a ticker is resolved that is NOT in the predefined list, the system MUST generate a "Safe Generic" report as specified in `DH-REQ-GENERIC`.

---

## 2. Dashboard Layout Fine-Tuning

### 2.1 Column Proportions
The 2-column layout defined in `UI-REQ-DASH-03` MUST use the following grid proportions on large screens (XL):
- **Column 1 (Market Overview):** 41.6% (`col-span-5` of 12)
- **Column 2 (Monitor & AI):** 58.3% (`col-span-7` of 12)

### 2.2 Timeframe Slicing
The `useTimeSlicing` hook MUST implement the following data points for the 4000-point mock history:
- **1Y View:** 252 trading days.
- **ALL View:** Full 4000 points.
- **24H View:** 15-minute intervals.

---

## 3. Technical Fallbacks

### 3.1 AI Service Unavailable
If the `ai_service` sidecar cannot be reached via IPC, the frontend MUST:
1. Set `error_state` to `SERVICE_UNAVAILABLE`.
2. Display a "Local AI Offline" banner in the `StatusBar`.
3. Provide a "Retry Connection" button.

### 3.2 Cache Eviction
The FIFO cache (1000 items) defined in `AG-REQ-CACHE-01` MUST be cleared if the user manually changes the `language` context, but preserved across `time_range` changes (using compound keys).

---

## 4. Referenzierte Artefakte

- **Styleguide:** Siehe `STYLEGUIDE.md` (Design-Tokens).
- **Prompts:** Siehe `PROMPTS.md` (System-Prompt Vorlagen).
