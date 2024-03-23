import requests
import logging

def getStockData(symbol, timeSeriesFunction, apikey, output_size="full"):
    # Adjust the URL based on the timeSeriesFunction and include output_size
    if "TIME_SERIES_INTRADAY" in timeSeriesFunction:
        # For intraday, output_size is not applicable; remove or handle separately if intraday supports it differently
        url = f"https://www.alphavantage.co/query?function={timeSeriesFunction}&symbol={symbol}&apikey={apikey}"
    else:
        # Include output_size for daily, weekly, and monthly time series
        url = f"https://www.alphavantage.co/query?function={timeSeriesFunction}&symbol={symbol}&apikey={apikey}&outputsize={output_size}"

    logging.info(f"Fetching stock data for: {symbol} using function: {timeSeriesFunction}, Output Size: {output_size}")
    print("URL created:", url)

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        data = response.json()

        # Check for an error message in the response
        if "Error Message" in data:
            raise ValueError(data["Error Message"])

        # Find the correct key for time series data
        time_series_key = next((key for key in data.keys() if "Time Series" in key), None)
        
        if not time_series_key:
            raise ValueError("Time Series data not found in API response.")

        # Extract and reformat the data
        time_series_data = data[time_series_key]
        processed_data = {}
        for date, details in time_series_data.items():
            processed_data[date] = {
                'Open': float(details['1. open']),
                'High': float(details['2. high']),
                'Low': float(details['3. low']),
                'Close': float(details['4. close']),
                # Include 'Volume' if needed and available in the response
            }
        return processed_data

    except requests.RequestException as e:
        logging.error("HTTP Request error for %s: %s", symbol, e)
    except ValueError as e:
        logging.error("Data Processing error for %s: %s", symbol, e)
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)
