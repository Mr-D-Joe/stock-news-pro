# DESIGN.md — Project Constitution  
# Stock News Pro

⚠️ **THIS DOCUMENT IS NORMATIVE AND IMMUTABLE**

This file is the **single source of truth** for:

- Architecture  
- Frontend design  
- Backend design  
- API contracts  
- Data flow  
- Code rules  
- Security rules  
- External API usage rules  
- LLM integration rules  
- Token usage governance  
- Testing and quality standards  
- Build and release governance  
- Documentation hierarchy  

It overrides and supersedes:

- README.md  
- SYSTEM_REPORT.md  
- any other markdown or documentation  
- any LLM-generated analysis, refactorings or suggestions  
- all historical design decisions  

No other document may define rules, constraints, or architectural authority.

---

## GOVERNANCE PRINCIPLE

DESIGN.md is the project constitution.  
SYSTEM_REPORT.md is an audit report.  
README.md is orientation documentation.

No other document may introduce binding rules.

---

## DOCUMENT PRIORITY ORDER

1. DESIGN.md — binding law  
2. SYSTEM_REPORT.md — descriptive audit only  
3. README.md — informational only  
4. Code comments — non-authoritative  

---

## LLM COMPLIANCE RULES (NON-NEGOTIABLE)

All LLMs MUST:

- Read this document fully before responding.  
- Follow every rule exactly.  
- Treat all rules as binding law.  
- Explicitly report missing requirements instead of inventing them.  
- Provide a short **Reasoning block** before generating any code explaining alignment with this document.

All LLMs MUST NOT:

- Modify this document.  
- Reformat this document.  
- Summarize this document.  
- Reinterpret rules.  
- Introduce alternative architectures.  
- Invent APIs, types, or parameters.  
- Override any rule.

Violation of this document constitutes a hard failure.

---

# ARCHITECTURE CONSTITUTION

## Core Architecture Model

The system follows strict separation:

- Frontend: React + TypeScript  
- Backend: JSON API  
- Desktop Shell: Tauri  
- Data Flow: Unidirectional  
- Rendering: Component-based  
- State: Explicit and controlled  

Frontend and backend are fully decoupled.  
Neither side may assume internals of the other.

---

# FRONTEND RULES

Frontend stack:

- React  
- TypeScript  
- TailwindCSS  
- ShadCN/UI  
- Vite  
- Tauri shell  

Frontend MUST:

- Be component-based.  
- Use props/state/context only.  
- Avoid direct DOM manipulation.  
- Avoid global mutable state.  
- Avoid layout calculations in JS.  
- Avoid JS-based width calculations for layout.  
- Use CSS `aspect-ratio` or Container Queries for dynamic sizing.  

State management:

- Server-state MUST be managed via **TanStack Query**.  
- Local UI state MUST stay in the smallest possible component scope.  

Data fetching:

- MUST be handled via custom hooks.  
- UI components MUST NEVER perform raw fetch or business logic.  

Styling:

- Styling MUST use Tailwind utility classes exclusively.  
- No CSS-in-JS.  

Components MUST:

- Have single responsibility.  
- Be independently testable.  
- Receive only required data.  
- Never fetch data directly.  

---

# BACKEND RULES

Backend MUST:

- Expose JSON APIs only.  
- Never expose UI logic.  
- Never depend on frontend implementation.  
- Be replaceable without frontend rewrite.  
- Return explicit error states.  

Backend MUST NOT:

- Return silent fallback data.  
- Return generated data without marking it.  
- Encode errors as successful responses.

---

# API CONTRACT RULES

All APIs MUST:

- Be versioned.  
- Be typed.  
- Return structured JSON.  
- Return explicit error objects.  
- Never return ambiguous success states.  

Frontend MUST:

- Treat APIs as unreliable.  
- Handle latency.  
- Handle errors.  
- Handle partial results.  

---

# DATA FLOW RULES

Data flow is strictly unidirectional:

User Input → State Update → API Call → Result → UI Render  

No reverse coupling.  
No UI mutation from services.  
No state mutation from components.

The Tauri backend is the Single Source of Truth for:

- File system access  
- Local cache persistence  
- System-level data  

---

# TAURI IPC RULES

All Tauri commands MUST:

- Be strictly typed on both sides.  
- Use Rust structs and matching TypeScript interfaces.  
- Never use `any` in IPC boundaries.  

