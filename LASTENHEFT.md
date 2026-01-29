# LASTENHEFT — Stock News Pro
## Requirements Specification Document

⚠️ Dieses Dokument ist normativ für funktionale Anforderungen.

Architektur-, Governance-, LLM- und Systemverhaltensregeln werden ausschließlich durch DESIGN.md definiert.

Im Konfliktfall besitzt DESIGN.md Vorrang.


Version: 1.6
Datum: 2026-01-28
Status: Draft

## Änderungshistorie

| Version | Datum       | Abschnitt | Änderungstyp | Beschreibung |
|--------:|------------|-----------|--------------|--------------|
| 1.9 | 2026-01-29 | 7 | Erweiterung | Einführung von NFRs für CI‑Reproduzierbarkeit und Test‑Determinismus (NFR-REQ-08/09). |
| 1.8 | 2026-01-29 | 3.7, 4.6 | Erweiterung | Einführung der Portfolio-Persistenz (BE-REQ-PERSIST, BE-REQ-PORTFOLIO) für Phase B. |
| 1.7 | 2026-01-29 | 2.12, 3.6 | Erweiterung | Einführung der Themen-Analyse (UI-REQ-THEMESEL, BE-REQ-THEME) für Schlagwortsuche (Phase A). |
| 1.6 | 2026-01-28 | 2.10, 4.5 | Refactoring | Entfernung des Analyse-Scope-Selectors (UI-REQ-SCOPE-xx) zur Vereinfachung sowie Einführung der Port-Isolation (BE-REQ-PORT-01) und des Dashboard Heroes (UI-REQ-HERO-01). |
| 1.5 | 2026-01-28 | 2.13, 3.7 | Erweiterung | Einführung der Sparkline-Anforderungen (UI-REQ-SPARK-01 bis -04, BE-REQ-SPARK-01 bis -02) für kompakte Trend-Visualisierungen |
| 1.4 | 2026-01-28 | 2.12, 3.6 | Erweiterung | Einführung der Sektor-Heatmap-Anforderungen (UI-REQ-HEATMAP-01 bis -09, BE-REQ-SECTOR-01 bis -04) für interaktive Treemap-Visualisierung der Marktsektoren |
| 1.3 | 2026-01-27 | 7 | Erweiterung | Einführung eines Kapitels „Nicht-funktionale Anforderungen“ mit atomaren, benutzerorientierten Qualitätsanforderungen (NFR-REQ-01 bis NFR-REQ-07) gemäß DESIGN.md |
| 1.3 | 2026-01-27 | 3.5.5 | Terminologie-Präzisierung | Präzisierung der Verantwortlichkeit für KI-Metadaten von „Backend“ auf „System“ zur Konsistenz mit Orchestrierungsarchitektur gemäß DESIGN.md |
| 1.3 | 2026-01-27 | 2.1, 2.2, 2.6–2.11 | Terminologie-Konsistenz | Vereinheitlichung der UI-Anforderungen: Ersetzung von „Das System …“ durch „Die Benutzeroberfläche …“ in UI-Requirements sowie Korrektur von Zustands-Terminologie in 2.2 zur klaren Trennung von UI- und Backend-Verantwortung gemäß DESIGN.md. |
| 1.3 | 2026-01-27 | 2.1, 2.2 | Terminologie-Präzisierung | Trennung von Nutzerkontext (Kontextwert) und systemseitigem Laufzeitstatus (Systemzustand). Umstellung von analysis_status, error_state, data_origin, generated_flag, fetched_at und stock_resolution_status auf konsistente Zustands-Terminologie gemäß DESIGN.md. |
| 1.3 | 2026-01-27 | 1.4–1.7 | Struktur-Refactoring | Entfernung der Meta-, Governance- und Spezifikationsabschnitte (1.4–1.7) aus dem Lastenheft. Normative Autorität dieser Inhalte wurde vollständig nach DESIGN.md verlagert. |
| 1.3 | 2026-01-27 | Gesamt | Governance-Abgrenzung | Ab Version 1.3 enthält das Lastenheft ausschließlich funktionale Anforderungen. Governance-, Meta- und Spezifikationsregeln werden ausschließlich in DESIGN.md geführt. |
| 1.1 | 2026-01-24 | Gesamt | Konsolidierung | Bereinigung von Inkonsistenzen in Änderungshistorie, ID-Zuordnung und Arbeitsübersicht gemäß RE-STRUCT und RE-TRACE |
| 1.1 | 2026-01-24 | 2.5–2.11 | Regelkonformität | Vereinheitlichung der UI-Formulierungen auf „Benutzeroberfläche“ sowie explizite Trennung von UI- und Backend-Verantwortung gemäß DESIGN.md |
| 1.1 | 2026-01-24 | 3.1–6.4 | Regelkonformität | Korrektur fehlerhafter Abschnittsnummerierungen (z. B. mehrfach „3.1“) in Backend-, Tauri- und Data-Handling-Anforderungen gemäß RE-STRUCT-02 |
| 1.1 | 2026-01-24 | Gesamt | Konsistenzprüfung | Vollständiger Abgleich aller funktionalen Anforderungen (2.x–6.x) mit DESIGN.md zur Sicherstellung klarer Architektur- und Verantwortungs­trennung |
| 1.1 | 2026-01-22 | 6.4 | Anforderungsauflösung | Auflösung der Sammelanforderung F-DH-04 in atomare Anforderungen zur In-Flight-De-Duplizierung |
| 1.1 | 2026-01-22 | 6.3 | Anforderungsauflösung | Auflösung der Sammelanforderung F-DH-03 in atomare Anforderungen zum Name-zu-Symbol-Mapping |
| 1.1 | 2026-01-22 | 6.2 | Anforderungsauflösung | Auflösung der Sammelanforderung F-DH-02 in atomare Anforderungen zur fehlertoleranten Auflösung |
| 1.1 | 2026-01-22 | 6.1 | Anforderungsauflösung | Auflösung der Sammelanforderung F-DH-01 in atomare Anforderungen zur internetbasierten Ticker-Auflösung |
| 1.1 | 2026-01-22 | 5.5 | Anforderungsauflösung | Auflösung der Sammelanforderung F-AG-05 in atomare Anforderungen zum Token-Usage-Tracking |
| 1.1 | 2026-01-22 | 5.4 | Anforderungsauflösung | Auflösung der Sammelanforderung F-AG-04 in atomare Anforderungen zum Cache-Pre-Check |
| 1.1 | 2026-01-22 | 5.3 | Anforderungsauflösung | Auflösung der Sammelanforderung F-AG-03 in atomare Anforderungen zur Provider-Priorisierung |
| 1.1 | 2026-01-22 | 5.2 | Anforderungsauflösung | Auflösung der Sammelanforderung F-AG-02 in atomare Anforderungen zur API-Startup-Warnung |
| 1.1 | 2026-01-22 | 5.1 | Anforderungsauflösung | Auflösung der Sammelanforderung F-AG-01 in atomare Anforderungen zum DEV_MODE |
| 1.1 | 2026-01-22 | 4.4 | Anforderungsauflösung | Auflösung der Sammelanforderung F-TA-04 in atomare Anforderungen zum typisierten IPC-Service-Layer |
| 1.1 | 2026-01-22 | 4.3 | Anforderungsauflösung | Auflösung der Sammelanforderung F-TA-03 in atomare Anforderungen zum Backend-Stopp |
| 1.1 | 2026-01-22 | 4.2 | Anforderungsauflösung | Auflösung der Sammelanforderung F-TA-02 in atomare Anforderungen zum Backend-Start |
| 1.1 | 2026-01-22 | 4.1 | Anforderungsauflösung | Auflösung der Sammelanforderung F-TA-01 in atomare Anforderungen zur nativen Desktop-Anwendung |
| 1.1 | 2026-01-22 | 3.5 | Anforderungsauflösung | Auflösung der Sammelanforderung F-BE-05 in atomare Anforderungen zur KI-Analyse |
| 1.1 | 2026-01-22 | 3.4 | Anforderungsauflösung | Auflösung der Sammelanforderung F-BE-04 in atomare Anforderungen zur Nachrichtenaggregation |
| 1.1 | 2026-01-22 | 3.3 | Anforderungsauflösung | Auflösung der Sammelanforderung F-BE-03 in atomare Anforderungen zu historischen Preisdaten |
| 1.1 | 2026-01-22 | 3.2 | Anforderungsauflösung | Auflösung der Sammelanforderung F-BE-02 in atomare Anforderungen zum Fundamentaldaten-Abruf |
| 1.1 | 2026-01-22 | 3.1 | Anforderungsauflösung | Auflösung der Sammelanforderung F-BE-01 in atomare Anforderungen zur Ticker-Auflösung |
| 1.1 | 2026-01-22 | 2 | Struktur-Refactoring | Umstellung von tabellarischen Sammelanforderungen auf abschnittsbasierte atomare Einzelanforderungen |
| 1.1 | 2026-01-22 | Gesamt | Governance-Anpassung | Entfernung von Implementierungsstatus und Systemzustand aus dem Lastenheft |
| 1.0 | 2026-01-22 | Gesamt | Initialfassung | Erste Version des Lastenhefts mit tabellarischen Sammelanforderungen |


