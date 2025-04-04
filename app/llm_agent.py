import os
import yfinance as yf
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the OpenRouter API key from the environment variable.
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
print("DEBUG: OPENROUTER_API_KEY =", OPENROUTER_API_KEY)
if not OPENROUTER_API_KEY:
    raise ValueError("Missing OPENROUTER_API_KEY environment variable. Please set it in your .env file.")

def fetch_stock_price(ticker: str) -> float:
    """
    Fetch the latest closing price for the given stock ticker using Yahoo Finance.
    """
    stock = yf.Ticker(ticker)
    history = stock.history(period="1d")
    if history.empty:
        raise ValueError(f"No historical data found for ticker: {ticker}")
    price = history["Close"].iloc[-1]
    if price is None or price <= 0:
        raise ValueError(f"Invalid stock price for {ticker}: {price}")
    return float(price)

def analyze_stock(ticker: str) -> dict:
    """
    Uses OpenRouter's DeepSeek V3 free API to generate a buy/sell/hold recommendation.
    It fetches the latest stock price from Yahoo Finance and sends a prompt to OpenRouter,
    which returns a final decision and an explanation.
    """
    # Fetch the current stock price
    stock_price = fetch_stock_price(ticker)
    
    # Prepare the request payload for OpenRouter's DeepSeek API
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek/deepseek-chat-v3-0324:free",
        "messages": [
            {"role": "system", "content": "You are a financial analyst."},
            {"role": "user", "content": (
                f"Analyze the stock {ticker} with the current price of ${stock_price:.2f}. "
                "Based on market trends, provide your final decision in the following format:\n\n"
                "Decision: [BUY/HOLD/SELL]\n"
                "Explanation: [Your reasoning]."
            )}
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise ValueError(f"Error generating recommendation: {response.text}")
    
    result = response.json()
    recommendation = result.get("choices", [{}])[0].get("message", {}).get("content", "No recommendation provided.")
    
    return {
        "ticker": ticker,
        "price": stock_price,
        "recommendation": recommendation.strip()
    }
