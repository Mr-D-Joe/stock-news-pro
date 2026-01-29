# DESIGN.md — Project Constitution
# Stock News Pro

⚠️ THIS DOCUMENT IS NORMATIVE AND BINDING

Version: 1.3  
Datum: 2026-01-27  
Status: Draft  

Dieses Dokument definiert die verbindlichen Regeln für Architektur, Governance und Implementierung des Systems.

---

## Änderungshistorie

| Version | Datum       | Abschnitt | Änderungstyp | Beschreibung |
|--------:|------------|-----------|--------------|--------------|
| 1.4 | 2026-01-29 | Governance | Erweiterung | Einführung der CI-/Typing-/Test-Determinismus-Regeln (DES-GOV-49 bis DES-GOV-53). |
| 1.3 | 2026-01-27 | Governance | Erweiterung | Übernahme der formalen Anforderungsregeln (Atomarisierung, Verifizierbarkeit, Struktur) als projektverbindliche Governance in DESIGN.md |
| 1.3 | 2026-01-27 | Governance | Erweiterung | Übernahme des Änderungs- und Erweiterungsprozesses für externe Änderungswünsche als normative Governance in DESIGN.md |
| 1.3 | 2026-01-27 | Governance | Erweiterung | Übernahme der Governance zur Interpretation und normativen Autorität als normative Governance in DESIGN.md |
| 1.3 | 2026-01-27 | Governance | Erweiterung | Übernahme der Dokumentationsartefakte (SYSTEM_REPORT, README, TECHNICAL_SPEC, STYLEGUIDE, PROMPTS) als Dokumenten-Governance in DESIGN.md |
| 1.3 | 2026-01-27 | Architektur | Erweiterung | Übernahme der Desktop-Integration (native Desktop-App, Backend-Lifecycle, typisierte IPC) als Architektur-Requirements in DESIGN.md |
| 1.3 | 2026-01-27 | Governance | Erweiterung | Einfügung der Governance-Regel DES-GOV-48 zur verpflichtenden Pflege von CHANGELOG.md |
| 1.3 | 2026-01-27 | Architektur / LLM | Erweiterung | Übernahme der API- und LLM-Governance (Mock/Real-Modus, Warnung, Provider-Priorisierung, Cache-Precheck, Token-Telemetrie) als normative Regeln in DESIGN.md |
| 1.2 | 2026-01-27 | Governance / LLM | Entkopplung | Auflösung der inhaltlichen Überlappung zwischen deterministischer Aufgabenlösung (DES-GOV-09) und LLM-Aufrufkriterium (DES-LLM-07) durch eindeutige Zuständigkeiten je Requirement |
| 1.2 | 2026-01-27 | Frontend | Präzisierung | Klare Trennung von Render-Ökonomie (DES-FE-08) und Rendering-Strategie (DES-FE-20) |
| 1.2 | 2026-01-27 | Governance | Erweiterung | Ergänzung einer Sanitization-Trace-Anforderung (DES-GOV-27) zur nachvollziehbaren Sanitization pro gerendertem Output |
| 1.1 | 2026-01-27 | Governance | Präzisierung | Schärfung der Vorrangregel und positive Formulierung normativer vs. informativer Artefakte |
| 1.1 | 2026-01-27 | Governance | Regelkonformität | Reduktion von Mehrfachinhalten pro Requirement durch Trennung von Dokumenthierarchie (informativ) und normativen Regeln |
| 1.1 | 2026-01-27 | Backend | Konsolidierung | Konsolidierung überlappender API-Requirements zu expliziten Ergebnis- und Kennzeichnungsfeldern |
| 1.0 | 2026-01-27 | Gesamt | Initialisierung | Transformation der ursprünglichen Prosa-Verfassung in atomare Design-Requirements (DES-*) |
| 1.0 | 2026-01-27 | Gesamt | Struktur | Einführung der Requirement-Typen DES-GOV, DES-ARCH, DES-FE, DES-BE, DES-LLM |
| 1.0 | 2026-01-27 | Governance | Erweiterung | Einführung der normativen Governance-Anforderungen DES-GOV-01 bis DES-GOV-26 |
| 1.0 | 2026-01-27 | Architektur | Präzisierung | Atomarisierung der Architekturprinzipien DES-ARCH-01 bis DES-ARCH-18 |
| 1.0 | 2026-01-27 | Frontend | Präzisierung | Ableitung atomarer Frontend-Designanforderungen DES-FE-01 bis DES-FE-20 |
| 1.0 | 2026-01-27 | Backend | Präzisierung | Einführung atomarer Backend-Anforderungen DES-BE-01 bis DES-BE-16 |
| 1.0 | 2026-01-27 | LLM | Erweiterung | Einführung dedizierter LLM-Governance DES-LLM-01 bis DES-LLM-12 |