## ID-Zuordnung – Auflösung von Sammelanforderungen (nicht normativ)

Hinweis zur Sortierung: Tabellen sind von „neu nach alt“ sortiert (höhere ursprüngliche F-IDs zuerst). Innerhalb einer Tabelle sind die neuen Requirement-IDs aufsteigend sortiert.

### Auflösung der ursprünglichen Anforderung F-BE-05

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-BE-05 | BE-REQ-AI-01 |
| F-BE-05 | BE-REQ-AI-02 |
| F-BE-05 | BE-REQ-AI-03 |
| F-BE-05 | BE-REQ-AI-04 |
| F-BE-05 | BE-REQ-AI-05 |

### Auflösung der ursprünglichen Anforderung F-BE-04

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-BE-04 | BE-REQ-NEWS-01 |
| F-BE-04 | BE-REQ-NEWS-02 |
| F-BE-04 | BE-REQ-NEWS-03 |
| F-BE-04 | BE-REQ-NEWS-04 |

### Auflösung der ursprünglichen Anforderung F-BE-03

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-BE-03 | BE-REQ-HISTORY-01 |
| F-BE-03 | BE-REQ-HISTORY-02 |
| F-BE-03 | BE-REQ-HISTORY-03 |

### Auflösung der ursprünglichen Anforderung F-BE-02

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-BE-02 | BE-REQ-FUNDAMENTAL-01 |
| F-BE-02 | BE-REQ-FUNDAMENTAL-02 |
| F-BE-02 | BE-REQ-FUNDAMENTAL-03 |
| F-BE-02 | BE-REQ-FUNDAMENTAL-04 |

### Auflösung der ursprünglichen Anforderung F-BE-01

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-BE-01 | BE-REQ-RESOLUTION-01 |
| F-BE-01 | BE-REQ-RESOLUTION-02 |
| F-BE-01 | BE-REQ-RESOLUTION-03 |
| F-BE-01 | BE-REQ-RESOLUTION-04 |

### Auflösung der ursprünglichen Anforderung F-TA-04

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-TA-04 | TA-REQ-IPC-01 |
| F-TA-04 | TA-REQ-IPC-02 |

### Auflösung der ursprünglichen Anforderung F-TA-03

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-TA-03 | TA-REQ-STOP-01 |

### Auflösung der ursprünglichen Anforderung F-TA-02

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-TA-02 | TA-REQ-START-01 |
| F-TA-02 | TA-REQ-START-02 |

### Auflösung der ursprünglichen Anforderung F-TA-01

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-TA-01 | TA-REQ-NATIVE-01 |

### Auflösung der ursprünglichen Anforderung F-AG-05

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-AG-05 | AG-REQ-TOKEN-01 |

### Auflösung der ursprünglichen Anforderung F-AG-04

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-AG-04 | AG-REQ-CACHE-01 |

### Auflösung der ursprünglichen Anforderung F-AG-03

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-AG-03 | AG-REQ-PRIORITY-01 |

### Auflösung der ursprünglichen Anforderung F-AG-02

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-AG-02 | AG-REQ-WARN-01 |

### Auflösung der ursprünglichen Anforderung F-AG-01

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-AG-01 | AG-REQ-DEVMODE-01 |

### Auflösung der ursprünglichen Anforderung F-DH-04

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-DH-04 | DH-REQ-DEDUP-01 |

### Neue Anforderungen (v1.6)

| Ursprüngliche ID | Neue Requirement-ID | Beschreibung |
|------------------|---------------------|--------------|
| - | BE-REQ-PORT-01 | Port-Isolation (8200) zur Vermeidung von Konflikten. |
| - | UI-REQ-HERO-01 | Dashboard Hero View für besseren Einstieg. |

### Auflösung der ursprünglichen Anforderung F-DH-03

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-DH-03 | DH-REQ-MAPPING-01 |

### Auflösung der ursprünglichen Anforderung F-DH-02

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-DH-02 | DH-REQ-FUZZY-01 |

### Auflösung der ursprünglichen Anforderung F-DH-01

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-DH-01 | DH-REQ-REAL-01 |

### Auflösung der ursprünglichen Anforderung F-UI-11

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-UI-11 | UI-REQ-VCHART-01 |
| F-UI-11 | UI-REQ-VCHART-02 |
| F-UI-11 | UI-REQ-VCHART-03 |
| F-UI-11 | UI-REQ-VCHART-04 |
| F-UI-11 | UI-REQ-VCHART-05 |
| F-UI-11 | UI-REQ-VCHART-06 |

### Auflösung der ursprünglichen Anforderung F-UI-10

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-UI-10 | UI-REQ-SCOPE-01 |
| F-UI-10 | UI-REQ-SCOPE-02 |
| F-UI-10 | UI-REQ-SCOPE-03 |
| F-UI-10 | UI-REQ-SCOPE-04 |
| F-UI-10 | UI-REQ-SCOPE-05 |

### Auflösung der ursprünglichen Anforderung F-UI-09

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-UI-09 | UI-REQ-ESSAY-01 |
| F-UI-09 | UI-REQ-ESSAY-02 |
| F-UI-09 | UI-REQ-ESSAY-03 |
| F-UI-09 | UI-REQ-ESSAY-04 |
| F-UI-09 | UI-REQ-ESSAY-05 |

### Auflösung der ursprünglichen Anforderung F-UI-08

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-UI-08 | UI-REQ-PCHART-01 |
| F-UI-08 | UI-REQ-PCHART-02 |
| F-UI-08 | UI-REQ-PCHART-03 |
| F-UI-08 | UI-REQ-PCHART-04 |
| F-UI-08 | UI-REQ-PCHART-05 |
| F-UI-08 | UI-REQ-PCHART-06 |
| F-UI-08 | UI-REQ-PCHART-07 |
| F-UI-08 | UI-REQ-PCHART-08 |

### Auflösung der ursprünglichen Anforderung F-UI-07

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-UI-07 | UI-REQ-SUMMARY-01 |
| F-UI-07 | UI-REQ-SUMMARY-02 |
| F-UI-07 | UI-REQ-SUMMARY-03 |
| F-UI-07 | UI-REQ-SUMMARY-04 |
| F-UI-07 | UI-REQ-SUMMARY-05 |

### Auflösung der ursprünglichen Anforderung F-UI-06

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-UI-06 | UI-REQ-TICKER-01 |
| F-UI-06 | UI-REQ-TICKER-02 |
| F-UI-06 | UI-REQ-TICKER-03 |
| F-UI-06 | UI-REQ-TICKER-04 |
| F-UI-06 | UI-REQ-TICKER-05 |

### Auflösung der ursprünglichen Anforderung F-UI-05

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-UI-05 | UI-REQ-PERIOD-01 |
| F-UI-05 | UI-REQ-PERIOD-02 |
| F-UI-05 | UI-REQ-PERIOD-03 |
| F-UI-05 | UI-REQ-PERIOD-04 |
| F-UI-05 | UI-REQ-PERIOD-05 |
| F-UI-05 | UI-REQ-PERIOD-06 |
| F-UI-05 | UI-REQ-PERIOD-07 |

### Auflösung der ursprünglichen Anforderung F-UI-04

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-UI-04 | UI-REQ-LANG-01 |
| F-UI-04 | UI-REQ-LANG-02 |
| F-UI-04 | UI-REQ-LANG-03 |
| F-UI-04 | UI-REQ-LANG-04 |
| F-UI-04 | UI-REQ-LANG-05 |
| F-UI-04 | UI-REQ-LANG-06 |
| F-UI-04 | UI-REQ-LANG-07 |

