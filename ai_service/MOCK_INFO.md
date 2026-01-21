# Mock Environment Changes Documentation

> **Zweck:** Alle Änderungen dokumentieren, die für den DEV_MODE (Mock-Umgebung) gemacht wurden.
> Diese müssen bei Rückkehr zur Produktion **NICHT rückgängig** gemacht werden - sie sind durch `DEV_MODE=false` automatisch deaktiviert.

---

## Aktivierung

```bash
# Mock aktivieren
DEV_MODE=true

# Mock deaktivieren (Produktion)
DEV_MODE=false  # oder Variable entfernen
```

---

## Geänderte Dateien

### 1. Konfiguration

| Datei | Änderung | Zeilen |
|-------|----------|--------|
| `ai_service/config.py` | `dev_mode: bool` Field hinzugefügt | 60-61 |
| `.env` | `DEV_MODE=true` hinzugefügt | 1 |

---

### 2. Mock-Modul (NEU erstellt)

| Datei | Beschreibung |
|-------|--------------|
| `ai_service/mock/__init__.py` | Exports aller Mock-Klassen |
| `ai_service/mock/mock_data.py` | 4 Pseudo-Aktien mit vollständigen Daten |
| `ai_service/mock/mock_ai_client.py` | MockAIClient - simuliert AI-Antworten |
| `ai_service/mock/mock_fetchers.py` | MockNewsFetcher, MockHistoricAnalyzer, MockDeepCollector, MockTickerResolver |

---

### 3. Provider-Integrationen (DEV_MODE-Switch)

| Datei | Änderung | Bedingte Logik |
|-------|----------|----------------|
| `ai_service/analyzers/provider_factory.py` | Returns `MockAIClient` | `if settings.dev_mode:` |
| `ai_service/fetchers/__init__.py` | Returns `MockNewsFetcher` | `if settings.dev_mode:` |
| `ai_service/main.py` | `/resolve/ticker` nutzt `MockTickerResolver` | `if _settings.dev_mode:` |
| `ai_service/main.py` | `/resolve/sector` nutzt `MockTickerResolver` | `if _settings.dev_mode:` |
| `ai_service/main.py` | `/api/fundamentals` nutzt `MockHistoricAnalyzer` | `if _settings.dev_mode:` |
| `ai_service/pipeline/orchestrator.py` | Factory-Methoden für Mock-Provider | `if self._is_dev_mode:` |

---

### 4. GUI-Änderungen (Java/JavaFX)

| Datei | Änderung |
|-------|----------|
| `gui/.../ApiService.java` | `getFundamentals()` Methode hinzugefügt |
| `gui/.../MainViewModel.java` | Fundamentals Properties + `loadFundamentals()` |
| `gui/.../MainApp.java` | `createBoundMetricBox()` für dynamische Bindung |

---

### 5. Rate Limit Verbesserungen (NICHT mock-spezifisch)

Diese Änderungen gelten für **BEIDE** Modi (Dev + Produktion):

| Datei | Änderung |
|-------|----------|
| `ai_service/analyzers/gemini_client.py` | Jitter + Exponential Backoff |
| `ai_service/analyzers/openai_client.py` | Jitter + Exponential Backoff + Proaktive Verzögerung |
| `ai_service/analyzers/groq_client.py` | Jitter + Exponential Backoff + Proaktive Verzögerung |
| `ai_service/analyzers/perplexity_client.py` | Jitter + Exponential Backoff |
| `ai_service/analyzers/openrouter_client.py` | Jitter + Exponential Backoff |

---

## Mock-Aktien

| Ticker | Unternehmen | Sektor | Empfehlung |
|--------|-------------|--------|------------|
| `ACME` | ACME Corporation | Technology | Strong Buy |
| `BGNX` | BioGenX Inc. | Healthcare | Hold |
| `NOVA` | NovaCraft Energy | Energy | Buy |
| `FINX` | FinanceX Holdings | Financials | Strong Buy |

---

## Rückkehr zur Produktion

**Keine Code-Änderungen nötig!** Einfach:

```bash
# In .env:
DEV_MODE=false

# Oder Variable entfernen
```

Alle `if dev_mode:` Checks werden automatisch übersprungen.

---

## Changelog

| Datum | Änderung |
|-------|----------|
| 2026-01-17 | Initiale Mock-Umgebung erstellt |
| 2026-01-17 | 4 Pseudo-Aktien hinzugefügt (ACME, BGNX, NOVA, FINX) |
| 2026-01-17 | Rate Limit Best Practices implementiert (alle AI-Clients) |
| 2026-01-17 | `/resolve/ticker` für DEV_MODE gefixt |
| 2026-01-17 | SecureKeyManager Utility erstellt |
| 2026-01-17 | `/api/fundamentals` Endpoint erstellt |
| 2026-01-17 | GUI: Dynamische Fundamentals-Bindung implementiert |
