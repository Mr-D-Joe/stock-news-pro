# LASTENHEFT — Stock News Pro  
## Requirements Specification Document

**Version:** 1.1  
**Datum:** 2026-01-22  
**Status:** Draft  

---

## Änderungshistorie

| Version | Datum | Änderung | Beschreibung |
|--------|-------|----------|--------------|
| 1.0 | 2026-01-22 | Initialfassung | Erste vollständige Lastenheft-Version |
| 1.1 | 2026-01-22 | Struktur-Refactoring | Auflösung tabellarischer Anforderungen in abschnittsbasierte, RE-konforme Struktur. Entfernung von Implementierungsstatus. Ergänzung formaler Governance- und Konfliktregeln. |

---

## Arbeitsübersicht – Identifizierte Anforderungen (nicht normativ)

> Diese Tabelle dient ausschließlich als Änderungs-, Arbeits- und Migrationsübersicht.  
> **Maßgeblich und bindend sind ausschließlich die normativen Anforderungsabschnitte im Dokument.**

### UI-Anforderungen (Frontend)

| Referenz | Kurzbeschreibung |
|--------|------------------|
| F-UI-01 | Dashboard mit Marktübersicht |
| F-UI-02 | Ticker-Eingabe mit Fehlertoleranz |
| F-UI-03 | Sektor-Auswahl |
| F-UI-04 | Sprachumschaltung |
| F-UI-05 | Zeitraumauswahl |
| F-UI-06 | Nachrichtenanzeige |
| F-UI-07 | Executive Summary |
| F-UI-08 | Preis-Chart |
| F-UI-09 | KI-Analyseausgabe |
| F-UI-10 | Analyse-Scope |
| F-UI-11 | Volumen-Chart |

### Backend-Anforderungen (AI Service)

| Referenz | Kurzbeschreibung |
|--------|------------------|
| F-BE-01 | Ticker-Auflösung |
| F-BE-02 | Fundamentaldaten |
| F-BE-03 | Historische Preisdaten |
| F-BE-04 | Nachrichtenaggregation |
| F-BE-05 | KI-Analyse & Bericht |

### Desktop / Governance / Data Handling

| Referenz | Kurzbeschreibung |
|--------|------------------|
| F-TA-01 | Native Desktop-App |
| F-TA-02 | Backend-Prozesssteuerung |
| F-AG-01 | DEV_MODE |
| F-AG-02 | Provider-Priorisierung |
| F-DH-01 | Internetbasierte Ticker-Auflösung |
| F-DH-02 | Fehlertolerante Auflösung |
| F-DH-03 | Name → Symbol |
| F-DH-04 | In-Flight De-Duplizierung |

---

## 1. Projektübersicht

### 1.1 Projektname

Stock News Pro — AI-powered Financial Intelligence Dashboard

---

### 1.2 Projektziel

Ziel des Projekts **Stock News Pro** ist die Entwicklung einer modularen, desktopbasierten Softwareplattform zur KI-gestützten Analyse von Finanzmärkten, Aktien und Sektoren.

Die Plattform dient der strukturierten Aufbereitung, Analyse und Interpretation finanzrelevanter Daten sowie der unterstützenden Generierung von Analyseberichten und Zusammenfassungen.

Darüber hinaus schafft Stock News Pro eine technische und konzeptionelle Basis für funktionale Erweiterungen innerhalb des Finanzanalyse- und Entscheidungsunterstützungsdomänen.

Das Projektziel ist verbindlich und bildet die fachliche Grundlage für alle weiteren Anforderungen dieses Lastenhefts.

---

### 1.3 Zielgruppe

Stock News Pro richtet sich an Nutzer, die finanzielle Informationen strukturiert analysieren und für fundierte Entscheidungen nutzen möchten.

Die primäre Zielgruppe umfasst:

- Privatanleger  
- Finanzanalysten  
- Investment-Berater  

Alle Anforderungen dieses Lastenhefts sind an den Bedürfnissen dieser Zielgruppen auszurichten.

---

## 2. Funktionale Anforderungen

Alle funktionalen Anforderungen sind lösungsneutral, eindeutig formuliert und überprüfbar.  
Sie sind verbindlich umzusetzen, sofern sie nicht im Widerspruch zu **DESIGN.md** stehen.

---

### 2.1 Benutzeroberfläche (Frontend)

Die Benutzeroberfläche stellt die Interaktionsschicht zwischen Nutzer und System dar.

Sie ist verantwortlich für die strukturierte Darstellung von Informationen, die kontrollierte Auslösung von Analyseprozessen sowie die transparente Abbildung des aktuellen System- und Analysezustands.

Die Benutzeroberfläche ist strikt von Geschäftslogik, Datenbeschaffung und Entscheidungslogik getrennt.  
Alle fachlichen Operationen erfolgen ausschließlich über definierte Service- und State-Schnittstellen gemäß **DESIGN.md**.

---

#### 2.1.1 Dashboard mit Marktübersicht (F-UI-01)

**Typ:** Funktionale Anforderung  
**Priorität:** MUSS  

_Beschreibung folgt._

---

#### 2.1.2 Ticker-Eingabe mit Fehlertoleranz (F-UI-02)

**Typ:** Funktionale Anforderung  
**Priorität:** MUSS  

_Beschreibung folgt._

---

<!-- weitere Anforderungen folgen analog -->

---

## 7. Dokumenten-Hierarchie und Governance

1. **DESIGN.md** — Bindende Architektur- und Governance-Konstitution  
2. **LASTENHEFT.md** — Anforderungsdokumentation  
3. **SYSTEM_REPORT.md** — Deskriptives Audit- und Statusformat  
4. **README.md** — Orientierung und Einstieg  

### Konfliktauflösung

- **DESIGN.md hat immer Vorrang.**
- Anforderungen sind anzupassen, nicht die Architektur.
- Konflikte sind explizit zu dokumentieren.

---

**Ende des Lastenhefts**