### Auflösung der ursprünglichen Anforderung F-UI-03

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-UI-03 | UI-REQ-SECTORSEL-01 |
| F-UI-03 | UI-REQ-SECTORSEL-02 |
| F-UI-03 | UI-REQ-SECTORSEL-03 |
| F-UI-03 | UI-REQ-SECTORSEL-04 |
| F-UI-03 | UI-REQ-SECTORSEL-05 |
| F-UI-03 | UI-REQ-SECTORSEL-06 |
| F-UI-03 | UI-REQ-SECTORSEL-07 |
| F-UI-03 | UI-REQ-SECTORSEL-08 |

### Auflösung der ursprünglichen Anforderung F-UI-02

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-UI-02 | UI-REQ-STOCKSEL-01 |
| F-UI-02 | UI-REQ-STOCKSEL-02 |
| F-UI-02 | UI-REQ-STOCKSEL-03 |
| F-UI-02 | UI-REQ-STOCKSEL-04 |
| F-UI-02 | UI-REQ-STOCKSEL-05 |
| F-UI-02 | UI-REQ-STOCKSEL-06 |
| F-UI-02 | UI-REQ-STOCKSEL-07 |
| F-UI-02 | UI-REQ-STOCKSEL-08 |
| F-UI-02 | UI-REQ-STOCKSEL-09 |
| F-UI-02 | UI-REQ-STOCKSEL-10 |
| F-UI-02 | UI-REQ-STOCKSEL-11 |
| F-UI-02 | UI-REQ-STOCKSEL-12 |

### Auflösung der ursprünglichen Anforderung F-UI-01

| Ursprüngliche Requirement-ID | Neue Requirement-ID |
|-----------------------------|---------------------|
| F-UI-01 | UI-REQ-DASH-01 |
| F-UI-01 | UI-REQ-DASH-02 |
| F-UI-01 | UI-REQ-DASH-03 |
| F-UI-01 | UI-REQ-DASH-04 |
| F-UI-01 | UI-REQ-DASH-05 |
| F-UI-01 | UI-REQ-DASH-06 |
| F-UI-01 | UI-REQ-DASH-07 |
| F-UI-01 | UI-REQ-DASH-08 |
| F-UI-01 | UI-REQ-CTX-01 |
| F-UI-01 | UI-REQ-CTX-02 |
| F-UI-01 | UI-REQ-CTX-03 |
| F-UI-01 | UI-REQ-CTX-04 |
| F-UI-01 | UI-REQ-CTX-05 |
| F-UI-01 | UI-REQ-CTX-06 |
| F-UI-01 | UI-REQ-CTX-07 |
| F-UI-01 | UI-REQ-CTX-08 |
| F-UI-01 | UI-REQ-CTX-09 |
| F-UI-01 | UI-REQ-STATE-01 |
| F-UI-01 | UI-REQ-STATE-02 |
| F-UI-01 | UI-REQ-STATE-03 |
| F-UI-01 | UI-REQ-STATE-04 |
| F-UI-01 | UI-REQ-STATE-05 |
| F-UI-01 | UI-REQ-LINK-01 |
| F-UI-01 | UI-REQ-LINK-02 |
| F-UI-01 | UI-REQ-LINK-03 |
## Arbeitsübersicht – Identifizierte Sammelanforderungen (nicht normativ)

### UI (Frontend)

| Referenz | Kurzbeschreibung |
|--------|------------------|
| ~~F-UI-01~~ | ~~Dashboard mit Marktübersicht (aufgelöst)~~ |
| ~~F-UI-02~~ | ~~Ticker-Eingabe mit Fehlertoleranz (aufgelöst)~~ |
| ~~F-UI-03~~ | ~~Sektor-Auswahl (aufgelöst)~~ |
| ~~F-UI-04~~ | ~~Sprachumschaltung (aufgelöst)~~ |
| ~~F-UI-05~~ | ~~Zeitraumauswahl (aufgelöst)~~ |
| ~~F-UI-06~~ | ~~Nachrichtenanzeige (aufgelöst)~~ |
| ~~F-UI-07~~ | ~~Executive Summary (aufgelöst)~~ |
| ~~F-UI-08~~ | ~~Preis-Chart (aufgelöst)~~ |
| ~~F-UI-09~~ | ~~KI-Analyseausgabe (aufgelöst)~~ |
| ~~F-UI-10~~ | ~~Analyse-Scope (aufgelöst)~~ |
| ~~F-UI-11~~ | ~~Volumen-Chart (aufgelöst)~~ |

### Backend (AI Service)

| Referenz | Kurzbeschreibung |
|--------|------------------|
| ~~F-BE-01~~ | ~~Ticker-Auflösung (aufgelöst)~~ |
| ~~F-BE-02~~ | ~~Fundamentaldaten (aufgelöst)~~ |
| ~~F-BE-03~~ | ~~Historische Preisdaten (aufgelöst)~~ |
| ~~F-BE-04~~ | ~~Nachrichtenaggregation (aufgelöst)~~ |
| ~~F-BE-05~~ | ~~KI-Analyse & Bericht (aufgelöst)~~ |

### Desktop / Governance / Data Handling

| Referenz | Kurzbeschreibung |
|--------|------------------|
| ~~F-TA-01~~ | ~~Native Desktop-App (aufgelöst)~~ |
| ~~F-TA-02~~ | ~~Backend-Prozesssteuerung (aufgelöst)~~ |
| ~~F-TA-03~~ | ~~Backend-Stopp (aufgelöst)~~ |
| ~~F-TA-04~~ | ~~Typed IPC Service Layer (aufgelöst)~~ |
| ~~F-AG-01~~ | ~~DEV_MODE (aufgelöst)~~ |
| ~~F-AG-02~~ | ~~API-Startup-Warnung (aufgelöst)~~ |
| ~~F-AG-03~~ | ~~Provider-Priorisierung (aufgelöst)~~ |
| ~~F-AG-04~~ | ~~Cache Pre-Check (aufgelöst)~~ |
| ~~F-AG-05~~ | ~~Token-Usage-Tracking (aufgelöst)~~ |
| ~~F-DH-01~~ | ~~Internetbasierte Ticker-Auflösung (aufgelöst)~~ |
| ~~F-DH-02~~ | ~~Fehlertolerante Auflösung (aufgelöst)~~ |
| ~~F-DH-03~~ | ~~Name → Symbol Mapping (aufgelöst)~~ |
| ~~F-DH-04~~ | ~~In-Flight De-Duplizierung (aufgelöst)~~ |

## 1. Projektübersicht

### 1.1 Projektname

Stock News Pro — AI-powered Financial Intelligence Dashboard

### 1.2 Projektziel

Ziel des Projekts Stock News Pro ist die Entwicklung einer modularen, desktopbasierten Softwareplattform zur KI-gestützten Analyse von Finanzmärkten, Aktien und Sektoren.

Die Plattform dient der strukturierten Aufbereitung, Analyse und Interpretation finanzrelevanter Daten sowie der unterstützenden Generierung von Analyseberichten und Zusammenfassungen.

Darüber hinaus definiert Stock News Pro einen fachlichen Rahmen für zukünftige funktionale Erweiterungen im Kontext der Finanzanalyse.

Das Projektziel ist verbindlich und bildet die fachliche Grundlage für alle weiteren Anforderungen dieses Lastenhefts.

### 1.3 Zielgruppe

Stock News Pro richtet sich an Nutzer, die finanzielle Informationen strukturiert analysieren und für fundierte Entscheidungen nutzen möchten.

Primäre Zielgruppen sind:
- Privatanleger
- Finanzanalysten
- Investment-Berater

Alle Anforderungen dieses Lastenhefts sind an den Bedürfnissen dieser Zielgruppen auszurichten.

Hinweis: Die früheren Abschnitte 1.4–1.7 (Formale Spezifikationsregeln, Dokumentationsartefakte, Änderungsprozess und Governance) wurden mit Version 1.3 vollständig entfernt.  
Die normative Definition dieser Inhalte erfolgt ausschließlich in DESIGN.md.

## 2. Funktionale Anforderungen

### 2.1 Benutzeroberfläche (Frontend)

