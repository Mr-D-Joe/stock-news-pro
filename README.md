# Stock News Pro  

Stock News Pro is an enterprise-grade financial analysis platform focused on long-term maintainability, architectural clarity, and controlled AI integration.  
The project is designed as a desktop-first application with strict governance to prevent code drift, uncontrolled AI behavior, and architectural erosion.

The repository serves as a foundation for evolving a mock-driven prototype into a production-grade financial analytics system.

---

> [!IMPORTANT]  
> **SPECIFICATION GOVERNANCE: ACTIVE**  
> This project is governed by strict compliance rules.  
> 📜 **Constitution:** [`DESIGN.md`](./DESIGN.md)  
> 📋 **Requirements:** [`LASTENHEFT.md`](./LASTENHEFT.md)  
> 🤝 **Contributing:** [`CONTRIBUTING.md`](./CONTRIBUTING.md)  
>
> 🤖 **AI Agents:** You MUST read `CONTRIBUTING.md` before generating code.

--- 

## Project Purpose

Stock News Pro provides:

- Stock and sector analysis
- News aggregation and sentiment signals
- AI-assisted report generation
- Local-first desktop experience
- Architecture validation for future production systems

--- 

## Governance Model

This repository is governed by three documents:

| Document | Role |
|--------|------|
| DESIGN.md | Binding project constitution |
| SYSTEM_REPORT.md | Descriptive system audit |
| README.md | Orientation and navigation only |

DESIGN.md is the single source of architectural truth.  
SYSTEM_REPORT.md is non-normative and may be regenerated at any time.  
README.md contains no binding rules and introduces no architectural authority.

---

## Current Architecture

The system follows a strict separation of concerns.

### Frontend

Technologies:

- React
- TypeScript
- TailwindCSS
- ShadCN/UI
- Vite
- Tauri desktop shell

Responsibilities:

- UI rendering
- User interaction
- State presentation
- No business logic
- No API logic

---

### Backend (Planned)

Characteristics:

- JSON API
- Fully decoupled from frontend
- Language-agnostic
- Replaceable

Responsibilities:

- Data aggregation
- Business logic
- Persistence
- API contract enforcement

---

### AI Integration

Characteristics:

- Currently mock-driven
- Designed for controlled LLM integration
- Governed by token usage and reliability rules defined in DESIGN.md

Responsibilities:

- Report generation
- Text analysis
- Enrichment services

---

### Desktop Shell

Technology:

- Tauri

Responsibilities:

- Native window management
- File system access
- Persistence
- IPC communication
- No UI logic

---

## Repository Structure

```text
/frontend        React frontend application
/ai_service      Mock and future AI service layer
/engine          Legacy engine (deprecated)
/shared          Shared schemas or contracts

Legacy JavaFX and C++ components are deprecated and kept only for historical reference.

⸻

## Development Philosophy

This project follows:

- Strict architectural separation
- Governance-first development
- LLM discipline and token control
- Auditability
- Deterministic behavior over convenience

All architectural and behavioral rules are defined in DESIGN.md.

⸻ 

## Development Setup

### Frontend

cd frontend
npm install
npm run dev

### AI Service (Mock / Optional)

The current frontend prototype runs in standalone mode using an internal MockApiService.
No external backend service is required for UI development.

The Python AI service is provided for future backend integration and experimentation.

cd ai_service 
pip install -r requirements.txt 
uvicorn main:app --reload 

### Real Mode (Ticker Resolution)

To enable real ticker resolution via Yahoo Finance API:

1. Create `frontend/.env`:
```
VITE_USE_REAL_API=true
```

2. Rate limits apply automatically:
   - Yahoo: 5 req/s, 500/day
   - Results are cached (30 day TTL)

3. The UI will show "LIVE API" indicator when Real Mode is active.

Note: Mock mode uses local aliases and is suitable for UI development.

## Contribution Policy

All contributions must comply with:
	•	DESIGN.md
	•	Architectural separation principles
	•	Typed interfaces
	•	No hidden coupling

Pull requests violating DESIGN.md will be rejected.

⸻

## Project Status

Current stage:
	•	High-fidelity prototype
	•	Mock-driven
	•	Architecture-ready
	•	Not production-ready

⸻

## License

License information will be defined at a later stage.

⸻

## Final Note 

This repository is intentionally governed more strictly than typical projects.

This is by design to support:
	•	AI-assisted development
	•	Enterprise auditability
	•	Long-term maintainability
	•	Architectural integrity

