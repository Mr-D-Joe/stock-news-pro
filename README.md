# Stock News Pro (Polyglot Edition)

A professional-grade stock news analysis system rebuilt for performance and scalability.

## Architecture

- **GUI**: Universal JavaFX application (`/gui`)
- **Engine**: High-performance C++ Data processing & C Database (`/engine`)
- **AI Service**: Python-based AI orchestration service (`/ai_service`)
- **Models**: Shared Protobuf definitions (`/shared`)

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

## GitHub Integration

To push this project to GitHub:
1. Create a new repository on GitHub.
2. Run:
```bash
git remote add origin https://github.com/YOUR_USERNAME/stock-news-pro.git
git branch -M main
git push -u origin main
```
