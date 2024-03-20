from datetime import datetime
import logging

class UserCancelledOperation(Exception):
    """Exception raised when a user cancels an input operation."""

def getChartType():
    print("\nChart Types:")
    print("---------------")
    print("1. Line Chart ")
    print("2. Bar Chart ")
    chart_type_input = input("\nEnter the chart type you want (1, 2): ")

    while chart_type_input not in ['1', '2']:
        print("\nError: Invalid selection. Please choose 1 for Line Chart or 2 for Bar Chart.")
        chart_type_input = input("\nEnter your choice (1 for Line Chart, 2 for Bar Chart): ")
    
    return 'line' if chart_type_input == '1' else 'bar'

def parseDate(date_string):
    #arse a string into a datetime object
    try:
        return datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        print("\nError: Invalid date format. Please use YYYY-MM-DD.")
        return None

def getValidDate(prompt):
    #prompt the user to enter a date until a valid date is provided
    while True:
        try:
            date_input = input(prompt)
            date = parseDate(date_input)
            if date:
                return date
        except KeyboardInterrupt:
            logging.warning("User cancelled operation.")
            raise UserCancelledOperation()

def getStartDate():
    #prompt user for a valid start date.
    # logging.info("Please enter the start date.")
    return getValidDate("\nEnter the start date (YYYY-MM-DD): ")

def getEndDate(startDate):
    #prompt user for a valid end date, ensuring it's not before the start date.
    endDate = getValidDate("Enter the end date (YYYY-MM-DD): ")
    while endDate < startDate:
        print("\nError: End date cannot be before the start date. Please enter a valid end date.")
        endDate = getValidDate("\nEnter the end date (YYYY-MM-DD): ")
    return endDate

def getStockSymbol():
    while True:
        symbol = input("\nEnter the stock symbol you are looking for: ").strip().upper()
        # Check if the symbol meets the criteria
        if not symbol.isalpha() or len(symbol) > 5:
            print("\nError: Invalid stock symbol. Please enter a valid symbol consisting of up to 5 uppercase alphabetic characters.")
        else:
            return symbol


