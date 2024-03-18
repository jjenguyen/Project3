def getStockSymbol():
    # prompt user to enter stock symbol
    symbol = input("Enter the stock symbol (e.g. AAPL = Apple, MSFT = Microsoft): ")
    return symbol

def getChartType():
    # prompt user to select chart type
    chartType = input("Select the chart type (line/bar): ")
    return chartType

def getStartDate():
    # prompt user to enter start date
    startDate = input("Enter the start date (YYYY-MM-DD): ")
    return startDate

def getEndDate():
    # prompt user to enter end date
    endDate = input("Enter the end date (YYYY-MM-DD): ")
    return endDate