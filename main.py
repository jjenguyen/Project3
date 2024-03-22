import json
import logging
from datetime import datetime
from graphGenerator import generate_graph

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_json_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def get_date_input(prompt):
    while True:
        date_str = input(prompt)
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            print("This is the incorrect date string format. It should be YYYY-MM-DD")

def main():
    logging.info("Welcome to the Stock Data Visualization Tool.")
    
    json_file = 'alphavantage.json'
    stock_data = read_json_file(json_file)
    
    chart_type = input("Enter chart type (line/bar): ").strip().lower()
    while chart_type not in ['line', 'bar']:
        print("Invalid chart type. Please enter 'line' or 'bar'.")
        chart_type = input("Enter chart type (line/bar): ").strip().lower()
    
    start_date = get_date_input("Enter start date (YYYY-MM-DD): ")
    end_date = get_date_input("Enter end date (YYYY-MM-DD): ")
    
    
    generate_graph(stock_data, chart_type, start_date, end_date)

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