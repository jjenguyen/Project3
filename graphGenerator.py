import pygal
from pygal.style import Style
import logging
import platform
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def preprocess_data(api_response, start_date_str, end_date_str):
    # This line attempts to find the correct key for the time series data
    time_series_key = next((key for key in api_response if "Time Series" in key), None)
    
    if time_series_key:
        time_series_data = api_response[time_series_key]  # This is where time_series_data is defined
    else:
        logging.error("Time series key not found in API response.")
        return {}

    # Convert user input strings to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    
    # Filter data within the specified date range and reformat
    filtered_data = {}
    for date_str, details in time_series_data.items():  # Now time_series_data is correctly used
        date = datetime.strptime(date_str, '%Y-%m-%d')
        if start_date <= date <= end_date:
            filtered_data[date_str] = float(details['4. close'])

    if not filtered_data:
        logging.warning(f"No data available for the given date range: {start_date_str} to {end_date_str}")
    return filtered_data


#Function get it to open directly in the browser
def get_default_browser():
    """Get the default browser command based on platform."""
    system = platform.system()
    if system == "Windows":
        return "start"
    elif system == "Darwin":  # macOS
        return "open"
    else:  # Linux, Unix, etc.
        return "xdg-open"


import pygal
from pygal.style import Style
import logging
import webbrowser

def generate_graph(data, chart_type, start_date, end_date):
    custom_style = Style(
        background='transparent',
        plot_background='lightgrey',
        foreground='black',
        opacity='1',
        opacity_hover='.9',
        transition='400ms ease-in',
        colors=('#FF5733', '#33FF57', '#3357FF', '#FF33FB', '#F3FF33', '#33FFF3')
    )

    company_symbol = data.get("Meta Data", {}).get("2. Symbol", "Unknown Company")

    
    chart = pygal.Line(style=custom_style, x_label_rotation=80, show_legend=True, title=f"Stock Data for {company_symbol} ({start_date} to {end_date})") if chart_type == 'line' else pygal.Bar(style=custom_style, x_label_rotation=110, show_legend=True, title=f"Stock Data for {company_symbol} ({start_date} to {end_date})")

    filtered_sorted_data = {date: details for date, details in sorted(time_series_data.items()) if start_date <= date <= end_date}

    # Initialize the chart based on the chart_type
    chart = pygal.Line(style=custom_style, x_label_rotation=20, show_legend=True,
                       title=f"Stock Data for {company_symbol} ({start_date} to {end_date})") if chart_type == 'line' \
        else pygal.Bar(style=custom_style, x_label_rotation=20, show_legend=True,
                       title=f"Stock Data for {company_symbol} ({start_date} to {end_date})")
    
    dates = sorted(data.keys())
    chart.x_labels = dates
    closes = [data[date] for date in dates]
    chart.add('Close', closes)

    file_name = 'stock_chart.svg'
    chart.render_to_file(file_name)
    logging.info("Chart generated and displayed successfully.")
    webbrowser.open(file_name)
#This portions is correct
    dates = list(filtered_sorted_data.keys())
    opens = [float(details['1. open']) for details in filtered_sorted_data.values()]
    highs = [float(details['2. high']) for details in filtered_sorted_data.values()]
    lows = [float(details['3. low']) for details in filtered_sorted_data.values()]
    closes = [float(details['4. close']) for details in filtered_sorted_data.values()]
    
    # Set chart data
    chart.x_labels = dates
    chart.add('Open', opens)
    chart.add('High', highs)
    chart.add('Low', lows)
    chart.add('Close', closes)
    
    file_name = 'stock_chart.svg'
    chart.render_to_file(file_name)
