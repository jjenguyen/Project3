import requests
import logging

def getStockData(symbol, apikey):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={symbol}&apikey={apikey}"
    logging.info("Fetching stock data for: %s", symbol)

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "Time Series (Weekly Adjusted)" not in data:
            raise ValueError("Unexpected data format received from API.")
        return data["Time Series (Weekly Adjusted)"]
    except requests.RequestException as e:
        logging.error("HTTP Request error for %s: %s", symbol, e)
        raise e  #propagates the exception to the caller
    except ValueError as e:
        logging.error("Data Processing error for %s: %s", symbol, e)
        raise e  #propagates the exception to the caller
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)
        raise e  #propagates the exception to the caller
