# STYLEGUIDE — Stock News Pro
## Visual Standards and Design Tokens

Version: 1.0  
Datum: 2026-01-24  
Status: Active

---

## 1. Design Tokens (Farbatlas)

### 1.1 Primärfarben

#### 1.1.1 STYLE-SPEC-TOKEN-01 — Definition der Primärfarbe Slate-900

Die Farbe Slate-900 (#0f172a) dient als primärer Hintergrund für App-Container und Header.

#### 1.1.2 STYLE-SPEC-TOKEN-02 — Definition der Akzentfarbe Blue-500

Die Farbe Blue-500 (#3b82f6) dient als Akzentfarbe für interaktive Elemente, Icons und Primäraktionen.

### 1.2 Statusfarben

#### 1.2.1 STYLE-SPEC-TOKEN-03 — Definition der Erfolgsfarbe Emerald-500

Die Farbe Emerald-500 wird zur Signalisierung positiver Kursentwicklungen und erfolgreicher Systemzustände verwendet.

#### 1.2.2 STYLE-SPEC-TOKEN-04 — Definition der Fehlerfarbe Rose-500

Die Farbe Rose-500 wird zur Signalisierung negativer Kursentwicklungen und kritischer Fehlerzustände verwendet.

---

## 2. Typografie

### 2.1 Schriftarten

#### 2.1.1 STYLE-SPEC-TYPO-01 — Standard-Schriftfamilie Sans

Als primäre Schriftart wird ein Sans-Interface-Stack (Inter, system-ui, sans-serif) verwendet.

#### 2.1.2 STYLE-SPEC-TYPO-02 — Schriftart für Datenanzeige

Für die Anzeige von numerischen Kurswerten und Finanzdaten wird eine monospaced Schriftart (JetBrains Mono, UI-Monospace) verwendet.

---

## 3. Komponentendesign

### 3.1 Karten-Container

#### 3.1.1 STYLE-SPEC-UI-01 — Standard Eckenradius

Alle Dashboard-Karten verfügen über einen einheitlichen Eckenradius von 0.75rem (rounded-xl).

#### 3.1.2 STYLE-SPEC-UI-02 — Schatten-Definition

Karten im Dashboard werden mit einem subtilen Schatten (shadow-sm) und einer feinen Randlinie (border-slate-200) visualisiert.

### 3.2 Micro-Interaktionen

#### 3.2.1 STYLE-SPEC-UI-03 — Hover-Effekt für interaktive Karten

Interaktive Karten reagieren auf Nutzerinteraktion mit einer leichten Schattenintensivierung (hover:shadow-md) und sanfter Skalierung (transition-all).