Die Benutzeroberfläche stellt die Interaktionsschicht zwischen Nutzer und System dar.

#### 2.1.1 UI-REQ-DASH-01 — Bereitstellung eines Dashboard-Containers

Die Benutzeroberfläche muss einen Dashboard-Container bereitstellen, der als primäre strukturelle Einheit der Benutzeroberfläche fungiert.

#### 2.1.2 UI-REQ-DASH-02 — Initialisierbarkeit des Dashboard-Containers

Der Dashboard-Container muss initialisierbar sein, ohne dass Inhalte, Daten oder Analyseergebnisse vorliegen.

#### 2.1.3 UI-REQ-DASH-03 — Aufnahme mehrerer UI-Elemente

Der Dashboard-Container muss die gleichzeitige Aufnahme mehrerer UI-Elemente ermöglichen.

#### 2.1.4 UI-REQ-DASH-04 — Dynamische Erweiterbarkeit

Der Dashboard-Container muss die dynamische Hinzufügung weiterer UI-Elemente zur Laufzeit ermöglichen.

#### 2.1.5 UI-REQ-DASH-05 — Inhaltsunabhängige Struktur

#### 2.1.5 UI-REQ-DASH-05 — Inhaltsunabhängige Struktur

Der Dashboard-Container muss unabhängig vom fachlichen Inhalt der enthaltenen UI-Elemente funktionieren.

#### 2.1.6 UI-REQ-HERO-01 — Initialer Hero-Screen (Empty State)

Die Benutzeroberfläche muss im initialen Zustand (keine aktive Analyse) einen "Hero-Screen" anzeigen, der eine klare Suchaufforderung und Schnellzugriffe (Trending Stocks) bietet, anstatt leerer Platzhalter.

#### 2.1.6 UI-REQ-DASH-06 — Unterstützung heterogener UI-Elementtypen

Der Dashboard-Container muss unterschiedliche UI-Elementtypen darstellen können.

#### 2.1.7 UI-REQ-DASH-07 — Bezug von Daten über interne Schnittstellen

UI-Elemente müssen ihre Daten ausschließlich über interne, definierte Schnittstellen beziehen.

#### 2.1.8 UI-REQ-DASH-08 — Bereitstellung von UI-Zuständen

UI-Elemente müssen ihren Anzeige- und Interaktionszustand über interne, definierte Schnittstellen bereitstellen.

#### 2.1.9 UI-REQ-CTX-01 — UI-Kontext: Analyseobjekt Aktie

Die Benutzeroberfläche muss einen Kontextwert selected_stock führen.

#### 2.1.10 UI-REQ-CTX-02 — UI-Kontext: Analyseobjekt Sektor

Die Benutzeroberfläche muss einen Kontextwert selected_sector führen.

Die Benutzeroberfläche muss einen Kontextwert selected_sector führen.

#### 2.1.11 [ENTFERNT] UI-REQ-CTX-03 — UI-Kontext: Analyse-Scope

(Anforderung entfernt mit v1.6 zugunsten einer impliziten "Combined"-Logik).

#### 2.1.12 UI-REQ-CTX-04 — UI-Kontext: Sprache

Die Benutzeroberfläche muss einen Kontextwert language führen.

#### 2.1.13 UI-REQ-CTX-05 — UI-Kontext: Zeitraum

Die Benutzeroberfläche muss einen Kontextwert time_range führen.

#### 2.1.14 UI-REQ-CTX-06 — UI-Kontext: Thematische Suchanfrage

Die Benutzeroberfläche muss einen Kontextwert `theme_query` führen.

#### 2.1.15 UI-REQ-CTX-10 — Kontext-Exklusivität

Die Benutzeroberfläche muss sicherstellen, dass `selected_stock` und `theme_query` nicht gleichzeitig belegt sind (gegenseitiger Ausschluss).

#### 2.1.15 UI-REQ-CTX-07 — Gleichzeitige Kontextführung

Die Benutzeroberfläche muss alle definierten Kontextwerte gleichzeitig führen können.

#### 2.1.16 UI-REQ-CTX-08 — Leerer Kontextzustand Aktie

Die Benutzeroberfläche muss einen gültigen Zustand ohne gesetzten selected_stock unterstützen.

#### 2.1.17 UI-REQ-CTX-09 — Leerer Kontextzustand Sektor

Die Benutzeroberfläche muss einen gültigen Zustand ohne gesetzten selected_sector unterstützen.

#### 2.1.18 UI-REQ-STATE-01 — Analysezustand

Die Benutzeroberfläche muss einen Systemzustand analysis_status führen.

#### 2.1.19 UI-REQ-STATE-02 — Fehlerzustand

Die Benutzeroberfläche muss einen Systemzustand error_state führen.

#### 2.1.20 UI-REQ-STATE-03 — Datenherkunft

Die Benutzeroberfläche muss einen Systemzustand data_origin führen.

#### 2.1.21 UI-REQ-STATE-04 — Generiert-Kennzeichnung

Die Benutzeroberfläche muss einen Systemzustand generated_flag führen.

#### 2.1.22 UI-REQ-STATE-05 — Aktualität

Die Benutzeroberfläche muss einen Systemzustand fetched_at führen.

#### 2.1.23 UI-REQ-LINK-01 — Abhängigkeit Aktie → Sektor

Wenn selected_stock gesetzt wird und ein zugehöriger Sektor vorliegt, muss selected_sector aktualisiert werden.

#### 2.1.24 UI-REQ-LINK-02 — Abhängigkeit bei Sektorwechsel

Wenn selected_stock gesetzt ist und selected_sector geändert wird, müssen beide Kontextwerte gültig bleiben.

Wenn selected_stock gesetzt ist und selected_sector geändert wird, müssen beide Kontextwerte gültig bleiben.

#### 2.1.25 [ENTFERNT] UI-REQ-LINK-03 — Scope-Steuerung

(Anforderung entfernt mit v1.6).

### 2.2 Analyseobjekt-Auswahl Aktie (F-UI-02)

#### 2.2.1 UI-REQ-STOCKSEL-01 — Bereitstellung einer Texteingabe zur Aktienauswahl

Die Benutzeroberfläche stellt eine Texteingabe bereit, über die Nutzer eine Aktie zur Analyse auswählen können.

#### 2.2.2 UI-REQ-STOCKSEL-02 — Kontextwert für Roh-Eingabe zur Aktienauswahl

Die Benutzeroberfläche führt einen Kontextwert `stock_query`, der die aktuelle Roh-Eingabe zur Aktienauswahl repräsentiert.

#### 2.2.3 UI-REQ-STOCKSEL-03 — Akzeptanz von Symbol- und Namenseingaben

Die Benutzeroberfläche akzeptiert `stock_query` sowohl als Wert vom Typ Symbol (z. B. Ticker) als auch als Wert vom Typ Name (z. B. Unternehmensname).

#### 2.2.4 UI-REQ-STOCKSEL-04 — Normalisierung der Roh-Eingabe

Die Benutzeroberfläche normalisiert `stock_query` vor der Auflösung durch Trimmen führender und nachgestellter Whitespaces.

#### 2.2.5 UI-REQ-STOCKSEL-05 — Case-insensitive Verarbeitung der Roh-Eingabe

Die Benutzeroberfläche verarbeitet `stock_query` case-insensitive für die Auflösung.

#### 2.2.6 UI-REQ-STOCKSEL-06 — Auslösung einer Auflösungsanfrage über interne Schnittstellen

Die Benutzeroberfläche löst eine Auflösungsanfrage für `stock_query` ausschließlich über interne, definierte Schnittstellen aus.

#### 2.2.7 UI-REQ-STOCKSEL-07 — Systemzustand für Auflösungsstatus

Die Benutzeroberfläche führt einen Systemzustand stock_resolution_status, der den aktuellen Status der Auflösung von stock_query repräsentiert.

#### 2.2.8 UI-REQ-STOCKSEL-08 — Setzen des Analyseobjekts bei erfolgreicher Auflösung

Bei erfolgreicher Auflösung von `stock_query` setzt die Benutzeroberfläche den Kontextwert `selected_stock` auf das aufgelöste Analyseobjekt.

#### 2.2.9 UI-REQ-STOCKSEL-09 — Kontextwert für Mehrdeutigkeitskandidaten

