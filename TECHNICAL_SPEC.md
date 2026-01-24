# TECHNICAL_SPEC — Stock News Pro
## Implementation-Level Specification

Version: 1.1  
Datum: 2026-01-24  
Status: Active

---

## 1. Mock Data Strategy (Demo Mode)

### 1.1 Predefined Equity Entities

#### 1.1.1 TECH-SPEC-MOCK-01 — Konfiguration der Mock-Aktie ACME

Das System konfiguriert die Mock-Aktie ACME Corp (Symbol: ACME) im Sektor „Technology“ für den Demo-Modus.

#### 1.1.2 TECH-SPEC-MOCK-02 — Konfiguration der Mock-Aktie BioGenix

Das System konfiguriert die Mock-Aktie BioGenix (Symbol: BGNX) im Sektor „Healthcare“ für den Demo-Modus.

#### 1.1.3 TECH-SPEC-MOCK-03 — Konfiguration der Mock-Aktie Novo Nordisk

Das System konfiguriert die Mock-Aktie Novo Nordisk (Symbol: NVO) im Sektor „Healthcare“ für den Demo-Modus.

#### 1.1.4 TECH-SPEC-MOCK-04 — Konfiguration der Mock-Aktie Eli Lilly

Das System konfiguriert die Mock-Aktie Eli Lilly (Symbol: LLY) im Sektor „Healthcare“ für den Demo-Modus.

### 1.2 Fallback-Generator Logic

#### 1.2.1 TECH-SPEC-FALLBACK-01 — Generierung sicherer Fallback-Reports

Für Ticker, die nicht in der Mock-Liste enthalten sind, generiert das System einen strukturell validen, aber generisch markierten Analysebericht.

---

## 2. Dashboard Layout Fine-Tuning

### 2.1 Spalten-Proportionen

#### 2.1.1 TECH-SPEC-LAYOUT-01 — Spaltenbreite Market Overview

Die linke Spalte (Market Overview) belegt im XL-Layout eine Breite von 41,6 % (5 von 12 Gridschlitzen).

#### 2.1.2 TECH-SPEC-LAYOUT-02 — Spaltenbreite Monitor & AI

Die rechte Spalte (Monitor & AI) belegt im XL-Layout eine Breite von 58,3 % (7 von 12 Gridschlitzen).

### 2.2 Timeframe Slicing

#### 2.2.1 TECH-SPEC-CHART-01 — Granularität für 1Y-Ansicht

Die 1Y-Ansicht im Chart-Slicing Hook aggregiert Daten auf Basis von 252 Handelstagen.

#### 2.2.2 TECH-SPEC-CHART-02 — Granularität für 24H-Ansicht

Die 24H-Ansicht im Chart-Slicing Hook präsentiert Daten in einer Granularität von 15-Minuten-Intervallen.

---

## 3. Technische Fallbacks

### 3.1 AI Service Verfügbarkeit

#### 3.1.1 TECH-SPEC-ERROR-01 — Behandlung von IPC-Verbindungsfehlern

Bei Nichterreichbarkeit des Backend-Sidecars über IPC setzt die Benutzeroberfläche den Fehlerzustand auf SERVICE_UNAVAILABLE.

#### 3.1.2 TECH-SPEC-ERROR-02 — Visualisierung des Verbindungsfehlers

Ein Verbindungsfehler wird dem Nutzer über ein Warn-Banner in der Statusleiste signalisiert.

### 3.2 Cache-Verwaltung

#### 3.2.1 TECH-SPEC-CACHE-01 — Invalidierung bei Sprachwechsel

Der Analyse-Cache wird bei einer Änderung des Kontextwerts „language“ vollständig invalidiert.

#### 3.2.2 TECH-SPEC-CACHE-02 — Persistenz über Zeitrahmenwechsel

Analyseergebnisse bleiben bei einem Wechsel des Kontextwerts „time_range“ im Cache erhalten (Compound-Key Nutzung).
