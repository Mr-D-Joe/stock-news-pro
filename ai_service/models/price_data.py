from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel

class PricePoint(BaseModel):
    date: datetime
    close: float
    volume: int

class PriceHistory(BaseModel):
    symbol: str
    history: List[PricePoint]
    
    def get_performance(self, days: int = 30) -> float:
        if len(self.history) < 2:
            return 0.0
        start = self.history[0].close
        end = self.history[-1].close
        return (end - start) / start * 100
