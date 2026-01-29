# Contributing to Stock News Pro

> **For AI Agents:**  
> STOP. Read `DESIGN.md` explicitly before generating any code.  
> `DESIGN.md` contains the rigid, normative rules for this project.  
> Do not infer architecture. Do not hallucinate patterns. Follow the rules defined there.

---

## 1. The Golden Rule

**DESIGN.md is the Constitution.**

All code, all refactoring, and all new features must comply with the requirements in `DESIGN.md`.  
If you find a conflict between "best practices" and `DESIGN.md`, **`DESIGN.md` wins**.

## 2. Repository Structure

This project follows a strict strict directory layout to maintain separation of concerns:

- **`/frontend`**: The User Interface.
  - *Rule:* Only presentation logic. No heavy business calculations.
  - *Tech:* React, TypeScript, Tailwind.
- **`/ai_service`**: The Backend (currently Mock/Python).
  - *Rule:* Data aggregation, LLM orchestration.
  - *Tech:* Python (FastAPI/Uvicorn).
- **`/docs`**: Project documentation and release checklists.
- **`/shared`**: (Optional) Contract definitions shared via IPC/JSON.

## 3. Workflow for Changes

1. **Check Requirements:**
   - Is this change covered by `LASTENHEFT.md`?
   - Does it violate any `DESIGN.md` constraints?

2. **Update Documentation:**
   - **`CHANGELOG.md`**: Log your specific changes under "Unreleased" or current version. (Rule `DES-GOV-48`)
   - **`LASTENHEFT.md`**: Update requirements if functionality changes.

3. **Branching:**
   - Use descriptive names: `feat/new-chart`, `fix/ticker-resolution`, `docs/update-readme`.

4. **Commit Messages:**
   - Use [Conventional Commits](https://www.conventionalcommits.org/).
   - Format: `type(scope): description`
   - Example: `feat(ui): add volume chart component`
   - Example: `chore(spec): update nfr requirements`

## 4. Instructions for AI Coding Assistants

If you are an AI agent working on this repo:

1. **Context Loading:** Always load `DESIGN.md` and `LASTENHEFT.md` into your context first.
2. **Atomic Changes:** Do not refactor unrelated files "while you are at it". Stick to the user's prompt.
3. **No Hallucinations:** If a file or function is not present, ask before creating it. Do not invent new architectural layers (e.g., "Redux") if they are not specified in `DESIGN.md`.
4. **Mocking:** If adding a new data feature, implement it as a **Mock** first (see `DES-GOV-17`).
5. **Remote Verification:** A project conclusion or task completion is only considered "clean" if `git push` has been successfully executed AND verified. Verification **MUST include both technical parity check** (git status/hash) **AND visual content confirmation** (via Browser/Server-View) to ensure files are actually present and correct on the remote. Local commits are insufficient.

## 5. Release Process

See `docs/RELEASE_CHECKLIST.md` for the exact steps to cut a new version.
