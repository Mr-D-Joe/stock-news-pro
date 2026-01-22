# LASTENHEFT — Stock News Pro
## Requirements Specification Document

**Version:** 1.0  
**Datum:** 2026-01-22  
**Status:** Draft  

---

## 1. Projektübersicht

### 1.1 Projektname
Stock News Pro — AI-powered Financial Intelligence Dashboard

### 1.2 Projektziel
Entwicklung einer Desktop-Anwendung zur KI-gestützten Analyse von Aktien und Sektoren mit automatisierter Nachrichtenverarbeitung und Berichtserstellung.

### 1.3 Zielgruppe
- Privatanleger
- Finanzanalysten
- Investment-Berater

---

## 2. Funktionale Anforderungen

### 2.1 Benutzeroberfläche (Frontend)

| ID | Anforderung | Priorität | Status |
|----|-------------|-----------|--------|
| F-UI-01 | Dashboard mit Marktübersicht, Charts und AI-Analysen | MUSS | ✅ Implementiert |
| F-UI-02 | Ticker-Eingabefeld mit Fuzzy-Suche (Google-ähnlich) | MUSS | ⚠️ Defekt |
| F-UI-03 | Sektor-Eingabefeld mit Auto-Vervollständigung | MUSS | ⚠️ Überprüfen |
| F-UI-04 | Sprach-Auswahl (DE, EN, TR, FR) | MUSS | ✅ Implementiert |
| F-UI-05 | Zeitraum-Slider (24H bis ALL) | MUSS | ✅ Implementiert |
| F-UI-06 | News-Ticker (Sektor + Aktie) | MUSS | ✅ Implementiert |
| F-UI-07 | Executive Summary Card | MUSS | ✅ Implementiert |
| F-UI-08 | Preis-Chart mit Recharts | MUSS | ✅ Implementiert |
| F-UI-09 | AI-Essay Ausgabe | MUSS | ✅ Implementiert |
| F-UI-10 | Analyse-Scope (Stock/Sector/Market/Combined) | SOLL | ✅ Implementiert |
| F-UI-11 | **Volumen-Chart (48h, stündlich)** | SOLL | ❌ Neu |

#### 2.1.1 Volumen-Chart Spezifikation

| Aspekt | Spezifikation |
|--------|---------------|
| **Zeitraum** | Letzte 48 Stunden |
| **Granularität** | 1 Stunde (Standard), optional 15-min Drill-down |
| **Darstellung** | Area-Chart oder Bar-Chart |
| **Datenpunkte** | 48 (stündlich) / 192 (15-min) |
| **Position** | Unterhalb Preis-Chart oder als separater Tab |

```
Volumen-Chart (48h)
│
│    ██
│   ████  ██
│  ██████████     ██
│ ████████████   ████  ██
├─────────────────────────────
  12:00   18:00   00:00   06:00   12:00
   (gestern)              (heute)
```

#### 2.1.2 Quality & Valuation Metrics Card (Buffett/Lynch Style)

Diese Komponente zeigt fundamentale Bewertungs- und Qualitätsmetriken im Stil von Warren Buffett und Peter Lynch.

##### Bewertungs-Metriken (Valuation)

| ID | Metrik | Beschreibung | Formel/Quelle | Status |
|----|--------|--------------|---------------|--------|
| F-UI-VAL-01 | **P/E Ratio** | Kurs-Gewinn-Verhältnis | Preis / EPS | ⚠️ Zeigt "None" |
| F-UI-VAL-02 | **PEG Ratio** | Wachstumskorrektes P/E | P/E / Gewinnwachstum | ⚠️ Zeigt "N/A" |

##### Qualitäts-Metriken (Quality)

| ID | Metrik | Beschreibung | Interpretation | Status |
|----|--------|--------------|----------------|--------|
| F-UI-QUA-01 | **ROE** | Return on Equity | >15% = gut (Buffett) | ⚠️ Zeigt "N/A" |
| F-UI-QUA-02 | **Debt/Equity** | Verschuldungsgrad | <0.5 = konservativ | ⚠️ Zeigt "N/A" |

