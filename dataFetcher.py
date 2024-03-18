import requests

def getStockData(symbol, startDate, endDate, apikey):
    # change to (symbol, function, startDate, endDate, apikey) once getTimeSeries() is implemented
    # fetch stock data from Alpha Vantage API
    # temporary function = "TIME_SERIES_WEEKLY_ADJUSTED" for testing purposes, will change to {function} once getTimeSeries() is implemented
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={symbol}&apikey={apikey}"

    print("API URL Created:", url)

    try:
        # making the api request
        response = requests.get(url)
        # raise an exception for any HTTP errors
        response.raise_for_status()

        # parse json response
        data = response.json()
        return data
    except Exception as e:
        print("Error:", e)
        return None