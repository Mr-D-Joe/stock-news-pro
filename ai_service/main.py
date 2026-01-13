from fastapi import FastAPI
from ai_service.analyzers.provider_factory import ProviderFactory
from ai_service.analyzers.impact_analyzer import ImpactAnalyzer

app = FastAPI(title="Stock News AI Service")

@app.get("/")
async def root():
    return {"status": "AI Service Online", "providers": ["gemini", "openai", "perplexity"]}

@app.post("/analyze/impact")
async def analyze_impact(symbol: str):
    # This will be refined to use the data from the C++ engine
    return {"symbol": symbol, "message": "Impact analysis endpoint ready"}