##### Analysten-Ratings

| ID | Metrik | Anzeige | Farbkodierung | Status |
|----|--------|---------|---------------|--------|
| F-UI-ANA-01 | **Target Mean** | $XXX.XX | Neutral (Schwarz) | ✅ Funktional |
| F-UI-ANA-02 | **Target High** | $XXX.XX | Grün (Upside) | ✅ Funktional |
| F-UI-ANA-03 | **Target Low** | $XXX.XX | Rot (Downside) | ✅ Funktional |
| F-UI-ANA-04 | **Recommendation** | BUY/HOLD/SELL | N/A bei fehlend | ⚠️ Zeigt "N/A" |

##### UI-Spezifikation

```
┌─────────────────────────────────────────────────────────────┐
│ 💎 Quality & Valuation Metrics (Buffett/Lynch Style)        │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ VALUATION:   │  │ GROWTH:      │  │ QUALITY:     │       │
│  │ P/E RATIO    │  │ PEG RATIO    │  │ ROE          │       │
│  │   [Value]    │  │   [Value]    │  │   [Value]    │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│  ┌──────────────┐                                           │
│  │ HEALTH:      │                                           │
│  │ DEBT/EQUITY  │                                           │
│  │   [Value]    │                                           │
│  └──────────────┘                                           │
├─────────────────────────────────────────────────────────────┤
│  ANALYST TARGET     ANALYST HIGH      ANALYST LOW           │
│     (MEAN)                                                  │
│    $321.55          $390.00           $190.00               │
│                     (grün)            (rot)                 │
│                                                             │
│  RECOMMENDATION: [BUY/HOLD/SELL/N/A]                        │
└─────────────────────────────────────────────────────────────┘
```

##### Buffett/Lynch Bewertungskriterien

| Metrik | Gut | Neutral | Schlecht |
|--------|-----|---------|----------|
| P/E Ratio | <15 | 15-25 | >25 |
| PEG Ratio | <1.0 | 1.0-2.0 | >2.0 |
| ROE | >15% | 10-15% | <10% |
| Debt/Equity | <0.5 | 0.5-1.0 | >1.0 |


### 2.2 Backend (AI Service)

| ID | Anforderung | Priorität | Status |
|----|-------------|-----------|--------|
| F-BE-01 | Ticker Resolution via Fuzzy-Match | MUSS | ✅ Implementiert |
| F-BE-02 | Fundamentaldaten-Abruf (P/E, ROE, etc.) | MUSS | ✅ Implementiert |
| F-BE-03 | Historische Preisdaten (10 Jahre) | MUSS | ✅ Implementiert |
| F-BE-04 | Nachrichten-Aggregation (RSS, APIs) | MUSS | ⚠️ Mock |
| F-BE-05 | AI-Analyse mit Essay-Generierung | MUSS | ✅ Implementiert |
| F-BE-06 | Mehrsprachige Ausgabe | MUSS | ✅ Implementiert |
| F-BE-07 | DEV_MODE für Mock-Daten | MUSS | ✅ Implementiert |
| F-BE-08 | Caching mit Content-Hash | MUSS | ✅ Implementiert |
| F-BE-09 | News-Timestamp (fetched_at) | MUSS | ✅ Implementiert |

### 2.3 Desktop-Integration (Tauri)

| ID | Anforderung | Priorität | Status |
|----|-------------|-----------|--------|
| F-TA-01 | Native macOS/Windows App | MUSS | ✅ Implementiert |
| F-TA-02 | Backend Auto-Start bei App-Start | MUSS | ⚠️ Pfad-Fehler |
| F-TA-03 | Backend Auto-Stop bei App-Schließen | MUSS | ✅ Implementiert |
| F-TA-04 | Typed IPC Service Layer | MUSS | ✅ Implementiert |

