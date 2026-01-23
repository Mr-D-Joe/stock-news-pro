# LASTENHEFT — Stock News Pro
## Requirements Specification Document

Version: 1.1  
Datum: 2026-01-22  
Status: Draft  

## Änderungshistorie

| Version | Datum       | Abschnitt | Änderungstyp | Beschreibung |
|--------:|------------|-----------|--------------|--------------|
| 1.1 | 2026-01-22 | 2.4 | Anforderungsauflösung | Auflösung der Sammelanforderung F-UI-04 in atomare Anforderungen zur Sprachumschaltung |
| 1.1 | 2026-01-22 | 2.4 | Anforderungserweiterung | Einführung atomarer UI-Anforderungen für Sprachwahl, Kontextführung und Sprachwechsel |
| 1.1 | 2026-01-22 | 2.4 | Präzisierung | Sprachliche Präzisierung und Vereinzelung der UI-REQ-LANG-Anforderungen gemäß RE-BASE- und RE-CTX-Regeln |
| 1.1 | 2026-01-22 | 2.3 | Anforderungsauflösung | Auflösung der Sammelanforderung F-UI-03 in atomare Anforderungen zur Sektorauswahl |
| 1.1 | 2026-01-22 | 2.3 | Anforderungserweiterung | Einführung atomarer UI-Anforderungen für Sektorauswahl, Kontextführung und Rücksetzen |
| 1.1 | 2026-01-22 | 2.3 | Präzisierung | Sprachliche Präzisierung und Vereinzelung der UI-REQ-SECTORSEL-Anforderungen gemäß RE-BASE- und RE-CTX-Regeln |
| 1.1 | 2026-01-22 | 2.2 | Anforderungsauflösung | Auflösung der Sammelanforderung F-UI-02 in atomare Anforderungen zur Aktienauswahl mit fehlertoleranter Eingabe |
| 1.1 | 2026-01-22 | 2.2 | Anforderungserweiterung | Einführung atomarer UI-Anforderungen für Texteingabe, Normalisierung, Auflösung, Mehrdeutigkeit und Fehlerbehandlung |
| 1.1 | 2026-01-22 | 2.2 | Präzisierung | Sprachliche Präzisierung und Vereinheitlichung der UI-REQ-STOCKSEL-Anforderungen gemäß RE-BASE- und RE-CTX-Regeln |
| 1.1 | 2026-01-22 | 1.5 | Dokumentationsstruktur | Einführung eines eigenständigen Abschnitts für verpflichtende Dokumentationsartefakte (System Report, README) |
| 1.1 | 2026-01-22 | 1.4 | Regelergänzung | Ergänzung von RE-STRUCT-03 zur einheitlichen Anforderungsformatierung ohne Trennzeichen |
| 1.1 | 2026-01-22 | 1.4 | Regelkonsolidierung | Bereinigung und Vereinzelung der formalen RE-Regeln ohne Doppelungen oder Negierungen |
| 1.1 | 2026-01-22 | 1.4 | Regelergänzung | Einführung der Klassifikation generischer und spezialisierter Kontextanforderungen (RE-CTX-01 bis RE-CTX-03) |
| 1.1 | 2026-01-22 | 1.4 | Regelergänzung | Einführung der Klassifikation generischer und spezialisierter Zustandsanforderungen (RE-STATE-01 bis RE-STATE-03) |
| 1.1 | 2026-01-22 | 1.4 | Regelergänzung | Einführung der Klassifikation generischer und spezialisierter Abhängigkeitsanforderungen sowie expliziter Semantikpflicht (RE-LINK-01 bis RE-LINK-04) |
| 1.1 | 2026-01-22 | 2.1 | Anforderungsauflösung | Auflösung der Sammelanforderung F-UI-01 in atomare Dashboard-Anforderungen UI-REQ-DASH-01 bis UI-REQ-DASH-08 |
| 1.1 | 2026-01-22 | 2.1 | Anforderungserweiterung | Einführung atomarer UI-Kontextanforderungen UI-REQ-CTX-01 bis UI-REQ-CTX-09 |
| 1.1 | 2026-01-22 | 2.1 | Anforderungserweiterung | Einführung atomarer UI-Zustandsanforderungen UI-REQ-STATE-01 bis UI-REQ-STATE-05 |
| 1.1 | 2026-01-22 | 2.1 | Anforderungserweiterung | Einführung atomarer UI-Abhängigkeitsanforderungen UI-REQ-LINK-01 bis UI-REQ-LINK-03 |
| 1.1 | 2026-01-22 | 2.1 | Präzisierung | Vereinheitlichung und sprachliche Präzisierung der UI-REQ-DASH-, UI-REQ-CTX- und UI-REQ-STATE-Anforderungen |
| 1.1 | 2026-01-22 | 2 | Struktur-Refactoring | Umstellung von tabellarischen Sammelanforderungen auf abschnittsbasierte, atomare Einzelanforderungen |
| 1.1 | 2026-01-22 | 7 | Strukturänderung | Entfernung von Kapitel 7 und Überführung relevanter Governance-Regeln in Abschnitt 1.4 |
| 1.1 | 2026-01-22 | Gesamt | Governance-Anpassung | Entfernung von Implementierungsstatus und Systemzustand aus dem Lastenheft |
| 1.0 | 2026-01-22 | Gesamt | Initialfassung | Erste Version des Lastenhefts mit tabellarischen Sammelanforderungen |