Die Benutzeroberfläche führt einen Kontextwert `stock_resolution_candidates`, der die Kandidatenliste bei mehrdeutiger Auflösung von `stock_query` repräsentiert.

#### 2.2.10 UI-REQ-STOCKSEL-10 — Übernahme eines Kandidaten als Analyseobjekt

Wenn ein Kandidat aus `stock_resolution_candidates` ausgewählt wird, setzt die Benutzeroberfläche den Kontextwert `selected_stock` auf das ausgewählte Analyseobjekt.

#### 2.2.11 UI-REQ-STOCKSEL-11 — Abbildung eines Auflösungsfehlers als Fehlerzustand

Wenn die Auflösung von `stock_query` fehlschlägt, setzt die Benutzeroberfläche den Systemzustand `error_state` auf einen zur Auflösung gehörenden Fehlerzustand.

#### 2.2.12 UI-REQ-STOCKSEL-12 — Rücksetzen der Aktienauswahl

Die Benutzeroberfläche unterstützt eine Nutzeraktion, die `selected_stock` in den Zustand „nicht gesetzt“ überführt.

### 2.3 Analyseobjekt-Auswahl Sektor (F-UI-03)

#### 2.3.1 UI-REQ-SECTORSEL-01 — Bereitstellung einer Interaktionsmöglichkeit zur Sektorauswahl

Die Benutzeroberfläche stellt eine Interaktionsmöglichkeit zur Auswahl eines Sektors bereit.

#### 2.3.2 UI-REQ-SECTORSEL-02 — Kontextwert für ausgewählten Sektor

Die Benutzeroberfläche führt einen Kontextwert `selected_sector`, der den aktuell ausgewählten Sektor repräsentiert.

#### 2.3.3 UI-REQ-SECTORSEL-03 — Anzeige verfügbarer Sektoren

Die Benutzeroberfläche stellt eine Menge verfügbarer Sektoren zur Auswahl bereit.

#### 2.3.4 UI-REQ-SECTORSEL-04 — Auswahl eines einzelnen Sektors

Die Benutzeroberfläche unterstützt die Auswahl eines einzelnen Sektors aus der bereitgestellten Sektormenge.

#### 2.3.5 UI-REQ-SECTORSEL-05 — Setzen des Sektorkontexts bei Auswahl

Bei Auswahl eines Sektors setzt die Benutzeroberfläche den Kontextwert `selected_sector` auf den ausgewählten Sektor.

#### 2.3.6 UI-REQ-SECTORSEL-06 — Wechsel des ausgewählten Sektors

Die Benutzeroberfläche unterstützt den Wechsel des aktuell gesetzten Sektors durch erneute Auswahl.

#### 2.3.7 UI-REQ-SECTORSEL-07 — Kontextzustand ohne gesetzten Sektor

Die Benutzeroberfläche unterstützt einen gültigen Zustand, in dem kein Sektor ausgewählt ist.

#### 2.3.8 UI-REQ-SECTORSEL-08 — Rücksetzen der Sektorauswahl

Die Benutzeroberfläche unterstützt eine Nutzeraktion, die den Kontextwert `selected_sector` in den Zustand „nicht gesetzt“ überführt.

### 2.4 Sprachumschaltung (F-UI-04)

#### 2.4.1 UI-REQ-LANG-01 — Bereitstellung einer Interaktionsmöglichkeit zur Sprachumschaltung

Die Benutzeroberfläche stellt eine Interaktionsmöglichkeit bereit, über die Nutzer die Anzeigesprache auswählen können.

#### 2.4.2 UI-REQ-LANG-02 — Kontextwert für aktuelle Sprache

Die Benutzeroberfläche führt einen Kontextwert `language`, der die aktuell aktive Anzeigesprache repräsentiert.

#### 2.4.3 UI-REQ-LANG-03 — Bereitstellung verfügbarer Sprachen

Die Benutzeroberfläche stellt eine Menge verfügbarer Sprachen zur Auswahl bereit.

#### 2.4.4 UI-REQ-LANG-04 — Auswahl einer einzelnen Sprache

Die Benutzeroberfläche unterstützt die Auswahl genau einer Sprache aus der bereitgestellten Sprachmenge.

#### 2.4.5 UI-REQ-LANG-05 — Setzen des Sprachkontexts bei Auswahl

Bei Auswahl einer Sprache setzt die Benutzeroberfläche den Kontextwert `language` auf die ausgewählte Sprache.

#### 2.4.6 UI-REQ-LANG-06 — Wechsel der aktiven Sprache

Die Benutzeroberfläche unterstützt den Wechsel der aktuell gesetzten Sprache durch erneute Auswahl.

#### 2.4.7 UI-REQ-LANG-07 — Gültiger Kontextzustand der Sprache

Die Benutzeroberfläche unterstützt einen gültigen Zustand, in dem der Kontextwert `language` gesetzt ist.

### 2.5 Zeitraumauswahl (F-UI-05)

#### 2.5.1 UI-REQ-PERIOD-01 — Bereitstellung einer Interaktionsmöglichkeit zur Zeitraumauswahl

Die Benutzeroberfläche stellt eine Interaktionsmöglichkeit bereit, über die Nutzer den Zeitraum für die historische Datenanzeige auswählen können.

#### 2.5.2 UI-REQ-PERIOD-02 — Kontextwert für den Analysezeitraum

Die Benutzeroberfläche führt einen Kontextwert `time_range`, der den aktuell ausgewählten Analysezeitraum repräsentiert.

#### 2.5.3 UI-REQ-PERIOD-03 — Unterstützung definierter Zeitintervalle

Die Benutzeroberfläche unterstützt die Auswahl definierter Zeitintervalle (z. B. 24H, 7D, 1M, 3M, 6M, 1Y, 3Y, 5Y, 10Y, ALL).

#### 2.5.4 UI-REQ-PERIOD-04 — Setzen des Zeitraumkontexts bei Auswahl

Bei Auswahl eines Zeitintervalls setzt die Benutzeroberfläche den Kontextwert `time_range` auf das ausgewählte Intervall.

#### 2.5.5 UI-REQ-PERIOD-05 — Visuelle Markierung des aktiven Zeitintervalls

Die Benutzeroberfläche kennzeichnet das aktuell aktive Zeitintervall visuell innerhalb der Interaktionsmöglichkeit.

#### 2.5.6 UI-REQ-PERIOD-06 — Unterstützung eines Standardzeitraums

Die Benutzeroberfläche initialisiert den Kontextwert `time_range` mit einem definierten Standardzeitraum (z. B. 1Y).

#### 2.5.7 UI-REQ-PERIOD-07 — Wechsel des Analysezeitraums

Die Benutzeroberfläche unterstützt den Wechsel des aktuellen Zeitraums durch erneute Auswahl eines Intervalls.

### 2.6 Nachrichten-Anzeige (F-UI-06)

#### 2.6.1 UI-REQ-TICKER-01 — Bereitstellung eines visuellen Elements zur Nachrichtenanzeige

Die Benutzeroberfläche stellt ein visuelles Element bereit, das Nachrichten als Ticker oder Liste darstellt.

#### 2.6.2 UI-REQ-TICKER-02 — Trennung von Branchen- und Unternehmensnachrichten

Die Benutzeroberfläche ermöglicht die separate Darstellung von sektorbezogenen Nachrichten und unternehmensbezogenen Nachrichten.

#### 2.6.3 UI-REQ-TICKER-03 — Darstellung von Nachrichtentiteln

Das visuelle Element zeigt mindestens den Titel der jeweiligen Nachricht an.

#### 2.6.4 UI-REQ-TICKER-04 — Kennzeichnung der Nachrichtenquelle

Das visuelle Element zeigt für jede Nachricht die zugehörige Quelle an.

#### 2.6.5 UI-REQ-TICKER-05 — Anzeige der Nachrichtenaktualität

Das visuelle Element zeigt für jede Nachricht den Erstellungs- oder Fetch-Zeitpunkt an.

### 2.7 Executive Summary Card (F-UI-07)

#### 2.7.1 UI-REQ-SUMMARY-01 — Bereitstellung einer Zusammenfassungskomponente

Die Benutzeroberfläche stellt eine Komponente bereit, die eine prägnante Zusammenfassung der Analyseergebnisse anzeigt.

#### 2.7.2 UI-REQ-SUMMARY-02 — Anzeige des generierten Zusammenfassungstextes