---

## Dokumenthierarchie (informativ)

1. DESIGN.md — normative Architektur- und Governance-Quelle  
2. LASTENHEFT.md — normative funktionale Spezifikation auf Basis von DESIGN.md  
3. SYSTEM_REPORT.md — deskriptiver Auditbericht  
4. README.md — Orientierung  
5. übrige Dokumente — informativ  

---

## Requirement-Typen

Alle Anforderungen in diesem Dokument gehören genau zu einem der folgenden Typen:

- DES-GOV — Governance
- DES-ARCH — Architektur
- DES-FE — Frontend
- DES-BE — Backend
- DES-LLM — LLM

---

## Governance

### DES-GOV-01 — Normative Autorität von DESIGN.md
DESIGN.md definiert die verbindlichen Regeln für Architektur, Governance und Implementierung des Systems.

### DES-GOV-02 — Vorrang von DESIGN.md
DESIGN.md besitzt Vorrang gegenüber allen anderen Projektdokumenten und Ausgaben.

### DES-GOV-03 — Rolle von LASTENHEFT.md
LASTENHEFT.md definiert die verbindlichen funktionalen Anforderungen auf Basis von DESIGN.md.

### DES-GOV-04 — Normative Form von Anforderungen
Normative Wirkung besitzen ausschließlich Anforderungen, die in DESIGN.md oder LASTENHEFT.md als Requirement mit eindeutiger ID formuliert sind.

### DES-GOV-05 — Charakter informativer Artefakte
SYSTEM_REPORT.md, README.md, TECHNICAL_SPEC.md, PROMPTS.md, STYLEGUIDE.md und Code-Kommentare besitzen informativen Charakter.

### DES-GOV-06 — Anpassungsregel bei Abweichungen
Bei Abweichungen zwischen Systemverhalten und Anforderungen aus DESIGN.md werden Code und Konfiguration so angepasst, dass das Systemverhalten den Anforderungen entspricht.

### DES-GOV-07 — Klassifikation der Design-Anforderungen
Jede Anforderung in DESIGN.md verwendet genau einen Requirement-Typ aus der Typenliste.

### DES-GOV-08 — Autorität gegenüber LLM-Ausgaben
LLM-generierte Inhalte besitzen informativen Charakter im Projektkontext.

### DES-GOV-09 — Deterministische Aufgabenlösung
Aufgaben mit deterministisch lösbarer Zielstellung werden durch deterministische Verfahren umgesetzt.

### DES-GOV-10 — Ereignisprotokollierung
Das System erzeugt strukturierte Protokolleinträge für Fehlerereignisse, Integrationsereignisse und LLM-Aufrufereignisse.

### DES-GOV-11 — Abhängigkeitsdokumentation
Jede hinzugefügte Software-Abhängigkeit wird mit Zweck, Scope und Austauschstrategie dokumentiert.

### DES-GOV-12 — Build-Reproduzierbarkeit
Build-Prozesse erzeugen reproduzierbare Artefakte bei identischem Quellstand und identischer Toolchain-Konfiguration.

### DES-GOV-13 — CI-Qualitäts-Gates
CI-Pipelines führen Typprüfung und Linting als verpflichtende Qualitäts-Gates aus.

### DES-GOV-14 — Release-Rückführbarkeit
Releases besitzen eine eindeutige Version und sind auf konkrete Commits rückführbar.

### DES-GOV-15 — Generierungskennzeichnung im Systemmodell
Das Systemmodell klassifiziert Inhalte mit einem expliziten Herkunftsattribut (z. B. generiert, verifiziert, extern).

### DES-GOV-16 — Sanitization vor Darstellung
Darzustellende Daten werden vor UI-Rendering durch einen Sanitization-Schritt geführt.

### DES-GOV-17 — Mock-Kennzeichnung
Mock-Daten werden im UI und im Datenmodell als Mock gekennzeichnet.

### DES-GOV-18 — Mock-Austauschbarkeit
Mock-Datenquellen sind durch Real-Datenquellen austauschbar; UI-Komponenten bleiben dabei unverändert.