## ID-Zuordnung – Auflösung von Sammelanforderungen (nicht normativ)

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
|| ~~F-UI-04~~ | ~~Sprachumschaltung (aufgelöst)~~ |
| F-UI-05 | Zeitraumauswahl |
| F-UI-06 | Nachrichtenanzeige |
| F-UI-07 | Executive Summary |
| F-UI-08 | Preis-Chart |
| F-UI-09 | KI-Analyseausgabe |
| F-UI-10 | Analyse-Scope |
| F-UI-11 | Volumen-Chart |

### Backend (AI Service)

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

### 1.4 Formale Regeln zur Anforderungsspezifikation

#### 1.4.1 RE-BASE-01 — Atomare Anforderung

Jede Anforderung beschreibt genau eine fachliche oder technische Eigenschaft.

#### 1.4.2 RE-BASE-02 — Eigenständige Verifizierbarkeit

Jede Anforderung ist unabhängig prüfbar und eindeutig verifizierbar.

#### 1.4.3 RE-BASE-03 — Eigener Anforderungsabschnitt

Jede Anforderung ist als eigener Abschnitt formuliert.

#### 1.4.4 RE-BASE-04 — Eindeutige Anforderungs-ID

Jede Anforderung besitzt eine eindeutige Anforderungs-ID.

#### 1.4.5 RE-STRUCT-01 — Abschnittsbasierte Strukturierung

Anforderungen werden ausschließlich über Abschnittsnummerierung und Überschriften strukturiert.

#### 1.4.6 RE-STRUCT-02 — Einheitliches Überschriftenformat

Jede Anforderung verwendet das Überschriftenformat  
<Abschnittsnummer> <Anforderungs-ID> — <Kurzbezeichnung>

#### 1.4.7 RE-STRUCT-03 — Verzicht auf Trennzeichen zwischen Anforderungen

Zwischen Anforderungen werden keine Trennlinien, dekorativen Markierungen oder Sonderzeichen verwendet.

#### 1.4.8 RE-SCOPE-01 — Lösungsneutrale Formulierung

Anforderungen sind lösungsneutral formuliert.

#### 1.4.9 RE-TRACE-01 — Explizite Anforderungsauflösung

Die Auflösung einer Anforderung in mehrere Anforderungen wird explizit dokumentiert.

#### 1.4.10 RE-TRACE-02 — Eindeutige ID-Zuordnung bei Auflösung

Jede aus einer Anforderungsauflösung hervorgehende Anforderung referenziert eindeutig die ursprüngliche Anforderungs-ID.

#### 1.4.11 RE-TRACE-03 — Tabellarische ID-Zuordnung

Die Zuordnung zwischen ursprünglicher Anforderungs-ID und neuen Anforderungs-IDs erfolgt tabellarisch.

#### 1.4.12 RE-TRACE-04 — Platzierung der ID-Zuordnung

Die tabellarische ID-Zuordnung ist Bestandteil der Änderungshistorie.

#### 1.4.13 RE-GOV-01 — Architekturkonforme Anforderungserstellung

Anforderungen werden gemäß den in DESIGN.md definierten architektonischen und governancebezogenen Vorgaben erstellt.

#### 1.4.14 RE-CTX-01 — Klassifikation von Kontextanforderungen