### 2.4 API-Governance

| ID | Anforderung | Priorität | Status |
|----|-------------|-----------|--------|
| F-AG-01 | DEV_MODE=True als Standard | MUSS | ✅ Implementiert |
| F-AG-02 | Startup-Warnung bei Real API | MUSS | ✅ Implementiert |
| F-AG-03 | AI Provider Priorität: OpenAI → Gemini | MUSS | ✅ Implementiert |
| F-AG-04 | Cache Pre-Check vor AI-Calls | MUSS | ✅ Implementiert |
| F-AG-05 | Token-Usage Tracking | SOLL | ❌ Offen |

### 2.5 Datenverarbeitung (Data Handling)

#### 2.5.1 Ticker Resolution (Real Mode)

| ID | Anforderung | Priorität | Status |
|----|-------------|-----------|--------|
| F-DH-01 | **Internet-basierte Ticker-Auflösung** via API (Yahoo Finance primary) | MUSS | ❌ Offen |
| F-DH-02 | **Tippfehler-Toleranz** via Levenshtein-Distanz (≤2 Zeichen) | MUSS | ✅ Implementiert |
| F-DH-03 | **Firmennamen → Symbol** Mapping (z.B. "Alphabet" → GOOG) | MUSS | ❌ Offen |
| F-DH-04 | **In-Flight De-duplication** (keine parallelen Requests für gleiche Query) | MUSS | ❌ Offen |

> [!IMPORTANT]
> Die Mock-Aliases (z.B. GOOGLE → ACME) dienen NUR zu Testzwecken.
> In Real Mode MUSS eine echte Ticker-Auflösung erfolgen!

#### 2.5.2 Ticker Resolution Cache

##### Cache-Typen (Zwei separate Caches)

| ID | Cache | Beschreibung | TTL |
|----|-------|--------------|-----|
| F-DH-10 | **name_to_symbol** | Normalisierte Eingabe → Symbol | 30 Tage |
| F-DH-11 | **symbol_to_name** | Symbol → Kanonischer Firmenname | 90 Tage |

##### Cache-Spezifikation

| ID | Anforderung | Spezifikation |
|----|-------------|---------------|
| F-DH-12 | **Cache-Größe** | 1000 Einträge pro Cache |
| F-DH-13 | **Eviction-Policy** | FIFO (First-In-First-Out) |
| F-DH-14 | **Persistence** | Tauri Filesystem (primary), localStorage (warm-start only) |
| F-DH-15 | **Negative Caching** | NOT_FOUND Ergebnisse für 24h cachen |

##### Cache-Entry Struktur

```typescript
interface TickerCacheEntry {
  query_normalized: string;   // "ALPHABET"
  symbol: string;             // "GOOG"
  name: string;               // "Alphabet Inc."
  sector: string;             // "Technology"
  confidence: number;         // 0.0 - 1.0
  source: 'FMP' | 'Yahoo';    // Provider
  timestamp: string;          // ISO8601
  expiresAt: string;          // ISO8601
}
```

##### Cache-Workflow

```
User Input: "alphabet"
     ↓
[Normalize] → "ALPHABET"
     ↓
[Cache Lookup] ───→ Hit + Valid? → Return cached result
     ↓ Miss or Expired
[In-Flight Check] ───→ Pending? → Wait for existing request
     ↓ No pending
[Rate Limit Check] ───→ Exceeded? → Return RATE_LIMIT error
     ↓ OK
[API Resolution] → Yahoo → "GOOG", "Technology", "Alphabet Inc."
     ↓
[Cache Write] → Store result, evict oldest if full (FIFO)
     ↓
Return result
```

#### 2.5.3 Rate Limit & Backoff Policy

