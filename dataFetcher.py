import requests
import logging

def getStockData(symbol, timeSeriesFunction, apikey):
    if "TIME_SERIES_INTRADAY" in timeSeriesFunction:
        # symbol is already included from timeSeriesFunctions.py so we do not need it again here
        url = f"https://www.alphavantage.co/query?function={timeSeriesFunction}&apikey={apikey}"
    else:
        # url format for all other time series functions
        url = f"https://www.alphavantage.co/query?function={timeSeriesFunction}&symbol={symbol}&apikey={apikey}"

    # temporary for error checking
    logging.info(f"Fetching stock data for: {symbol} using function: {timeSeriesFunction}")
    print("URL created:", url)

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # temporary for error checking
        # logging.error("API Response Content: %s", response.content)

        time_series_key = next((key for key in data.keys() if "Time Series" in key), None)
        
        if not time_series_key:
            raise ValueError("Time Series data not found in API response.")

        # extract and reformat the data
        time_series_data = data[time_series_key]
        processed_data = {}
        for date, details in time_series_data.items():
            processed_data[date] = {
                'Open': float(details['1. open']),
                'High': float(details['2. high']),
                'Low': float(details['3. low']),
                'Close': float(details['4. close'])
            }
        return processed_data

    except requests.RequestException as e:
        logging.error("HTTP Request error for %s: %s", symbol, e)
        raise
    except ValueError as e:
        logging.error("Data Processing error for %s: %s", symbol, e)
        raise
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)
        raise