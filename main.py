from datetime import datetime
import logging
import os

from dataFetcher import getStockData
from userInput import getStockSymbol, getChartType, getStartDate, getEndDate
from graphGenerator import generateGraph

#setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parseDate(date_string):
    """Parse a string into a datetime object."""
    try:
        return datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        logging.error("Invalid date format. Please use YYYY-MM-DD.")
        return None

def preprocess_data(api_response, start_date, end_date):
    """Extract and reformat data from Alpha Vantage API response."""
    time_series_key = next(key for key in api_response.keys() if "Time Series" in key)
    raw_data = api_response[time_series_key]
    
    #filter data within the specified date range and reformat
    data = {date: float(details['4. close']) for date, details in raw_data.items() if start_date <= date <= end_date}
    
    return data

def main():
    apikey = "542MHNFURI47POKH"
    symbol = getStockSymbol()
    chartType = getChartType()
    startDateStr = getStartDate()  #YYYY-MM-DD format
    endDateStr = getEndDate()  #YYYY-MM-DD format

    #validate and parse the user input dates
    startDate = parseDate(startDateStr)
    endDate = parseDate(endDateStr)
    if not startDate or not endDate:
        logging.error("Invalid date input. Exiting.")
        return

    #fetch stock data from Alpha Vantage
    raw_data = getStockData(symbol, apikey)
    if not raw_data:
        logging.error("Failed to fetch data for symbol: %s", symbol)
        return
    
    #preprocess the fetched data
    data = preprocess_data(raw_data, startDateStr, endDateStr)
    if not data:
        logging.error("No data available for the selected date range.")
        return

    #generate and display the graph
    generateGraph(data, chartType, startDateStr, endDateStr)

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