All Tauri commands MUST:

- Be wrapped in a typed service layer.  
- Never be invoked directly inside React components.  

Direct `invoke()` calls inside components are forbidden.

---

# LLM INTEGRATION RULES

LLMs are external, unreliable, non-deterministic services.

LLM outputs MUST:

- Be labeled as generated.  
- Never overwrite verified data.  
- Never silently replace API data.  

LLM hallucinations MUST NOT be masked.

If data is missing, the LLM MUST report the gap.

---

# TOKEN USAGE GOVERNANCE

LLM tokens are a controlled enterprise resource.

The system MUST:

- Minimize LLM calls.  
- Cache LLM results.  
- Deduplicate identical prompts.  
- Avoid LLM calls for UI-only actions.  
- Never call LLM for formatting or layout tasks.  
- Never call LLM redundantly for identical context.  

The system MUST:

- Track token usage.  
- Log token consumption.  
- Support future token budgeting.

LLMs MUST NOT be used where deterministic code can solve the task.

---

# MOCK ENVIRONMENT RULES

Mocks exist only for:

- UI development  
- Demo  
- Offline testing  

Mocks MUST:

- Be clearly labeled.  
- Be replaceable by real APIs.  
- Never leak into production paths.

---

# EXTERNAL API USAGE RULES

External APIs MUST:

- Be rate-limited.  
- Be cached.  
- Be abstracted behind service layers.  
- Never be called from UI components.  

API keys MUST:

- Never be hardcoded.  
- Never be committed.  
- Be injected via environment variables.  

---

# SECURITY RULES

The system MUST:

- Never expose secrets.  
- Never trust frontend input.  
- Never assume API correctness.  
- Never execute remote code.  

All rendered data MUST be sanitized.

---

# CODE QUALITY RULES

All code MUST:

- Be readable.  
- Be typed.  
- Avoid implicit any.  
- Avoid side effects.  
- Avoid magic numbers.  
- Avoid hidden coupling.  

Functions MUST:

- Have single responsibility.  
- Be testable.  
- Be deterministic when possible.  

---

# DEPENDENCY GOVERNANCE

Dependencies MUST:

- Be minimal.  
- Be justified.  
- Be reviewed before addition.  
- Be replaceable.  

No dependency may become architecturally critical without explicit approval.

---

# VERSIONING RULES

APIs MUST:

- Use semantic versioning.  
- Maintain backward compatibility where possible.  
- Document breaking changes.

---

# ERROR HANDLING RULES

Errors MUST:

- Be explicit.  
- Be typed.  
- Be user-visible when relevant.  
- Never be swallowed silently.

---

# LOGGING & OBSERVABILITY

The system MUST:

- Log errors.  
- Log API failures.  
- Log LLM failures.  
- Support future observability integration.

---

# BUILD & CI GOVERNANCE

Builds MUST:

- Be reproducible.  
- Be deterministic.  
- Fail on lint or type errors.

---

# RELEASE GOVERNANCE

Releases MUST:

- Be versioned.  
- Be documented.  
- Be traceable to commits.

---

# TESTING RULES

Testing is mandatory.

Minimum:

- UI component tests (Vitest).  
- API service tests.  
- Contract tests for IPC bridge.

---

# PERFORMANCE RULES

Frontend MUST:

- Avoid unnecessary re-renders.  
- Memoize heavy computations.  
- Avoid DOM overdraw.

Charts MUST:

- Never drive layout size.

---

# RESPONSIVE DESIGN RULES

Responsive behavior MUST:

- Be CSS-based.  
- Use Flexbox/Grid.  
- Never use scale transforms.  
- Never bind widths.

---

# LEGACY JAVAFX RULES

JavaFX UI is deprecated.

JavaFX code MUST NOT be reintroduced.

---

# DOCUMENTATION GOVERNANCE

DESIGN.md is law.  
SYSTEM_REPORT.md is audit.  
README.md is orientation.

No rule duplication allowed.  
No contradictions allowed.

---

# CHANGE GOVERNANCE

Any change to DESIGN.md:

- Must be explicit.  
- Must be intentional.  
- Must be reviewed.  
- Must be documented in commit history.

---

# FINAL CONSTITUTION RULE

If any part of the system violates this document, the system is wrong — not the document.

Fix the system, not the constitution.

---

END OF DESIGN.md
