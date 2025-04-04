import logging
import yfinance as yf

logger = logging.getLogger("stock_fetcher")

def get_stock_data(ticker: str) -> dict:
    """
    Fetch the latest stock price using yfinance.
    This function returns a dictionary with the latest closing price.
    """
    try:
        stock = yf.Ticker(ticker)
        # Get historical data for the last day
        data = stock.history(period="1d")
        if data.empty:
            logger.warning(f"No historical data returned for ticker: {ticker}")
            return None
        # Extract the most recent closing price
        price = data["Close"].iloc[-1]
        logger.info(f"Fetched price ${price} for ticker: {ticker}")
        return {"price": price}
    except Exception as e:
        logger.exception(f"Error fetching data for {ticker}: {e}")
        return None