Die Benutzeroberfläche stellt den durch die KI generierten Text der Zusammenfassung dar.

#### 2.7.3 UI-REQ-SUMMARY-03 — Visuelle Kennzeichnung als KI-Generiert

Die Zusammenfassung muss explizit als durch KI generiertes Analyseergebnis gekennzeichnet sein.

#### 2.7.4 UI-REQ-SUMMARY-04 — Anzeige des Generierungszeitpunkts

Die Benutzeroberfläche zeigt den Zeitpunkt der Generierung der Zusammenfassung an.

#### 2.7.5 UI-REQ-SUMMARY-05 — Darstellung wesentlicher Kennzahlen

Die Benutzeroberfläche ermöglicht die integrierte Darstellung wesentlicher Kennzahlen des Analyseobjekts.

### 2.8 Preis-Chart (F-UI-08)

#### 2.8.1 UI-REQ-PCHART-01 — Bereitstellung eines Charts zur Preisdarstellung

Die Benutzeroberfläche stellt ein grafisches Element zur Visualisierung historischer Preisdaten bereit.

#### 2.8.2 UI-REQ-PCHART-02 — Darstellung von zeitbasierten Preisdaten

Das Element bildet historische Preise auf einer Zeitachse ab.

#### 2.8.3 UI-REQ-PCHART-03 — Anzeige von Detailwerten bei Interaktion

Das Element zeigt bei Nutzerinteraktion (z. B. Hover) den konkreten Preis und das Datum eines Datenpunktes an.

#### 2.8.4 UI-REQ-PCHART-04 — Automatische Skalierung der Preisachse

Die Skalierung der Preisachse passt sich automatisch dem Wertebereich der dargestellten Daten an.

#### 2.8.5 UI-REQ-PCHART-05 — Kennzeichnung des Zeitintervalls

Der grafische Behälter kennzeichnet den aktuell dargestellten Zeitraum visuell.

#### 2.8.6 UI-REQ-PCHART-06 — Synchronisation mit Zeitraumkontext

Die Darstellung im Preis-Chart erfolgt konsistent zum Kontextwert `time_range`.

#### 2.8.7 UI-REQ-PCHART-07 — Behandlung fehlender Datenpunkte

Bei fehlenden historischen Datenpunkten muss das grafische Element eine konsistente Linie oder eine explizite Lücke darstellen.

#### 2.8.8 UI-REQ-PCHART-08 — Responsive Anpassung der Chartgröße

Das grafische Element passt seine Größe dynamisch an den verfügbaren Platz im Dashboard-Container an.

### 2.9 AI-Essay Ausgabe (F-UI-09)

#### 2.9.1 UI-REQ-ESSAY-01 — Bereitstellung einer Komponente für ausführliche KI-Analysen

Die Benutzeroberfläche stellt eine Komponente zur Anzeige detaillierter, essayistischer KI-Analysen bereit.

#### 2.9.2 UI-REQ-ESSAY-02 — Unterstützung formatierter Textausgabe

Die Komponente unterstützt die strukturierte Darstellung von Text (z. B. Absätze, Überschriften).

#### 2.9.3 UI-REQ-ESSAY-03 — Anzeige des KI-generierten Essay-Textes

Die Komponente stellt den durch die KI erzeugten ausführlichen Analysetext dar.

#### 2.9.4 UI-REQ-ESSAY-04 — Explizite Kennzeichnung als KI-Produkt

Das Analyse-Essay muss eindeutig als automatisiert generiertes Produkt gekennzeichnet sein.

#### 2.9.5 UI-REQ-ESSAY-05 — Scrollbare Inhaltsdarstellung

Die Komponente ermöglicht das Lesen umfangreicher Texte durch Bereitstellung einer Scroll-Funktionalität.

### 2.10 [ENTFERNT] Analyse-Scope Steuerung (F-UI-10)

(Dieser Abschnitt wurde in Version 1.6 entfernt).

### 2.12 Thematische Suche (F-UI-12)

#### 2.12.1 UI-REQ-THEMESEL-01 — Bereitstellung eines Themen-Eingabefeldes

Die Benutzeroberfläche stellt ein dediziertes Eingabefeld für thematische Suchbegriffe (z. B. "Künstliche Intelligenz") bereit.

#### 2.12.2 UI-REQ-THEMESEL-02 — Exklusives Eingabeverhalten

Bei Eingabe in das Themen-Feld wird eine eventuell bestehende Aktien-Auswahl (`selected_stock`) automatisch entfernt.

#### 2.12.3 UI-REQ-THEMESEL-03 — Tooltip-Hilfe

Das Eingabefeld muss bei Benutzerinteraktion (Hover/Focus) einen erklärenden Hilfetext (Tooltip) anzeigen.

#### 2.12.4 UI-REQ-THEMESEL-04 — Auslösung der Themen-Analyse

Die Benutzeroberfläche löst bei Bestätigung der Themeneingabe eine Analyseanfrage an den Themen-Endpunkt aus.

### 2.11 Volumen-Chart (F-UI-11)

#### 2.11.1 UI-REQ-VCHART-01 — Bereitstellung eines Charts zur Volumendarstellung

Die Benutzeroberfläche stellt ein grafisches Element zur Visualisierung des Handelsvolumens bereit.

#### 2.11.2 UI-REQ-VCHART-02 — Darstellung stündlicher Volumendaten der letzten 48 Stunden

Das grafische Element stellt das Handelsvolumen in stündlicher Granularität für einen Zeitraum von 48 Stunden dar.

#### 2.11.3 UI-REQ-VCHART-03 — Anzeige von Volumenwerten bei Interaktion

Das Element zeigt bei Nutzerinteraktion (z. B. Hover) das konkrete Volumen und den Zeitpunkt an.

#### 2.11.4 UI-REQ-VCHART-04 — Darstellung als Balken- oder Flächendiagramm

Das Volumen wird bevorzugt als Balkendiagramm (Bar Chart) dargestellt.

#### 2.11.5 UI-REQ-VCHART-05 — Konsistenz zum Analyseobjekt Aktie

Der Volumen-Chart zeigt die Daten des im Kontextwert `selected_stock` gesetzten Analyseobjekts an.

#### 2.11.6 UI-REQ-VCHART-06 — Vertikale Anordnung zum Preis-Chart

Der Volumen-Chart wird unterhalb des Preis-Charts angeordnet, um einen direkten visuellen Vergleich zu ermöglichen.

### 2.12 Sektor-Heatmap (F-UI-12)

#### 2.12.1 UI-REQ-HEATMAP-01 — Bereitstellung einer Treemap-Komponente für Sektorübersicht

Die Benutzeroberfläche stellt eine grafische Treemap-Komponente bereit, die eine hierarchische Übersicht aller Marktsektoren visualisiert.

#### 2.12.2 UI-REQ-HEATMAP-02 — Größencodierung nach Marktkapitalisierung

Die Treemap-Komponente stellt die relative Größe jeder Sektorkachel proportional zur aggregierten Marktkapitalisierung des Sektors dar.

#### 2.12.3 UI-REQ-HEATMAP-03 — Farbcodierung nach Performance

Die Treemap-Komponente zeigt die Performance jedes Sektors durch Farbcodierung an (grün für positive, rot für negative Veränderung).

#### 2.12.4 UI-REQ-HEATMAP-04 — Intensität der Farbcodierung nach Performancegrad

Die Intensität der Farbcodierung (Sättigung) variiert proportional zum Ausmaß der Performanceveränderung.

#### 2.12.5 UI-REQ-HEATMAP-05 — Anzeige von Sektor-Details bei Interaktion

Die Treemap-Komponente zeigt bei Nutzerinteraktion (z. B. Hover) den Sektornamen und die prozentuale Veränderung an.

#### 2.12.6 UI-REQ-HEATMAP-06 — Navigation zu Sektordetails bei Klick

Bei Klick auf eine Sektorkachel setzt die Benutzeroberfläche den Kontextwert `selected_sector` auf den ausgewählten Sektor.

#### 2.12.7 UI-REQ-HEATMAP-07 — Darstellung von Top-Aktien innerhalb einer Sektorkachel

Die Treemap-Komponente kann innerhalb jeder Sektorkachel die Top-Aktien des Sektors als verschachtelte Unterkacheln darstellen.