### DES-GOV-19 — Mock-Betriebsmodus
Das System führt einen expliziten Betriebsmodus zur Aktivierung von Mock-Datenquellen.

### DES-GOV-20 — Strukturierung nach Verantwortlichkeiten
Code-Module und Funktionen sind entlang klar abgegrenzter Verantwortlichkeiten strukturiert.

### DES-GOV-21 — Testbarkeit je Schicht
Systemkomponenten sind so gestaltet, dass automatisierte Tests pro Schicht möglich sind.

### DES-GOV-22 — Testarten je Schicht
Das System unterstützt UI-Komponententests, Service-/API-Tests und IPC-Vertragstests als getrennte Testarten.

### DES-GOV-23 — Konfiguration als expliziter Bestandteil
Konfigurationswerte werden als explizite Konfiguration geführt und versionierbar dokumentiert.

### DES-GOV-24 — Änderungsdokumentation für DESIGN.md
Änderungen an DESIGN.md werden in der Änderungshistorie dokumentiert.

### DES-GOV-25 — Freigabe für DESIGN.md-Änderungen
Änderungen an DESIGN.md werden vor Wirksamkeit freigegeben.

### DES-GOV-26 — Konsistenzabgleich DESIGN.md ↔ LASTENHEFT.md
Änderungen an DESIGN.md werden auf Auswirkungen in LASTENHEFT.md geprüft und bei Bedarf durch korrespondierende Anpassungen konsistent gehalten.

### DES-GOV-27 — Sanitization Traceability
Das System erzeugt für jede UI-Darstellung ein Sanitization-Trace-Metadatum, das Sanitization-Version und Sanitization-Status referenziert.

### DES-GOV-28 — Dokumentationsartefakt: SYSTEM_REPORT.md
Das Projekt führt eine SYSTEM_REPORT.md als deskriptiven Auditbericht pro Systemversion.

### DES-GOV-29 — Dokumentationsartefakt: README.md
Das Projekt führt eine README.md als Orientierungsdokument für Zweck, Einstieg und Nutzung.

### DES-GOV-30 — Dokumentationsartefakt: TECHNICAL_SPEC.md
Das Projekt führt eine TECHNICAL_SPEC.md zur Dokumentation implementierungsspezifischer Details und technischer Parameter.

### DES-GOV-31 — Dokumentationsartefakt: STYLEGUIDE.md
Das Projekt führt eine STYLEGUIDE.md zur Dokumentation visueller Standards, UX-Muster und Design-Tokens.

### DES-GOV-32 — Dokumentationsartefakt: PROMPTS.md
Das Projekt führt eine PROMPTS.md zur Versionierung und Dokumentation der im System verwendeten LLM-Prompts.

### DES-GOV-33 — Atomare Anforderung
Jede normative Anforderung beschreibt genau eine fachliche oder technische Eigenschaft.

### DES-GOV-34 — Eigenständige Verifizierbarkeit
Jede normative Anforderung ist unabhängig prüfbar und eindeutig verifizierbar.

### DES-GOV-35 — Eigener Anforderungsabschnitt
Jede normative Anforderung ist als eigener Abschnitt formuliert.

### DES-GOV-36 — Eindeutige Anforderungs-ID
Jede normative Anforderung besitzt eine eindeutige Anforderungs-ID.

### DES-GOV-37 — Abschnittsbasierte Strukturierung
Normative Anforderungen werden über Abschnittsnummerierung und Überschriften strukturiert.

### DES-GOV-38 — Einheitliches Überschriftenformat
Jede normative Anforderung verwendet das Überschriftenformat `<ID> — <Kurzbezeichnung>`.

### DES-GOV-39 — Explizite Anforderungsauflösung
Die Auflösung einer Anforderung in mehrere Anforderungen wird explizit dokumentiert.

### DES-GOV-40 — Eindeutige ID-Zuordnung bei Auflösung
Jede aus einer Auflösung hervorgehende Anforderung referenziert eindeutig die ursprüngliche Anforderungs-ID.

### DES-GOV-41 — Anforderungsbasierte Systemänderung
Jede Änderung, Erweiterung oder Korrektur des Systems basiert auf einer expliziten, normativen Anforderung.

### DES-GOV-42 — Ableitung aus externen Änderungswünschen
Extern formulierte Änderungswünsche werden vor Implementierung in eine oder mehrere atomare, normative Anforderungen überführt.

