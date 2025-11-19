from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from database import create_document, get_documents
from schemas import Strategy, Signal, PaperTrade

app = FastAPI(title="AI Robot Trading Platform API", version="0.1.0")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StrategyResponse(Strategy):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class CreateStrategyRequest(Strategy):
    pass

@app.get("/test")
async def test():
    return {"status": "ok"}

@app.post("/strategies", response_model=StrategyResponse)
async def create_strategy(payload: CreateStrategyRequest):
    created = await create_document("strategy", payload.model_dump())
    if not created:
        raise HTTPException(status_code=500, detail="Failed to create strategy")
    return created

@app.get("/strategies", response_model=List[StrategyResponse])
async def list_strategies():
    items = await get_documents("strategy", {}, 100)
    return items

class CreateSignalRequest(Signal):
    pass

@app.post("/signals")
async def create_signal(payload: CreateSignalRequest):
    created = await create_document("signal", payload.model_dump())
    if not created:
        raise HTTPException(status_code=500, detail="Failed to create signal")
    return created

class CreatePaperTradeRequest(PaperTrade):
    pass

@app.post("/paper-trades")
async def create_paper_trade(payload: CreatePaperTradeRequest):
    created = await create_document("papertrade", payload.model_dump())
    if not created:
        raise HTTPException(status_code=500, detail="Failed to create trade")
    return created
