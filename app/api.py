import logging
from fastapi import APIRouter, HTTPException, Query
from app.llm_agent import analyze_stock

router = APIRouter()
logger = logging.getLogger("api")

@router.get("/stock", tags=["Stock"])
async def get_stock_info(ticker: str = Query(..., description="Stock ticker symbol, e.g., NVDA")):
    """
    Fetch the latest stock price and generate an AI recommendation (buy/sell/hold)
    using Yahoo Finance data and ChatOpenAI.
    """
    logger.info(f"Received request for ticker: {ticker}")
    
    try:
        # Call the updated analyze_stock function, which fetches the stock price internally
        result = analyze_stock(ticker)
    except Exception as e:
        logger.exception("Error processing request for ticker: %s", ticker)
        raise HTTPException(status_code=500, detail="Error generating recommendation.")
    
    logger.info(f"Response: {result}")
    return result