Kontextanforderungen werden entweder als generische Kontextanforderungen oder als spezialisierte Kontextanforderungen formuliert.

#### 1.4.15 RE-CTX-02 — Definition generischer Kontextanforderungen

Generische Kontextanforderungen beschreiben ausschließlich die Fähigkeit der Benutzeroberfläche, mehrere Kontextwerte gleichzeitig zu führen, zu synchronisieren oder konsistent zu halten.

#### 1.4.16 RE-CTX-03 — Definition spezialisierter Kontextanforderungen

Spezialisierte Kontextanforderungen beschreiben konkrete fachliche Kontextwerte mit expliziter Semantik, wie Analyseobjekte, Zustände oder Abhängigkeiten.

#### 1.4.17 RE-STATE-01 — Klassifikation von Zustandsanforderungen

Zustandsanforderungen werden entweder als generische Zustandsanforderungen oder als spezialisierte Zustandsanforderungen formuliert.

#### 1.4.18 RE-STATE-02 — Definition generischer Zustandsanforderungen

Generische Zustandsanforderungen beschreiben ausschließlich die Fähigkeit der Benutzeroberfläche, Zustände unabhängig von ihrer fachlichen Bedeutung zu führen, zu synchronisieren oder konsistent zu halten.

#### 1.4.19 RE-STATE-03 — Definition spezialisierter Zustandsanforderungen

Spezialisierte Zustandsanforderungen beschreiben konkrete fachliche Zustände mit expliziter Semantik, die den Zustand des Systems oder seiner Analyseergebnisse abbilden.

#### 1.4.20 RE-LINK-01 — Klassifikation von Abhängigkeitsanforderungen

Abhängigkeitsanforderungen werden entweder als generische Abhängigkeitsanforderungen oder als spezialisierte Abhängigkeitsanforderungen formuliert.

#### 1.4.21 RE-LINK-02 — Definition generischer Abhängigkeitsanforderungen

Generische Abhängigkeitsanforderungen beschreiben ausschließlich die Fähigkeit der Benutzeroberfläche, Beziehungen zwischen Kontext- oder Zustandswerten unabhängig von ihrer fachlichen Bedeutung zu führen, zu synchronisieren oder konsistent zu halten.

#### 1.4.22 RE-LINK-03 — Definition spezialisierter Abhängigkeitsanforderungen

Spezialisierte Abhängigkeitsanforderungen beschreiben konkrete fachliche Abhängigkeiten mit expliziter Semantik, die fachliche Abhängigkeiten zwischen Analyseobjekten, Kontextwerten oder Analyseergebnissen abbilden.

#### 1.4.23 RE-LINK-04 — Explizite Formulierung fachlicher Abhängigkeiten

Fachliche Abhängigkeiten werden ausschließlich durch spezialisierte Abhängigkeitsanforderungen mit expliziter Semantik beschrieben.

### 1.5 Dokumentationsartefakte

#### 1.5.1 DOC-ART-01 — System Report

Für jede umgesetzte Version des Systems wird ein SYSTEM_REPORT.md gemäß der in DESIGN.md definierten Struktur erstellt.

#### 1.5.2 DOC-ART-02 — README

Für das Projekt wird eine README.md geführt, die Zweck, Einstieg und grundlegende Nutzung des Systems beschreibt.

## 2. Funktionale Anforderungen

### 2.1 Benutzeroberfläche (Frontend)

Die Benutzeroberfläche stellt die Interaktionsschicht zwischen Nutzer und System dar.

#### 2.1.1 UI-REQ-DASH-01 — Bereitstellung eines Dashboard-Containers

Das System muss einen Dashboard-Container bereitstellen, der als primäre strukturelle Einheit der Benutzeroberfläche fungiert.

#### 2.1.2 UI-REQ-DASH-02 — Initialisierbarkeit des Dashboard-Containers

Der Dashboard-Container muss initialisierbar sein, ohne dass Inhalte, Daten oder Analyseergebnisse vorliegen.

#### 2.1.3 UI-REQ-DASH-03 — Aufnahme mehrerer UI-Elemente

Der Dashboard-Container muss die gleichzeitige Aufnahme mehrerer UI-Elemente ermöglichen.

#### 2.1.4 UI-REQ-DASH-04 — Dynamische Erweiterbarkeit

