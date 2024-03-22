import json
import logging

def getStockData(symbol, timeSeriesFunction, apikey):
    file_path = 'alphavantage.json'
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Using the correct key based on your JSON structure
        time_series_key = "Weekly Time Series"
        
        # Check if the key exists
        if time_series_key not in data:
            raise ValueError("Time Series data not found in local JSON file.")
        
        # Optionally, you can further filter the data by symbol if your JSON includes multiple symbols
        # This example assumes the entire JSON is dedicated to one symbol and directly accesses the time series data
        time_series_data = data[time_series_key]
        
        # Here you can implement additional processing if needed, for example, filtering by date range
        
        return time_series_data
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except Exception as e:
        logging.error(f"An error occurred while loading JSON data: {e}")
        raise
