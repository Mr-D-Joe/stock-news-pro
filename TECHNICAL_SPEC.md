# TECHNICAL_SPEC — Stock News Pro
## Implementation-Level Specification

Version: 1.2  
Datum: 2026-01-28  
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

### 2.3 Sparkline & Mini-Charts

#### 2.3.1 TECH-SPEC-SPARK-01 — SVG Path Rendering

Die Sparkline-Komponente berechnet einen SVG-Pfad auf Basis von normalisierten Datenpunkten. Die Skalierung erfolgt über eine lineare Abbildung (Linear Mapping) des Wertebereichs [min, max] auf die Viewbox-Koordinaten.

#### 2.3.2 TECH-SPEC-SPARK-02 — Trend-Indikation Logik

Die Trendfarbe wird durch den Vergleich des ersten und letzten Datenpunktes der Sparkline bestimmt. Differenzen > 0 werden als `text-emerald-500` (Emerald-Sättigung 500) gerendert.

### 2.4 Heatmap Treemap Logic

#### 2.4.1 TECH-SPEC-HEATMAP-01 — Recharts Treemap Integration

Die Heatmap nutzt die `Treemap`-Komponente von Recharts. Die Hierarchie wird über das `data`-Attribut abgebildet, wobei die Sektoren als Root-Knoten und Aktien als Blatt-Knoten fungieren.

#### 2.4.2 TECH-SPEC-HEATMAP-02 — Performance Color Mapping

Die Hintergrundfarbe der Sektorkacheln wird über eine HSL-basierte Sättigungsfunktion gesteuert. Positive Performance (Sektor) führt zu grünen Farbtönen, negative zu roten. Der Sättigungsgrad entspricht dem Betrag der Performance im Intervall [0%, 5%].

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