| ID | Anforderung | Spezifikation |
|----|-------------|---------------|
| F-DH-20 | **Rate Limiter Typ** | Token Bucket (per Provider) |
| F-DH-21 | **Yahoo Limit** | 5 requests/second, 500/day |
| F-DH-22 | **FMP Limit** | 250 requests/day (Free Tier) |
| F-DH-23 | **Hard-Stop** | Bei Limit erreicht → RATE_LIMIT Error, kein Retry |
| F-DH-24 | **Backoff** | Exponential mit Jitter, max 5 Retries, max 60s |
| F-DH-25 | **In-Flight De-dupe** | Gleiche normalisierte Query → nur 1 Request |

##### Backoff-Strategie

```
Retry 1: 1s + random(0-500ms)
Retry 2: 2s + random(0-500ms)
Retry 3: 4s + random(0-500ms)
Retry 4: 8s + random(0-500ms)
Retry 5: 16s + random(0-500ms)
→ Nach 5 Retries: PROVIDER_DOWN Error
```

> [!CAUTION]
> Retry-Storms sind verboten. Hard-Stop bei Rate Limit.

#### 2.5.4 Error Semantics & UI Signals

| Error Code | Beschreibung | UI Behavior |
|------------|--------------|-------------|
| `NOT_FOUND` | Ticker/Firma nicht gefunden | "Kein Ergebnis für [input]" + Vorschläge |
| `RATE_LIMIT` | API-Limit erreicht | "Bitte später versuchen" + Cache-Only Mode |
| `PROVIDER_DOWN` | Provider nicht erreichbar | "Service nicht verfügbar" + Cache verwenden |
| `LOW_CONFIDENCE` | Confidence < 0.85 | Kandidatenliste anzeigen, User-Bestätigung |
| `AMBIGUOUS` | Mehrere gleich gute Matches | Dropdown zur Auswahl |

##### Error-Handling Regeln (DESIGN.md L343-346)

| Regel | Anforderung |
|-------|-------------|
| Explizit | Errors MÜSSEN explizit sein |
| Typed | Errors MÜSSEN typed sein |
| Visible | Errors MÜSSEN user-sichtbar sein wenn relevant |
| No Swallow | Errors DÜRFEN NICHT silent verschluckt werden |

> [!WARNING]
> Fallback DARF NIEMALS Symbol erfinden. Bei Unsicherheit: User fragen!

#### 2.5.5 Provider Strategy & Switching Rules

##### Provider Hierarchie

| Priority | Provider | Typ | Status |
|----------|----------|-----|--------|
| 1 | **Yahoo Finance** | Primary | ❌ Zu implementieren |
| 2 | **FMP** | Optional Premium | ❌ Später (wenn Free Tier viabel) |

##### Switching Logic

```
[Request] 
     ↓
[Yahoo Available?] ───→ Yes → Use Yahoo
     ↓ No (RATE_LIMIT / DOWN)
[Cache Available?] ───→ Yes → Return Cache (stale)
     ↓ No
[FMP Enabled & Key?] ───→ Yes → Try FMP
     ↓ No
Return PROVIDER_DOWN Error
```

##### Provider Interface (per DESIGN.md L273)

```typescript
interface TickerProvider {
  name: 'Yahoo' | 'FMP';
  search(query: string): Promise<ProviderResult>;
  isAvailable(): boolean;
  getRemainingQuota(): number;
}
```

#### 2.5.6 Mock vs Real Mode Unterscheidung

| Modus | Ticker-Auflösung | Cache | Rate Limit |
|-------|------------------|-------|------------|
| **DEV_MODE=true** | Lokale Alias-Map | In-Memory | Kein Limit |
| **DEV_MODE=false** | Yahoo API (+ FMP optional) | Tauri FS | Enforced |

---

## 3. Nicht-Funktionale Anforderungen

### 3.1 Architektur

