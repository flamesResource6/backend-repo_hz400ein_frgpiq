from typing import Optional, Literal
from pydantic import BaseModel, Field

# Schemas define collections: class name lowercased is the collection

class Strategy(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = Field(None, max_length=500)
    symbol: str = Field(..., description="Ticker symbol, e.g., BTCUSDT or AAPL")
    timeframe: str = Field(..., description="Timeframe like 1m, 5m, 1h")
    risk_per_trade: float = Field(..., ge=0, le=1, description="Fraction of equity risked per trade (0-1)")
    status: Literal["active", "paused"] = "paused"

class Signal(BaseModel):
    strategy_id: str
    side: Literal["buy", "sell"]
    price: float
    confidence: float = Field(..., ge=0, le=1)

class PaperTrade(BaseModel):
    strategy_id: str
    symbol: str
    side: Literal["buy", "sell"]
    qty: float
    entry_price: float
    pnl: float = 0.0
