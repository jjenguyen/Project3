import pygal
from pygal.style import Style
import logging
import platform
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def preprocess_data(api_response, start_date_str, end_date_str):
    """Extract and reformat data from Alpha Vantage API response."""
    time_series_key = next((key for key in api_response.keys() if "Time Series" in key), None)
    if not time_series_key:
        logging.error("Time series key not found in API response.")
        return {}
    
    raw_data = api_response[time_series_key]
    
    # Convert user input strings to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    
    # Filter data within the specified date range and reformat
    filtered_data = {}
    for date_str, details in raw_data.items():
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

    # Initialize the chart based on the chart_type
    chart = pygal.Line(style=custom_style, x_label_rotation=20, show_legend=True,
                       title=f"Stock Data ({start_date} to {end_date})") if chart_type == 'line' \
        else pygal.Bar(style=custom_style, x_label_rotation=20, show_legend=True,
                       title=f"Stock Data ({start_date} to {end_date})")
    
    # Use sorted dates from the preprocessed data for x_labels
    dates = sorted(data.keys())
    chart.x_labels = dates
    closes = [data[date] for date in dates]

    # Add the 'Close' data to the chart
    chart.add('Close', closes)

    # Save the chart to a file
    svg_file_path = 'chart.svg'
    chart.render_to_file(svg_file_path)
    logging.info("Chart generated and displayed successfully.")

    # Open the SVG file with the default browser
    webbrowser.open(svg_file_path)

        