| ID | Anforderung | Quelle |
|----|-------------|--------|
| NF-AR-01 | Frontend: React + TypeScript + TailwindCSS | DESIGN.md |
| NF-AR-02 | Backend: FastAPI (Python) | DESIGN.md |
| NF-AR-03 | Desktop: Tauri (Rust) | DESIGN.md |
| NF-AR-04 | Server-State via TanStack Query | DESIGN.md L118 |
| NF-AR-05 | Data Fetching via Custom Hooks | DESIGN.md L123 |
| NF-AR-06 | Typed Tauri IPC Commands | DESIGN.md L205-208 |

### 3.2 Sicherheit

| ID | Anforderung | Quelle |
|----|-------------|--------|
| NF-SE-01 | Keine Secrets im Code | DESIGN.md |
| NF-SE-02 | Frontend Input nie vertrauen | DESIGN.md |
| NF-SE-03 | Alle gerenderten Daten sanitizen | DESIGN.md |
| NF-SE-04 | .env Dateien in .gitignore | User |

### 3.3 Governance

| ID | Anforderung | Quelle |
|----|-------------|--------|
| NF-GO-01 | DESIGN.md ist einzige Architektur-Autorität | DESIGN.md |
| NF-GO-02 | LLMs müssen DESIGN.md befolgen | DESIGN.md |
| NF-GO-03 | Keine Silent Fallback Responses | DESIGN.md L152 |
| NF-GO-04 | LLM-Output muss als generiert markiert sein | DESIGN.md L218 |

---

## 4. Bekannte Defekte (Bugs)

| ID | Beschreibung | Priorität | Ursache |
|----|--------------|-----------|---------|
| BUG-01 | Backend-Pfad in Sidecar falsch (`../ai_service` existiert nicht) | KRITISCH | Relativer Pfad falsch |
| BUG-02 | Ticker-Suche befüllt Felder nicht mehr | KRITISCH | Legacy-Layer unvollständig |
| BUG-03 | runAnalysis/resolveStockInput sind Stubs | HOCH | TanStack Migration unvollständig |
| BUG-04 | Mock Fallback generiert Fake-Daten | MITTEL | DESIGN.md Verstoß |

---

## 5. Offene Aufgaben

### 5.1 Phase 3 (Ausstehend)
- [ ] MockApiService Silent Fallback entfernen
- [ ] Explizite Fehlermeldung bei unbekannten Tickern

### 5.2 Backend-Pfad Fix
- [ ] Absoluten Pfad in lib.rs verwenden
- [ ] Oder: Python-Venv korrekt aktivieren

### 5.3 Frontend-Backend Integration
- [ ] Ticker-Suche mit TanStack Query verbinden
- [ ] Legacy-Layer vollständig implementieren oder entfernen
- [ ] Analyse-Funktion mit Mutation Hook verbinden

---

## 6. Technologie-Stack

| Komponente | Technologie | Version |
|------------|-------------|---------|
| Frontend | React | 19.x |
| Sprache | TypeScript | 5.9.x |
| Styling | TailwindCSS | 3.4.x |
| UI-Library | ShadCN/UI | - |
| Charts | Recharts | 3.6.x |
| State | TanStack Query | 5.x |
| Desktop | Tauri | 2.x |
| Backend | FastAPI | 0.x |
| AI Provider | OpenAI, Gemini | - |
| Build | Vite | 7.3.x |

---

## 7. Dokumenten-Hierarchie

1. **DESIGN.md** — Bindende Architektur-Konstitution
2. **LASTENHEFT.md** — Anforderungsdokumentation (dieses Dokument)
3. **SYSTEM_REPORT.md** — Audit-Format Template
4. **README.md** — Orientierung/Schnellstart

---

## 8. Abnahmekriterien

| ID | Kriterium |
|----|-----------|
| AK-01 | App startet ohne Backend-Fehler |
| AK-02 | Ticker-Eingabe löst auf und befüllt Sektor |
| AK-03 | Analyse-Button generiert Report |
| AK-04 | Charts zeigen historische Daten |
| AK-05 | App-Schließen stoppt Backend-Prozess |
| AK-06 | DEV_MODE verhindert externe API-Calls |

---

**Ende des Lastenhefts**