### DES-GOV-43 — Freigabe vor Implementierung
Jede Änderung an normativen Anforderungen wird vor Implementierung freigegeben.

### DES-GOV-44 — Versionierung normativer Änderungen
Jede normative Änderung wird einer Version und einem Datum zugeordnet.

### DES-GOV-45 — Rückführbarkeit normativer Änderungen
Jede normative Änderung referenziert die betroffenen Requirement-IDs.

### DES-GOV-46 — Präzisierung vor Ableitung
Mehrdeutige Anforderungen werden vor Ableitung oder Implementierung präzisiert.

### DES-GOV-47 — Normative Gültigkeit freigegebener Versionen
Normative Gültigkeit besitzen die freigegebenen Versionen von DESIGN.md und LASTENHEFT.md.

### DES-GOV-48 — Pflege von CHANGELOG.md
Jede funktionale Änderung, Fehlerbehebung oder Release-Erstellung wird in `CHANGELOG.md` dokumentiert.

### DES-GOV-49 — CI-Toolchain-Vollständigkeit
Alle in CI verwendeten Tools und Abhängigkeiten sind im Repository dokumentiert und in CI reproduzierbar installierbar.

### DES-GOV-50 — Externe Binaries in Tests
Tests dürfen keine externen Binaries voraussetzen, es sei denn die CI installiert sie explizit oder der Code bietet einen Mock/Fallback-Pfad.

### DES-GOV-51 — Verbot von typing.Any ohne Ausnahme
typing.Any ist verboten, außer es existiert eine dokumentierte Ausnahme mit Begründung und Scope.

### DES-GOV-52 — Typing-Abhängigkeiten als Dev-Dependencies
Alle für die Typprüfung notwendigen Stubs/Typing-Pakete sind in den Dev-Dependencies geführt.

### DES-GOV-53 — Test-Determinismus und Isolation
Tests laufen deterministisch ohne Netzwerk- oder Browser-Abhängigkeiten, es sei denn sie sind explizit als Integrationstests markiert und getrennt ausführbar.

## Architektur

### DES-ARCH-01 — Strikte Schichtung
Das System besteht aus Frontend, Backend und Desktop-Shell mit klarer Trennung.

### DES-ARCH-02 — Unidirektionaler Datenfluss
Daten fließen von Benutzeraktion zu Zustand zu Service zu UI.

### DES-ARCH-03 — Schnittstellenbasierte Interaktion
Frontend und Backend interagieren ausschließlich über definierte Schnittstellen.

### DES-ARCH-04 — Desktop-Shell als Host
Das System stellt eine Desktop-Shell bereit, die das Frontend hostet.

### DES-ARCH-05 — Systemnahe Fähigkeiten über Desktop-Shell
Das System stellt IPC, Filesystem-Zugriff, lokalen Cache und Packaging-Fähigkeiten über die Desktop-Shell bereit.

### DES-ARCH-06 — Service-Schicht als Integrationsgrenze
Services bilden die Integrationsgrenze zwischen UI-Zustand und externen/Backend-Funktionen.

### DES-ARCH-07 — Zustandsgetriebenes Rendering
UI-Rendering erfolgt auf Basis eines expliziten Zustandsmodells.

### DES-ARCH-08 — Koordination systemnaher Zugriffe
Systemzugriffe werden durch die Desktop-Shell koordiniert.

### DES-ARCH-09 — Austauschbarkeit des Backends
Das Backend ist hinter JSON- und IPC-Verträgen austauschbar.

### DES-ARCH-10 — Fehler als modellierte Zustände
Fehler werden als explizite Systemzustände modelliert und transportiert.

### DES-ARCH-11 — Externe API-Abstraktion
Externe APIs werden hinter internen Service-Abstraktionen genutzt.

### DES-ARCH-12 — Cache als Systemfunktion
Caching wird als Systemfunktion mit konsistentem Schlüsselraum umgesetzt.

### DES-ARCH-13 — Rate-Limit als Systemfunktion
Rate-Limiting wird als Systemfunktion pro externer Quelle konfigurierbar umgesetzt.

### DES-ARCH-14 — Deduplication als Systemfunktion
Identische In-Flight Requests werden als Systemfunktion dedupliziert.

### DES-ARCH-15 — Typisierte IPC-Verträge
IPC-Nachrichten besitzen korrespondierende Typdefinitionen auf Frontend- und Backend-Seite.

