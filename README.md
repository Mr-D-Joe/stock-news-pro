# Stock News Pro (Polyglot Edition)

A professional-grade stock news analysis system rebuilt for performance,
scalability, and long-term maintainability.

The project combines a high-performance native engine, a modern JavaFX GUI,
and a Python-based AI orchestration layer into a clean, modular architecture.

---

## Architecture

The system is composed of four clearly separated components:

- **GUI (`/gui`)**  
  Universal JavaFX application responsible for visualization, interaction,
  and user experience.

- **Engine (`/engine`)**  
  High-performance C++ data processing engine with a native database layer.

- **AI Service (`/ai_service`)**  
  Python-based AI orchestration service providing analytics, enrichment,
  and data abstraction via a REST API.

- **Shared (`/shared`)**  
  Shared Protobuf definitions used for cross-language communication.

This separation allows independent scaling, testing, and optimization
of each subsystem.

---

## Design Rules

This project follows **strict UI layout and scaling rules** to ensure a
stable, predictable, and professional JavaFX user interface across all
screen sizes.

All contributors, tools, and automated refactors **must comply** with the
rules defined in:

➡️ **[DESIGN.md](DESIGN.md)**

UI changes that violate these rules are considered incorrect and must be fixed
before merging.

---

## Setup

### 1. AI Service (Python)

```bash
cd ai_service
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. Engine (C++)
```bash
cd engine
mkdir build && cd build
cmake ..
make
```

### 3. GUI (Java)
```bash
cd gui
mvn javafx:run
```
Development Notes
	•	Each component can be developed and run independently.
	•	The GUI communicates with the AI Service via HTTP.
	•	The Engine is optimized for performance-critical workloads and data handling.
	•	UI layout stability is a hard requirement and not subject to aesthetic preference.

## GitHub Integration

To push this project to GitHub:
1. Create a new repository on GitHub.
2. Run:
```bash
git remote add origin https://github.com/YOUR_USERNAME/stock-news-pro.git
git branch -M main
git push -u origin main
```
License

This project is currently under active development.
Licensing information will be added at a later stage.

