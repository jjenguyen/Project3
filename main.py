from datetime import datetime
import logging
from dataFetcher import getStockData
from userInput import getStockSymbol, getChartType, getStartDate, getEndDate
from graphGenerator import generate_graph
from timeSeriesFunctions import getTimeSeriesFunction

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_data(raw_data, start_date, end_date):
    # convert date strings to datetime objects
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # filter data to fit desired date range
    filtered_data = {}
    for date_str, details in raw_data.items():
        date = datetime.strptime(date_str, '%Y-%m-%d')
        if start_date <= date <= end_date:
            filtered_data[date_str] = {
                "Open": details["Open"],
                "High": details["High"],
                "Low": details["Low"],
                "Close": details["Close"]
            }
    return filtered_data

def main():
    apikey = "V6BVQP0SPVJAVA6X"

    print("Stock Data Visualizer")
    print("---------------------")

    # loop until user chooses to exit
    while True:
        # get stock symbol
        symbol = getStockSymbol()

        # get chart type
        chartType = getChartType()

        # get time series function
        timeSeriesFunction = getTimeSeriesFunction(symbol)

        # get start date
        startDate = getStartDate()

        # get end date
        endDate = getEndDate(startDate)

        # fetch stock data from Alpha Vantage
        raw_data = getStockData(symbol, timeSeriesFunction, apikey)
        if not raw_data:
            logging.error(f"Failed to fetch data for symbol: {symbol}")
            return

        # temporary for error checking
        print("Raw data structure:", raw_data)

        # preprocess the fetched data
        formattedStartDate = startDate.strftime('%Y-%m-%d')
        formattedEndDate = endDate.strftime('%Y-%m-%d')
        data = preprocess_data(raw_data, formattedStartDate, formattedEndDate)

        # generate and display the graph
        if not data:
            logging.error("No data available for the selected date range.")
        else:
            generate_graph(data, chartType, formattedStartDate, formattedEndDate, symbol)

        # ask user to continue or exit
        choice = input("\nWould you like to view more stock data? (y/n): ").strip().lower()
        if choice != "y":
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