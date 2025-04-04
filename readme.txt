

# Stock Market AI Agent

## Overview

The Stock Market AI Agent is a Python-based backend API that fetches real-time stock prices using Yahoo Finance and generates buy/hold/sell recommendations using an LLM API (OpenRouter's DeepSeek V3 free API) orchestrated via LangChain. Built with FastAPI and served by Uvicorn, the solution is designed to be lightweight, stateless, and deployable on a public hosting platform (Railway). This project demonstrates an end-to-end system that integrates financial data retrieval, AI-driven decision-making, and RESTful API design.


## Live Testing

You can test the live API in several ways:

### 1. Swagger UI
Access the interactive API documentation provided by FastAPI:
- **URL:** [https://web-production-677e.up.railway.app/docs](https://web-production-677e.up.railway.app/docs)
- **Usage:**  
  - Open the link in your browser.
  - Find the `/stock` endpoint.
  - Enter a stock ticker (e.g., `NVDA` or `AAPL`) and click **Execute**.
  - View the JSON response containing the ticker, current price, and recommendation.

### 2. curl (Command Line)
Open a terminal or PowerShell and run:  
```bash
curl -X GET "https://web-production-677e.up.railway.app/stock?ticker=NVDA" -H "accept: application/json"
```
This command sends a GET request and returns the JSON response.

### 3. Postman:
Open Postman and create a new GET request.

Set the URL to:  
https://web-production-677e.up.railway.app/stock?ticker=NVDA

In the Headers tab, add:[ Key: accept | Value: application/json ]

Click Send and observe the returned JSON response.



## Technology Stack

- Python: Main programming language.

- FastAPI: A modern, high-performance web framework for building REST APIs. It automatically generates interactive documentation.

- Uvicorn: An ASGI server that runs the FastAPI application.

- yfinance: A library for fetching real-time stock price data from Yahoo Finance.

- LangChain: A framework that helps structure prompts and chain operations with LLMs.

- OpenRouter's DeepSeek V3 API: Provides the language model (DeepSeek) for generating AI-based financial recommendations.

- Environment Variables & .env: Securely manage sensitive keys (like OPENROUTER_API_KEY).

- Git & GitHub: Version control and code hosting.

- Railway: Free deployment platform to host your API publicly.



## How It Works (End-to-End Workflow)

When a client sends a request to your live API, here is what happens:

### Client Request:
A GET request is sent to https://web-production-677e.up.railway.app/stock?ticker=NVDA using Swagger UI, curl, or Postman.

### FastAPI Handling (app/main.py):
 -  FastAPI receives the request and routes it to the /stock/{ticker} endpoint.

 -  The endpoint function extracts the ticker (NVDA) and calls two functions:

         Stock Price Retrieval: Calls get_stock_price(ticker) from app/stock_fetcher.py to fetch the latest closing price using yfinance.
         LLM Recommendation: Calls analyze_stock(ticker) from app/llm_agent.py.

### Stock Data Fetching (app/stock_fetcher.py):
  This module uses yfinance to connect to Yahoo Finance and retrieve the latest closing price for the requested ticker.
  The price is returned to the API route handler.

### LLM Analysis (app/llm_agent.py):
  This module reads the API key from the environment variable OPENROUTER_API_KEY.
  It constructs a prompt that includes the ticker and the current stock price, instructing the LLM to decide whether to buy, hold, or sell.

  It sends a POST request to https://openrouter.ai/api/v1/chat/completions with the appropriate headers (including the API key) and JSON payload.
  The response is processed to extract the final decision and explanation.

### Response:
  FastAPI returns a JSON response containing:
  ```bash
  {
    "ticker": "NVDA",
    "price": <current_price>,
    "recommendation": "Decision: [BUY/HOLD/SELL]\nExplanation: [Your reasoning]."
  }
  ```
  This response is displayed to the client through the testing tool.

## Structure
```bash
stock-market-agent/
│
├── app/
│   ├── main.py
│   │   - Initializes FastAPI and defines the main routes.
│   │   - Example:
│   │       @app.get("/stock/{ticker}")
│   │       def stock_analysis(ticker: str):
│   │           price = get_stock_price(ticker)
│   │           decision = analyze_stock(ticker)
│   │           return {"ticker": ticker, "price": price, "recommendation": decision}
│   │
│   ├── stock_fetcher.py
│   │   - Contains the function to fetch real-time stock data using yfinance.
│   │   - Example:
│   │       def get_stock_price(ticker: str) -> float:
│   │           stock = yf.Ticker(ticker)
│   │           history = stock.history(period="1d")
│   │           price = history["Close"].iloc[-1]
│   │           return float(price)
│   │
│   ├── llm_agent.py
│       - Handles generating AI recommendations.
│       - Loads the API key from the environment.
│       - Constructs the request to OpenRouter's DeepSeek API.
│       - Processes and returns the final decision and explanation.
│
├── .env
│   - Contains sensitive environment variables (e.g., `OPENROUTER_API_KEY`).
│   - Not committed to GitHub (add to `.gitignore`).
│
├── requirements.txt
│   - Lists all project dependencies:
│     - `FastAPI`, `Uvicorn`, `yfinance`, `LangChain`, `openai`, `python-dotenv`, `requests`, etc.
│
├── Procfile
│   - Tells Railway how to run the app.
│   - Example content:
│     ```
│     web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-8000}
│     ```
│
└── README.md
    - Project documentation (you’re reading it!).

---

### ✅ Quick Tips:
- Use `.env` to store sensitive info.
- Don't forget to run `pip install -r requirements.txt` before running the app.
- To test locally:
  ```bash
  uvicorn app.main:app --reload


```



## How to Run Locally

Clone the Repository:
```bash
git clone https://github.com/humble-guyy/stock-market-agent.git
cd stock-market-agent
``` 
Create and Activate a Virtual Environment:
```bash
python -m venv venv
venv\Scripts\activate    # Windows
                         # or for macOS/Linux: source venv/bin/activate
```

Install Dependencies:
```bash
pip install -r requirements.txt
```

Set Environment Variables:
Create a .env file in the project root with:
OPENROUTER_API_KEY=your_actual_api_key_here

Alternatively, set the environment variable in your terminal:
```bash
set OPENROUTER_API_KEY=your_actual_api_key_here   # Windows
export OPENROUTER_API_KEY=your_actual_api_key_here  # macOS/Linux
```

Run the Application:
```bash
uvicorn app.main:app --reload
```
The app will run locally at http://127.0.0.1:8000.

Test the API Locally:
Open a browser and go to http://127.0.0.1:8000/docs to access Swagger UI.

Use curl:
```bash
curl -X GET "http://127.0.0.1:8000/stock?ticker=NVDA" -H "accept: application/json"
Or use Postman to send a GET request to http://127.0.0.1:8000/stock?ticker=NVDA.
```



## Roadmap

- Additional browser support

- Add more integrations

