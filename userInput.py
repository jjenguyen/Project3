from datetime import datetime
import logging
import requests

class UserCancelledOperation(Exception):
    """Exception raised when a user cancels an input operation."""

def getChartType():
    print("\nChart Types:")
    print("---------------")
    print("1. Bar")
    print("2. Line")
    chart_type_input = input("\nEnter the chart type you want (1, 2): ")

    while chart_type_input not in ['1', '2']:
        print("\nError: Invalid selection. Please choose 1 for Bar or 2 for Line.")
        chart_type_input = input("\nEnter your choice (1, 2): ")
    
    return 'bar' if chart_type_input == '1' else 'line'

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
            logging.warning("\nUser cancelled operation.")
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
        # Simple check for symbol length and characters without API call
        if not symbol.isalpha() or len(symbol) > 5:
            print("\nError: Invalid stock symbol. Please enter a valid symbol consisting of up to 5 uppercase alphabetic characters.")
        else:
            return symbol

def loadJsonData():
    """Load data from the local JSON file."""
    with open('alphavantage.json', 'r') as file:
        return json.load(file)

def main():
    try:
        print("Stock Data Visualizer")
        print("---------------------")
        symbol = getStockSymbol()
        chartType = getChartType()
        startDate = getStartDate()
        endDate = getEndDate(startDate)

        # Load data from JSON and select relevant data based on symbol, start, and end dates
        all_data = loadJsonData()
        # Example: Modify to navigate your specific JSON structure and filter based on dates
        # This is a placeholder step; actual implementation depends on your JSON structure
        relevant_data = all_data['Weekly Time Series']  # Adjust this according to your JSON structure

        # Generate and display the graph using the selected data
        # You'll need to adjust how you pass data to this function based on your graph generation logic
        generateGraph(relevant_data, chartType, startDate.strftime('%Y-%m-%d'), endDate.strftime('%Y-%m-%d'))

    except UserCancelledOperation:
        print("Operation cancelled by the user.")

if __name__ == "__main__":
    main()