#### 2.12.8 UI-REQ-HEATMAP-08 — Synchronisation mit Zeitraumkontext

Die Performanceberechnung der Heatmap erfolgt konsistent zum Kontextwert `time_range`.

#### 2.12.9 UI-REQ-HEATMAP-09 — Responsive Anpassung der Heatmap-Größe

Die Treemap-Komponente passt ihre Größe dynamisch an den verfügbaren Platz im Dashboard-Container an.

### 2.13 Sparklines — Kompakte Trend-Visualisierung

#### 2.13.1 UI-REQ-SPARK-01 — Bereitstellung einer Sparkline-Komponente

Die Benutzeroberfläche muss eine hochoptimierte Sparkline-Komponente (Mini-Chart) zur Visualisierung von Preistrends bereitstellen.

#### 2.13.2 UI-REQ-SPARK-02 — Farbindikation nach Preistrend

Die Sparkline-Komponente muss den Preistrend farblich kennzeichnen (z. B. Grün für positive Kursentwicklung, Rot für negative Kursentwicklung).

#### 2.13.3 UI-REQ-SPARK-03 — Integration in Watchlists und Suchergebnisse

Die Sparkline-Komponente muss in Listenansichten (Watchlists) und Suchergebnissen zur schnellen Trend-Erfassung integriert sein.

#### 2.13.4 UI-REQ-SPARK-04 — Fixierte Skalierung zur Vergleichbarkeit

Die Sparkline-Komponente muss die Kursdaten so skalieren, dass Trends zwischen verschiedenen Sparklines in derselben Ansicht visuell vergleichbar sind.

## 3. Backend (AI Service)

Alle Backend-Anforderungen beschreiben die Verhaltensweisen des KI-Dienstes und seiner Schnittstellen.

#### 3.1.1 BE-REQ-RESOLUTION-01 — Bereitstellung einer Schnittstelle zur Ticker-Auflösung

Das Backend muss eine programmtechnische Schnittstelle bereitstellen, die eine Texteingabe (Name oder Symbol) in ein eindeutiges Börsensymbol auflöst.

#### 3.1.2 BE-REQ-RESOLUTION-02 — Unterstützung von Fuzzy-Matching bei der Auflösung

Die Auflösungsschnittstelle muss Tippfehler tolerieren und bei unscharfen Eingaben passende Kandidaten zurückgeben.

#### 3.1.3 BE-REQ-RESOLUTION-03 — Rückgabe strukturierter Metadaten bei Auflösung

Bei erfolgreicher Auflösung muss die Schnittstelle Symbol, Unternehmensname und Sektor zurückgeben.

#### 3.1.4 BE-REQ-RESOLUTION-04 — Fehlerbehandlung bei unbekannten Analyseobjekten

Wenn eine Eingabe nicht aufgelöst werden kann, muss die Schnittstelle einen definierten Fehlerzustand zurückgeben.

#### 3.2.1 BE-REQ-FUNDAMENTAL-01 — Bereitstellung einer Schnittstelle für Fundamentaldaten

Das Backend muss eine Schnittstelle bereitstellen, die für ein gegebenes Symbol fundamentale Kennzahlen liefert.

#### 3.2.2 BE-REQ-FUNDAMENTAL-02 — Lieferung von Bewertungskennzahlen

Die Schnittstelle muss mindestens P/E Ratio und PEG Ratio für das Analyseobjekt zurückgeben.

#### 3.2.3 BE-REQ-FUNDAMENTAL-03 — Lieferung von Qualitätskennzahlen

Die Schnittstelle muss mindestens ROE und Debt-to-Equity Ratio für das Analyseobjekt zurückgeben.

#### 3.2.4 BE-REQ-FUNDAMENTAL-04 — Lieferung von Analysten-Ratings

Die Schnittstelle muss Analysten-Kursziele (Mean, High, Low) und die aktuelle Empfehlung zurückgeben.

#### 3.3.1 BE-REQ-HISTORY-01 — Bereitstellung einer Schnittstelle für historische Preise

Das Backend muss eine Schnittstelle bereitstellen, die historische Preisdaten für ein gegebenes Symbol und einen definierten Zeitraum liefert.

#### 3.3.2 BE-REQ-HISTORY-02 — Lieferung von Zeit-Preis-Paaren

Die Historien-Schnittstelle muss eine Liste von Paaren aus Zeitstempel und Schlusskurs zurückgeben.

#### 3.3.3 BE-REQ-HISTORY-03 — Unterstützung variabler Zeiträume

Die Schnittstelle muss Datenabfragen für unterschiedliche konfiguriurable Zeitperioden ermöglichen.

#### 3.4.1 BE-REQ-NEWS-01 — Aggregation von Nachrichtenquellen

Das Backend muss Nachrichten aus konfigurierten externen Quellen (z. B. RSS-Feeds, News-APIs) aggregieren.

#### 3.4.2 BE-REQ-NEWS-02 — Filterung von Nachrichten nach Sektor

Das Backend muss die Aggregation und Filterung von Nachrichten basierend auf Branchensektoren unterstützen.

#### 3.4.3 BE-REQ-NEWS-03 — Filterung von Nachrichten nach Unternehmen

Das Backend muss die Aggregation und Filterung von Nachrichten basierend auf spezifischen Aktiensymbolen unterstützen.

#### 3.4.4 BE-REQ-NEWS-04 — Normalisierung von Nachrichtenmetadaten

Aggregierte Nachrichten müssen in einer einheitlichen Struktur (Titel, Quelle, Zeitstempel, Link) bereitgestellt werden.

#### 3.5.1 BE-REQ-AI-01 — Generierung von Analyse-Zusammenfassungen

Das Backend muss unter Nutzung von KI-Modellen automatisierte Zusammenfassungen (Executive Summaries) erzeugen.

#### 3.5.2 BE-REQ-AI-02 — Generierung ausführlicher Analyse-Berichte

Das Backend muss unter Nutzung von KI-Modellen detaillierte Analyse-Essays zu Unternehmen und Sektoren erzeugen.

#### 3.5.3 BE-REQ-AI-03 — Berücksichtigung von Kontextvariablen in KI-Prompts

Die KI-Generierung muss Sektor, Stock und Zeitrahmen als Parameter in die Prompt-Erstellung einbeziehen.

#### 3.5.4 BE-REQ-AI-04 — Unterstützung mehrsprachiger KI-Ausgaben

Das Backend muss die Ausgabe der KI-generierten Texte in den angeforderten Sprachen (z. B. Deutsch, Englisch) ermöglichen.

#### 3.5.5 BE-REQ-AI-05 — Signierung der KI-Antworten mit Metadaten

Das System muss KI-Antworten mit Metadaten über Generierungszeitpunkt und verwendetes Modell versehen.

### 3.6 Sektor-Performance-Daten (F-BE-06)

#### 3.6.1 BE-REQ-SECTOR-01 — Bereitstellung einer Schnittstelle für Sektor-Performance

Das Backend muss eine Schnittstelle bereitstellen, die aggregierte Performance-Daten für alle Marktsektoren liefert.

#### 3.6.2 BE-REQ-SECTOR-02 — Lieferung von Sektor-Kennzahlen

Die Schnittstelle muss für jeden Sektor die prozentuale Veränderung und die aggregierte Marktkapitalisierung zurückgeben.

#### 3.6.3 BE-REQ-SECTOR-03 — Lieferung von Top-Aktien pro Sektor

Die Schnittstelle muss für jeden Sektor eine Liste der Top-Aktien (nach Marktkapitalisierung) mit deren individueller Performance liefern.

#### 3.6.4 BE-REQ-SECTOR-04 — Unterstützung variabler Zeiträume für Sektor-Performance

Die Schnittstelle muss Sektor-Performance-Daten für unterschiedliche konfigurierbare Zeitperioden (z. B. 1D, 1W, 1M, 1Y) bereitstellen.

### 3.7 Sparkline-Daten-Service

#### 3.7.1 BE-REQ-SPARK-01 — Bereitstellung kompakter Zeitreihendaten

Das System muss optimierte, kompakte Zeitreihendaten (z. B. aggregierte Schlusskurse) speziell für die Sparkline-Visualisierung bereitstellen.

#### 3.7.2 BE-REQ-SPARK-02 — Unterstützung zeitraumabhängiger Sparkline-Daten