### DES-ARCH-16 — IPC-Service-Layer
IPC-Aufrufe erfolgen über eine dedizierte Service-Abstraktionsschicht.

### DES-ARCH-17 — Vollständige IPC-Typdefinitionen
IPC-Typdefinitionen sind vollständig spezifiziert.

### DES-ARCH-18 — Strukturierter IPC-Fehlertransport
IPC transportiert Fehler als strukturierte, typisierte Fehlobjekte.

### DES-ARCH-19 — Plattformziel Desktop
Das System ist als Desktop-Anwendung für macOS und Windows ausführbar.

### DES-ARCH-20 — Backend-Lifecycle beim App-Start
Die Desktop-Shell initialisiert den Backend-Prozess beim Start der Anwendung.

### DES-ARCH-21 — Backend-Verfügbarkeitsprüfung
Die Desktop-Shell prüft nach Backend-Initialisierung die Erreichbarkeit des Backends über IPC.

### DES-ARCH-22 — Backend-Lifecycle beim App-Ende
Die Desktop-Shell terminiert den Backend-Prozess beim ordnungsgemäßen Beenden der Anwendung.

---

## Frontend

### DES-FE-01 — Komponentenbasierte Architektur
Das Frontend ist komponentenbasiert aufgebaut.

### DES-FE-02 — Komponenten-Zustandsmodelle
Frontend-Komponenten verwenden Props, lokalen State oder Context.

### DES-FE-03 — Server-State-Verwaltung
Server-State wird über ein dediziertes Server-State-Management verwaltet.

### DES-FE-04 — Custom Hooks für Datenzugriff
Alle Datenzugriffe erfolgen über dedizierte Custom Hooks.

### DES-FE-05 — Service-Layer-Nutzung
Frontend-Komponenten nutzen Backend- und IPC-Funktionalität über eine Service-Abstraktionsschicht.

### DES-FE-06 — Styling-System
Styling erfolgt über ein konsistentes, projektweit einheitliches Utility-Class-System.

### DES-FE-07 — Komponenten-Testbarkeit
UI-Komponenten sind isoliert testbar.

### DES-FE-08 — Render-Ökonomie
Frontend-Komponenten reduzieren Re-Renders durch stabile Props, selektive State-Abhängigkeiten und gezielte Komponentengrenzen.

### DES-FE-09 — Deklaratives Rendering
UI-Struktur wird durch deklaratives Rendering beschrieben.

### DES-FE-10 — Latenzmodellierung
Das Frontend modelliert Lade- und Wartezustände als explizite UI-Zustände.

### DES-FE-11 — Fehlerzustände als UI-Zustände
Das Frontend stellt Fehlerzustände als explizite UI-Zustände dar.

### DES-FE-12 — Partielle Ergebnisse
Das Frontend unterstützt die Darstellung partieller Ergebnisse.

### DES-FE-13 — Responsive Verhalten
Responsive Verhalten wird über CSS-basierte Layoutmechanismen umgesetzt.

### DES-FE-14 — Layoutgrößen als CSS-Verantwortung
Layoutgrößen werden durch CSS-basierte Mechanismen bestimmt.

### DES-FE-15 — Layoutneutrale Visualisierung
Visualisierungskomponenten passen sich an verfügbaren Platz an.

### DES-FE-16 — Globaler UI-Zustand als expliziter Store
Globaler UI-Zustand wird über einen expliziten Store mit klar definiertem Scope geführt.

### DES-FE-17 — Eingabenormalisierung
Frontend-Eingaben werden vor Service-Aufrufen normalisiert und validiert.

### DES-FE-18 — Datenherkunft in der UI
Das Frontend stellt die Datenherkunft als Anzeigeinformation dar.

### DES-FE-19 — Memoisierung schwerer Berechnungen
Wiederkehrende schwere Berechnungen werden memoisiert.

### DES-FE-20 — Rendering-Strategie
Das Frontend rendert die UI als Funktion des UI-Zustandsmodells.

---

## Backend

### DES-BE-01 — JSON APIs
Das Backend stellt JSON APIs bereit.

### DES-BE-02 — Typisierte Schnittstellen
APIs besitzen explizite Typdefinitionen.

### DES-BE-03 — Versionierte APIs
APIs sind versioniert.

### DES-BE-04 — Strukturierte Fehlerobjekte
Fehler werden als strukturierte Fehlerobjekte geliefert.

