# Release Checklist

**Target Audience:** Release Managers & Automation Agents  
**Scope:** Creating a new versioned release (e.g., `v1.3`).

---

## 1. Pre-Flight Check

- [ ] **Clean Working Tree:** `git status` must show no uncommitted changes.
- [ ] **Tests:** All local tests must pass.
- [ ] **Linting:** Code must adhere to `STYLEGUIDE.md`.

## 2. Specification Governance

- [ ] **Scan `Lastenheft.md`:** Does it contain *only* functional requirements?
- [ ] **Scan `DESIGN.md`:** Are governance/architecture changes reflected here?
- [ ] **Check Consistency:** Do requirement IDs match implementations?

## 3. Documentation Update

- [ ] **Update `CHANGELOG.md`:**
  - Add new version header `## [vX.Y] - YYYY-MM-DD`.
  - Categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`.
- [ ] **Update Version Numbers:** Check `package.json`, `tauri.conf.json`, and `LASTENHEFT.md` header.

## 4. Git Operations

1. **Commit Release:**
   ```bash
   git add .
   git commit -m "chore(release): prepare release vX.Y"
   ```

2. **Tagging:**
   ```bash
   git tag -a vX.Y -m "Release vX.Y - [Short Summary]"
   ```

3. **Push:**
   ```bash
   git push origin main vX.Y
   ```

## 5. GitHub Release

- [ ] Go to GitHub UI -> Releases -> Draft a new release.
- [ ] Select tag `vX.Y`.
- [ ] Paste `CHANGELOG.md` content for this version into the description.
- [ ] Publish.

---

**Confidentiality:** This process ensures auditability. Do not skip steps.
