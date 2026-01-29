from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True)
    amount: float
    price_at_purchase: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    type: str = Field(default="buy")  # buy/sell