### DES-BE-05 — Ergebniszustände und Kennzeichnung
API-Antworten enthalten explizite Felder zur Kennzeichnung von Erfolg, Teil-Erfolg und Fehler.

### DES-BE-06 — Markierung generierter Inhalte
Backend-Ausgaben aus LLM-Verarbeitung werden als generiert markiert.

### DES-BE-07 — Trennung von verifizierten und generierten Daten
Backend-Datenmodelle führen verifizierte Daten und generierte Inhalte als getrennte Kategorien.

### DES-BE-08 — Provider-Modell für externe Quellen
Externe Datenquellen werden als Provider konfigurierbar eingebunden.

### DES-BE-09 — Konfigurationsbasierte Zugangsdaten
Zugangsdaten werden zur Laufzeit über Konfigurationsmechanismen bereitgestellt.

### DES-BE-10 — Rate-Limit-Unterstützung
Backend-Zugriffe auf externe APIs berücksichtigen konfigurierbare Rate-Limits.

### DES-BE-11 — Cache-Unterstützung
Backend-Zugriffe auf externe APIs nutzen einen Cache zur Wiederverwendung von Ergebnissen.

### DES-BE-12 — Deduplication-Unterstützung
Zeitgleiche identische externe Anfragen werden dedupliziert.

### DES-BE-13 — Sanitization-Fähigkeit
Backend-Ausgaben liefern Felder in einer Form, die Sanitization und sichere Darstellung unterstützt.

### DES-BE-14 — Vertragstests für APIs
Backend-APIs werden durch Vertragstests abgesichert.

### DES-BE-15 — Strukturierte Logs
Backend-Prozesse liefern strukturierte Logs für Fehler und Integrationsereignisse.

### DES-BE-16 — Observability-Anschlussfähigkeit
Das Backend liefert strukturierte Ereignisdaten als Grundlage für Observability-Integration.

---

## LLM

### DES-LLM-01 — Externe Nichtdeterministik
LLMs gelten als externe, nichtdeterministische Dienste.

### DES-LLM-02 — Kennzeichnung generierter Inhalte
LLM-Ausgaben werden als generiert gekennzeichnet.

### DES-LLM-03 — Verifikationstrennung
Verifizierte Daten und LLM-generierte Inhalte werden getrennt behandelt.

### DES-LLM-04 — Ausweisung fehlender Daten
Fehlende Daten werden als explizite Lücken ausgewiesen.

### DES-LLM-05 — Zwischenspeicherung von Ergebnissen
LLM-Ergebnisse werden zwischengespeichert.

### DES-LLM-06 — Deduplication identischer Prompts
Identische LLM-Anfragen werden dedupliziert.

### DES-LLM-07 — LLM-Aufrufkriterium
LLM-Aufrufe erfolgen für Aufgaben, deren Ergebnis nicht deterministisch aus Systemdaten ableitbar ist.

### DES-LLM-08 — Tokenverbrauchsprotokollierung
Der Tokenverbrauch wird pro LLM-Aufruf protokolliert.

### DES-LLM-09 — Deterministische Cache-Schlüssel
LLM-Cache-Schlüssel werden aus Prompt-Inhalt, Parametern und Modellkonfiguration deterministisch abgeleitet.

### DES-LLM-10 — Provider-Priorisierung
LLM-Provider werden als priorisierte Kette konfigurierbar ausgewählt.

### DES-LLM-11 — Ergebnis-Metadaten
LLM-Ergebnisse enthalten Metadaten zu Modell, Zeitpunkt und Eingangsparametern.

### DES-LLM-12 — Token-Budget-Fähigkeit
Das System unterstützt die Einführung von Token-Budgets durch messbare Token-Telemetrie.

### DES-LLM-13 — Mock-Default zur Kostenkontrolle
Das System initialisiert den LLM-Betrieb in einem Mock-/Demo-Modus als Standardbetriebsmodus.

### DES-LLM-14 — Warnung bei Aktivierung realer LLM-Aufrufe
Das System zeigt beim Start eine explizite Warnung, wenn reale LLM-Aufrufe aktiviert sind.

### DES-LLM-15 — Cache-Precheck vor LLM-Aufruf
Das System prüft vor jedem LLM-Aufruf, ob für die aktuelle Parameterkombination ein valides Ergebnis im Cache vorliegt.

---

END OF DESIGN.md
