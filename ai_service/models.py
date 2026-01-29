
from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True)
    amount: float
    price_at_purchase: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Optional metadata
    type: str = Field(default="buy") # buy/sell
