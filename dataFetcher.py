
import requests
import logging

logging.basicConfig(level=logging.INFO)

def getStockData(symbol, time_series_function, api_key):
    base_url = "https://www.alphavantage.co/query"
    params = {
        'function': time_series_function,
        'symbol': symbol,
        'apikey': api_key
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(data)
        time_series_key = next((key for key in data if 'Time Series' in key), None)
        if time_series_key:
            return data['Meta Data'], data[time_series_key]
        else:
            logging.error("Time Series data not found.")
            return None, None
    else:
        logging.error(f"Failed to fetch data: HTTP Status Code {response.status_code}")
        return None, None