Der Dashboard-Container muss die dynamische Hinzufügung weiterer UI-Elemente zur Laufzeit ermöglichen.

#### 2.1.5 UI-REQ-DASH-05 — Inhaltsunabhängige Struktur

Der Dashboard-Container muss unabhängig vom fachlichen Inhalt der enthaltenen UI-Elemente funktionieren.

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

#### 2.1.11 UI-REQ-CTX-03 — UI-Kontext: Analyse-Scope

Die Benutzeroberfläche muss einen Kontextwert analysis_scope führen.

#### 2.1.12 UI-REQ-CTX-04 — UI-Kontext: Sprache

Die Benutzeroberfläche muss einen Kontextwert language führen.

#### 2.1.13 UI-REQ-CTX-05 — UI-Kontext: Zeitraum

Die Benutzeroberfläche muss einen Kontextwert time_range führen.

#### 2.1.14 UI-REQ-CTX-06 — UI-Kontext: Thematische Suchanfrage

Die Benutzeroberfläche muss einen Kontextwert theme_query führen.

#### 2.1.15 UI-REQ-CTX-07 — Gleichzeitige Kontextführung

Die Benutzeroberfläche muss alle definierten Kontextwerte gleichzeitig führen können.

#### 2.1.16 UI-REQ-CTX-08 — Leerer Kontextzustand Aktie

Die Benutzeroberfläche muss einen gültigen Zustand ohne gesetzten selected_stock unterstützen.

#### 2.1.17 UI-REQ-CTX-09 — Leerer Kontextzustand Sektor

Die Benutzeroberfläche muss einen gültigen Zustand ohne gesetzten selected_sector unterstützen.

#### 2.1.18 UI-REQ-STATE-01 — Analysezustand

Die Benutzeroberfläche muss einen Kontextwert analysis_status führen.

#### 2.1.19 UI-REQ-STATE-02 — Fehlerzustand

Die Benutzeroberfläche muss einen Kontextwert error_state führen.

#### 2.1.20 UI-REQ-STATE-03 — Datenherkunft

Die Benutzeroberfläche muss einen Kontextwert data_origin führen.

#### 2.1.21 UI-REQ-STATE-04 — Generiert-Kennzeichnung

Die Benutzeroberfläche muss einen Kontextwert generated_flag führen.

#### 2.1.22 UI-REQ-STATE-05 — Aktualität

Die Benutzeroberfläche muss einen Kontextwert fetched_at führen.

#### 2.1.23 UI-REQ-LINK-01 — Abhängigkeit Aktie → Sektor

Wenn selected_stock gesetzt wird und ein zugehöriger Sektor vorliegt, muss selected_sector aktualisiert werden.

#### 2.1.24 UI-REQ-LINK-02 — Abhängigkeit bei Sektorwechsel

Wenn selected_stock gesetzt ist und selected_sector geändert wird, müssen beide Kontextwerte gültig bleiben.

#### 2.1.25 UI-REQ-LINK-03 — Scope-Steuerung

Die Benutzeroberfläche muss Analyseauslösung und Darstellung anhand von analysis_scope steuern.

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

#### 2.2.7 UI-REQ-STOCKSEL-07 — Kontextwert für Auflösungsstatus

Die Benutzeroberfläche führt einen Kontextwert `stock_resolution_status`, der den aktuellen Status der Auflösung von `stock_query` repräsentiert.

#### 2.2.8 UI-REQ-STOCKSEL-08 — Setzen des Analyseobjekts bei erfolgreicher Auflösung

Bei erfolgreicher Auflösung von `stock_query` setzt die Benutzeroberfläche den Kontextwert `selected_stock` auf das aufgelöste Analyseobjekt.

#### 2.2.9 UI-REQ-STOCKSEL-09 — Kontextwert für Mehrdeutigkeitskandidaten

Die Benutzeroberfläche führt einen Kontextwert `stock_resolution_candidates`, der die Kandidatenliste bei mehrdeutiger Auflösung von `stock_query` repräsentiert.

#### 2.2.10 UI-REQ-STOCKSEL-10 — Übernahme eines Kandidaten als Analyseobjekt

Wenn ein Kandidat aus `stock_resolution_candidates` ausgewählt wird, setzt die Benutzeroberfläche den Kontextwert `selected_stock` auf das ausgewählte Analyseobjekt.