Das System muss die Sparkline-Daten in Abhängigkeit vom gewählten Zeitraum (z. B. 1D, 1W, 1M) liefern.

### 3.8 Thematische Analyse (Backend)

#### 3.8.1 BE-REQ-THEME-01 — Bereitstellung eines Themen-Analyse-Endpunkts

Das System stellt einen API-Endpunkt `/analyze/theme` zur Verfügung.

#### 3.8.2 BE-REQ-THEME-02 — Identifikation thematischer Gewinner und Verlierer

Der Endpunkt muss eine Liste von assoziierten Aktien zurückgeben, die als "Winners" (positiver Einfluss) oder "Losers" (negativer Einfluss/Risiko) klassifiziert sind.

### 3.9 Portfolio Management (Backend)

#### 3.9.1 BE-REQ-PORTFOLIO-01 — Bereitstellung von Portfolio-Endpunkten

Das System stellt API-Endpunkte zur Verwaltung von Portfolio-Transaktionen bereit.

#### 3.9.2 BE-REQ-PORTFOLIO-02 — Hinzufügen von Transaktionen

Das System ermöglicht das Hinzufügen einer Transaktion (Ticker, Menge, Preis, Datum) über einen API-Aufruf.

#### 3.9.3 BE-REQ-PORTFOLIO-03 — Abrufen des Portfolios

Das System ermöglicht das Abrufen aller gespeicherten Transaktionen als Liste.

#### 3.9.4 BE-REQ-PORTFOLIO-04 — Löschen von Transaktionen

Das System ermöglicht das Löschen einer Transaktion anhand ihrer ID.

#### 3.8.3 BE-REQ-THEME-03 — Generierung eines Themen-Reports

Der Analyse-Dienst generiert einen textuellen Report, der das Thema und seine Auswirkungen auf den Markt beschreibt.

---

## 4. Desktop-Integration & Systemverhalten

#### 4.1 TA-REQ-NATIVE-01 — Bereitstellung einer nativen Desktop-Anwendung

Das System muss als native Desktop-Anwendung für macOS und Windows ausführbar sein.

#### 4.2.1 TA-REQ-START-01 — Automatischer Start des Backend-Prozesses

Das System muss den Backend-Prozess (KI-Dienst) bei jedem Start der Desktop-Anwendung automatisch initialisieren.

#### 4.2.2 TA-REQ-START-02 — Überprüfung der Backend-Verfügbarkeit nach Systemstart

Die Desktop-Anwendung muss nach dem Start prüfen, ob der Backend-Prozess erfolgreich initialisiert wurde und über IPC erreichbar ist.

#### 4.3 TA-REQ-STOP-01 — Automatischer Stopp des Backend-Prozesses

Das System muss den Backend-Prozess beim ordnungsgemäßen Beenden der Desktop-Anwendung automatisch terminieren.

#### 4.4.1 TA-REQ-IPC-01 — Bereitstellung einer typisierten IPC-Schnittstelle

Die Kommunikation zwischen Frontend und Backend muss über eine strikt typisierte Inter-Process Communication (IPC) erfolgen.

#### 4.4.2 TA-REQ-IPC-02 — Abbildung von Systemfehlern über IPC

Fehler im Backend-Prozess oder in der IPC-Schicht müssen als typisierte Fehlermeldungen an das Frontend übermittelt werden.

### 4.6 Datenpersistenz (Data Persistence)

#### 4.6.1 BE-REQ-PERSIST-01 — SQLite-basierte Speicherung

Das System verwendet eine SQLite-Datenbank zur lokalen Speicherung von persistenten Nutzerdaten, insbesondere Portfolio-Transaktionen.

#### 4.6.2 BE-REQ-PERSIST-02 — Persistenter Speicherort

Die Datenbankdatei wird in einem betriebssystemkonformen Anwendungsdatenverzeichnis abgelegt, um Datenverlust bei Anwendungsneustarts zu verhindern.

#### 4.6.3 BE-REQ-PERSIST-03 — Automatische Initialisierung

Das System prüft beim Start die Existenz der Datenbank und initialisiert bei Bedarf das Schema (Tabellen) automatisch.

## 5. API-Governance

#### 5.1 AG-REQ-DEVMODE-01 — Bereitstellung eines DEV_MODE Standards

Das System muss standardmäßig im `DEV_MODE=True` (Mock-Modus) starten, um unkontrollierte externe API-Aufrufe zu verhindern.

#### 5.2 AG-REQ-WARN-01 — Warnung bei Aktivierung der Real-API

Das System muss beim Start explizit warnen, wenn der Modus für echte externe API-Aufrufe aktiviert ist.

#### 5.3 AG-REQ-PRIORITY-01 — Konfigurierbare KI-Provider-Hierarchie

Das System muss eine Priorisierung der KI-Provider (z. B. OpenAI vor Gemini) unterstützen.

#### 5.4 AG-REQ-CACHE-01 — Durchführung eines Cache Pre-Checks

Das System muss vor jedem KI-Aufruf prüfen, ob für die aktuelle Parameterkombination bereits ein valides Analyseergebnis im Cache vorliegt.

#### 5.5 AG-REQ-TOKEN-01 — Protokollierung des Token-Verbrauchs

Das System muss den Token-Verbrauch für jeden KI-Aufruf erfassen und protokollieren.

## 6. Datenverarbeitung (Data Handling)

#### 6.1 DH-REQ-REAL-01 — Durchführung internetbasierter Ticker-Auflösung

Im Real-Modus muss das System eine internetbasierte API (z. B. Yahoo Finance) zur Ticker-Auflösung nutzen.

#### 6.2 DH-REQ-FUZZY-01 — Implementierung fehlertoleranter Namensauflösung

Das System muss Abweichungen in der Schreibweise von Firmennamen bei der Ticker-Auflösung rechnerisch bewerten und tolerieren.

#### 6.3 DH-REQ-MAPPING-01 — Unterstützung von Name-zu-Symbol Mapping

Das System muss die Auflösung von Klartext-Firmennamen in kanonische Börsensymbole ermöglichen.

#### 6.4 DH-REQ-DEDUP-01 — Vermeidung paralleler identischer Anfragen

Das System muss sicherstellen, dass zeitgleiche identische Auflösungsanfragen de-dupliziert werden und nur eine externe Anfrage ausgelöst wird.

## 7. Nicht-funktionale Anforderungen

### 7.1 NFR-REQ-01 — Wahrnehmbare Reaktionsfähigkeit bei Cache-Treffern

Wenn Analyseergebnisse bereits vorliegen, muss die Benutzeroberfläche diese innerhalb von 2 Sekunden anzeigen.

### 7.2 NFR-REQ-02 — Explizite Ladeanzeige bei laufender Analyse

Während einer laufenden Analyse muss die Benutzeroberfläche einen klar erkennbaren Ladezustand darstellen.

### 7.3 NFR-REQ-03 — Explizite Fehlerrückmeldung

Bei Analyse- oder Datenfehlern muss die Benutzeroberfläche einen verständlichen Fehlerhinweis anzeigen.

### 7.4 NFR-REQ-04 — Wiederholbarkeit von Analyseaktionen

Nach einem Fehler muss der Nutzer die Analyse erneut auslösen können, ohne die Anwendung neu starten zu müssen.

### 7.5 NFR-REQ-05 — Sichtbare Datenherkunft

Für Analyseergebnisse muss die Benutzeroberfläche den Systemzustand `data_origin` sichtbar anzeigen (z. B. „extern bezogen“ vs. „KI-generiert“).

### 7.6 NFR-REQ-06 — Lesbarkeit umfangreicher Inhalte

Längere Analyseausgaben müssen scrollbar und strukturiert darstellbar sein.

### 7.7 NFR-REQ-07 — Zustandserhalt bei UI-Navigation

Beim Wechsel zwischen UI-Bereichen müssen gesetzte Kontextwerte erhalten bleiben.

### NFR-REQ-08 — CI‑Reproduzierbarkeit
Die CI muss ohne manuelle Setup‑Schritte reproduzierbar laufen; alle Test‑Dependencies müssen in der CI installierbar sein.

### NFR-REQ-09 — Test‑Determinismus
Tests müssen deterministisch ohne externe Dienste/Binaries laufen oder als Integrationstests markiert und getrennt ausführbar sein.

Ende des Lastenhefts