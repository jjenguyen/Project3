from datetime import datetime
import logging
from modified_dataFetcher import getStockData  # Ensure this matches the new filename if changed
from userInput import getStockSymbol, getChartType, getStartDate, getEndDate
from graphGenerator import generateGraph
from timeSeriesFunctions import getTimeSeriesFunction

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    print("Stock Data Visualizer")
    print("---------------------")

    # Loop until user chooses to exit
    while True:
        symbol = getStockSymbol()
        chartType = getChartType()
        timeSeriesFunction = getTimeSeriesFunction(symbol)
        startDate = getStartDate()
        endDate = getEndDate(startDate)

        # Adjusted to reflect local JSON data usage
        raw_data = getStockData(symbol, timeSeriesFunction, None)  # API key is not required for local data

        if not raw_data:
            logging.error(f"Failed to fetch data for symbol: {symbol}")
            return

        # Process and visualize the data
        formattedStartDate = startDate.strftime('%Y-%m-%d')
        formattedEndDate = endDate.strftime('%Y-%m-%d')
        generateGraph(raw_data, chartType, formattedStartDate, formattedEndDate)

        # User decision to continue or exit
        choice = input("\nWould you like to view more stock data? (y/n): ").strip().lower()
        if choice != "y":
            break

if __name__ == "__main__":
    main()


# # tested to see if api properly hooked up to app: successful
# import requests

# def fetch_stock_data(url):
#     try:
#         response = requests.get(url)
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