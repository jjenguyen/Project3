from datetime import datetime
import logging
from dataFetcher import getStockData  # Ensure this matches the actual function name
from userInput import getStockSymbol, getChartType, getStartDate, getEndDate
from graphGenerator import generate_graph  # Ensure this matches the actual function name
from timeSeriesFunctions import getTimeSeriesFunction  # Adjust if needed

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_data(raw_data, start_date, end_date):
    filtered_data = {}
    for date_str, details in raw_data.items():
        date = datetime.strptime(date_str, '%Y-%m-%d')
        if start_date <= date <= end_date:
            filtered_data[date_str] = details['4. close']
    return filtered_data

def main():
    apikey = "574R6DZXDBWETSKK"  # Use your actual API key here

    print("Stock Data Visualizer")

    while True:
        symbol = getStockSymbol()
        chartType = getChartType()

        # If getTimeSeriesFunction requires 'symbol', ensure it's passed correctly
        # Otherwise, adjust getTimeSeriesFunction not to require 'symbol' if not needed
        timeSeriesFunction = getTimeSeriesFunction(symbol)

        startDateStr = getStartDate()  # Fetch the start date string
        endDateStr = getEndDate(startDateStr)  # Fetch the end date string, ensuring logic for comparison

        # Fetch stock data from Alpha Vantage
        metadata, raw_data = getStockData(symbol, timeSeriesFunction, apikey)
        if not raw_data:
            logging.error(f"Failed to fetch data for symbol: {symbol}")
            continue  # Allows user to retry instead of ending the script

        # Preprocess the fetched data based on the user-specified date range
        data = preprocess_data(raw_data, startDateStr, endDateStr)
        if not data:
            logging.error("No data available for the selected date range.")
            continue

        # Generate and display the graph based on the preprocessed data
        generate_graph(data, chartType, startDateStr, endDateStr)

        if input("\nWould you like to view more stock data? (y/n): ").lower() != 'y':
            break

if __name__ == "__main__":
    main()

# # tested to see if api properly hooked up to app: successful
# # import requests

# def fetch_stock_data(url):
#     try:
# #         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             return data
#         else:
#             print("Error:", response.status_code)
#             return None
#     except Exception as e:
#         print("Error:", e)
#         return None

# def main():
#     api_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo"
#     data = fetch_stock_data(api_url)
#     if data:
#         print("Data fetched successfully:")
#         print(data)
#     else:
#         print("Failed to fetch data.")

# if __name__ == "__main__":
#     main()