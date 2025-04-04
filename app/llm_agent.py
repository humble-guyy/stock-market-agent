import os
import yfinance as yf
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the OpenRouter API key from environment variables
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is missing. Please set it in the .env file.")

def fetch_stock_price(ticker: str) -> float:
    """
    Fetch the latest closing price for the given stock ticker using Yahoo Finance.
    """
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period="1d")
        if history.empty:
            raise ValueError(f"No historical data found for ticker: {ticker}")
        price = history["Close"].iloc[-1]
        if price is None or price <= 0:
            raise ValueError(f"Invalid stock price retrieved for {ticker}: {price}")
        return float(price)
    except Exception as e:
        raise ValueError(f"Error fetching stock price for {ticker}: {e}")

def analyze_stock(ticker: str) -> dict:
    """
    Uses OpenRouter's DeepSeek V3 API to generate a buy/sell/hold recommendation.
    It fetches the latest stock price and sends it to the model for analysis.
    """
    # Fetch the latest stock price
    stock_price = fetch_stock_price(ticker)
    
    # Prepare the request for OpenRouter's DeepSeek API
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
                "Based on market trends and the price provided, please provide your final decision "
                "in the following format:\n\n"
                "Decision: [BUY/HOLD/SELL]\n"
                "Explanation: [Your detailed reasoning]."
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
