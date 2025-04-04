# Stock Market AI Agent API

This project provides a robust API endpoint that, given a stock ticker, returns the latest stock price along with an AI-generated recommendation (buy/sell/hold) using LangChain and OpenAI.

## Features

- **Real-Time Stock Data:**  
  Uses [yfinance](https://github.com/ranaroussi/yfinance) to fetch the latest stock price for any given ticker.

- **AI Analysis:**  
  Integrates LangChain with OpenAI to generate a clear buy/sell/hold recommendation, including a brief explanation.

- **API Service:**  
  Built using FastAPI and Uvicorn, with interactive documentation available at `/docs`.

- **Modular & Robust:**  
  Includes proper error handling, logging, and environment variable management.

## Project Structure

python-backend-llm-assessment/ ├── app/ │ ├── init.py │ ├── main.py │ ├── api.py │ ├── stock_fetcher.py │ └── llm_agent.py ├── tests/ │ └── test_api.py # (Optional) Automated tests for API endpoints ├── .env ├── requirements.txt └── README.md