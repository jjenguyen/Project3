from userInput import getStockSymbol, getChartType, getStartDate, getEndDate
# from timeSeriesFunctions import getTimeSeriesFunction
# from graphGenerator import generateGraph
from dataFetcher import getStockData

def main():
    apikey = "542MHNFURI47POKH"

    # ask the user to enter the stock symbol
    symbol = getStockSymbol()

    # ask the user for the chart type
    # chartType = getChartType()

    # ask the user for the time series function
    # function = getTimeSeriesFunction()
    # # temporary to check if function is in correct api request format for url
    # print("Selected function:", function)

    # ask the user for start date (yyyy-mm-dd)
    startDate = getStartDate()

    # ask the user for end date (yyyy-mm-dd)
    endDate = getEndDate()

    # validate the user input dates
    # note: end date cannot be before start date
    try:
        # startDate =
        # endDate =
        if endDate < startDate:
            raise ValueError("Error: end date cannot be before start date. Please enter the dates again.")
    except ValueError as e:
        print("Error:", e)
        return
    
    # call function to get stock data
    # change to (symbol, function, startDate, endDate, apikey) once timeSeries is implemented
    data = getStockData(symbol, startDate, endDate, apikey)

    if data:
        # generateGraph(data, chartType)

        # printing data to see if api is properly hooked up and can fetch stock data
        print(data)
    else:
        print("Error: no data returned.")

if __name__ == "__main__":
    # this will only execute if this script is run directly, not when it's imported as a module into another script
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