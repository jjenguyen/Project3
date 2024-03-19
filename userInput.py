from datetime import datetime
import logging

class UserCancelledOperation(Exception):
    """Exception raised when a user cancels an input operation."""

def parseDate(date_string):
    #arse a string into a datetime object
    try:
        return datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        logging.error("Invalid date format. Please use YYYY-MM-DD.")
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
    logging.info("Please enter the start date.")
    return getValidDate("Enter the start date (YYYY-MM-DD): ")

def getEndDate(startDate):
    #prompt user for a valid end date, ensuring it's not before the start date."""
    endDate = getValidDate("Enter the end date (YYYY-MM-DD): ")
    while endDate < startDate:
        logging.info("End date cannot be before the start date. Please enter a valid end date.")
        endDate = getValidDate("Enter the end date (YYYY-MM-DD): ")
    return endDate
