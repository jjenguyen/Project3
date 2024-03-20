import requests
import logging

def getStockData(symbol, timeSeriesFunction, apikey):
    url = f"https://www.alphavantage.co/query?function={timeSeriesFunction}&symbol={symbol}&apikey={apikey}"
    logging.info(f"Fetching stock data for: {symbol} using function: {timeSeriesFunction}")

    print("URL created:", url)

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Check if the API response contains the expected data key
        data_key = None
        for key in data:
            if "Time Series" in key:
                data_key = key
                break

        if not data_key:
            raise ValueError("Time Series data not found in API response.")

        return data[data_key]
    except requests.RequestException as e:
        logging.error("HTTP Request error for %s: %s", symbol, e)
        raise
    except ValueError as e:
        logging.error("Data Processing error for %s: %s", symbol, e)
        raise
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)
        raise
