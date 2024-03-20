def getTimeSeriesFunction():
    print("\nSelect the time series of the chart you want to generate:")
    print("------------------------------------------------------------")
    print("1. Intraday")
    print("2. Daily")
    print("3. Weekly")
    print("4. Monthly")
    choice = input("\nEnter your choice (1-4): ")
    
    functions = {"1": "TIME_SERIES_INTRADAY", "2": "TIME_SERIES_DAILY", "3": "TIME_SERIES_WEEKLY", "4": "TIME_SERIES_MONTHLY"}
    return functions.get(choice, "TIME_SERIES_DAILY")  # Default to Daily if invalid choice