#### 2.2.11 UI-REQ-STOCKSEL-11 — Abbildung eines Auflösungsfehlers als Fehlerzustand

Wenn die Auflösung von `stock_query` fehlschlägt, setzt die Benutzeroberfläche den Kontextwert `error_state` auf einen zur Auflösung gehörenden Fehlerzustand.

#### 2.2.12 UI-REQ-STOCKSEL-12 — Rücksetzen der Aktienauswahl

Die Benutzeroberfläche unterstützt eine Nutzeraktion, die `selected_stock` in den Zustand „nicht gesetzt“ überführt.

## 2.3 Analyseobjekt-Auswahl Sektor (F-UI-03)

### 2.3.1 UI-REQ-SECTORSEL-01 — Bereitstellung einer Interaktionsmöglichkeit zur Sektorauswahl

Die Benutzeroberfläche stellt eine Interaktionsmöglichkeit zur Auswahl eines Sektors bereit.

### 2.3.2 UI-REQ-SECTORSEL-02 — Kontextwert für ausgewählten Sektor

Die Benutzeroberfläche führt einen Kontextwert `selected_sector`, der den aktuell ausgewählten Sektor repräsentiert.

### 2.3.3 UI-REQ-SECTORSEL-03 — Anzeige verfügbarer Sektoren

Die Benutzeroberfläche stellt eine Menge verfügbarer Sektoren zur Auswahl bereit.

### 2.3.4 UI-REQ-SECTORSEL-04 — Auswahl eines einzelnen Sektors

Die Benutzeroberfläche unterstützt die Auswahl eines einzelnen Sektors aus der bereitgestellten Sektormenge.

### 2.3.5 UI-REQ-SECTORSEL-05 — Setzen des Sektorkontexts bei Auswahl

Bei Auswahl eines Sektors setzt die Benutzeroberfläche den Kontextwert `selected_sector` auf den ausgewählten Sektor.

### 2.3.6 UI-REQ-SECTORSEL-06 — Wechsel des ausgewählten Sektors

Die Benutzeroberfläche unterstützt den Wechsel des aktuell gesetzten Sektors durch erneute Auswahl.

### 2.3.7 UI-REQ-SECTORSEL-07 — Kontextzustand ohne gesetzten Sektor

Die Benutzeroberfläche unterstützt einen gültigen Zustand, in dem kein Sektor ausgewählt ist.

### 2.3.8 UI-REQ-SECTORSEL-08 — Rücksetzen der Sektorauswahl

Die Benutzeroberfläche unterstützt eine Nutzeraktion, die den Kontextwert `selected_sector` in den Zustand „nicht gesetzt“ überführt.

## 2.4 Sprachumschaltung (F-UI-04)

### 2.4.1 UI-REQ-LANG-01 — Bereitstellung einer Interaktionsmöglichkeit zur Sprachumschaltung

Die Benutzeroberfläche stellt eine Interaktionsmöglichkeit bereit, über die Nutzer die Anzeigesprache auswählen können.

### 2.4.2 UI-REQ-LANG-02 — Kontextwert für aktuelle Sprache

Die Benutzeroberfläche führt einen Kontextwert `language`, der die aktuell aktive Anzeigesprache repräsentiert.

### 2.4.3 UI-REQ-LANG-03 — Bereitstellung verfügbarer Sprachen

Die Benutzeroberfläche stellt eine Menge verfügbarer Sprachen zur Auswahl bereit.

### 2.4.4 UI-REQ-LANG-04 — Auswahl einer einzelnen Sprache

Die Benutzeroberfläche unterstützt die Auswahl genau einer Sprache aus der bereitgestellten Sprachmenge.

### 2.4.5 UI-REQ-LANG-05 — Setzen des Sprachkontexts bei Auswahl

Bei Auswahl einer Sprache setzt die Benutzeroberfläche den Kontextwert `language` auf die ausgewählte Sprache.

### 2.4.6 UI-REQ-LANG-06 — Wechsel der aktiven Sprache

Die Benutzeroberfläche unterstützt den Wechsel der aktuell gesetzten Sprache durch erneute Auswahl.

### 2.4.7 UI-REQ-LANG-07 — Gültiger Kontextzustand der Sprache

Die Benutzeroberfläche unterstützt einen gültigen Zustand, in dem der Kontextwert `language` gesetzt ist.



Ende des Lastenhefts