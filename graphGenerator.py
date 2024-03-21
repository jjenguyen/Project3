import pygal
from pygal.style import Style
import logging
import platform
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_data(api_response, start_date, end_date):
    """Extract and reformat data from Alpha Vantage API response."""
    time_series_key = next(key for key in api_response.keys() if "Time Series" in key)
    raw_data = api_response[time_series_key]
    
    #filter data within the specified date range and reformat
    data = {}
    for date, details in raw_data.items():
        if start_date <= date <= end_date:
            data[date] = {
                "open": float(details["1. open"]),
                "high": float(details["2. high"]),
                "low": float(details["3. low"]),
                "close": float(details["4. close"])
            }
    # data = {date: float(details['4. close']) for date, details in raw_data.items() if start_date <= date <= end_date}

    for date, details in data.items():
            logging.info(f"{date}: {details}")

    return data

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

def generateGraph(data, chartType, startDate, endDate):
    #customizing the chart style
    custom_style = Style(
        background='transparent',
        plot_background='transparent',
        foreground='#53E89B',
        foreground_strong='#53A0E8',
        foreground_subtle='#630C0D',
        opacity='.6',
        opacity_hover='.9',
        transition='400ms ease-in',
        colors=('#E853A0', '#E8537A', '#E95355', '#E88553')
    )
    
    #validate chart type
    if chartType not in ['line', 'bar']:
        logging.error(f"Invalid chart type selected: {chartType}")
        return

    try:
        #initialize chart with custom style
        chart = pygal.Line(style=custom_style, x_label_rotation=20, show_legend=True) if chartType == 'line' else pygal.Bar(style=custom_style, x_label_rotation=20, show_legend=True)
        
        #prepare data
        dates = sorted(list(data.keys()))

        logging.info(f"Dates: {dates}")
        logging.info("Data details:")
        for date, details in data.items():
            logging.info(f"{date}: {details}")

        opens = [float(details["open"]) for date, details in data.items() if date >= startDate and date <= endDate]
        highs = [float(details["high"]) for date, details in data.items() if date >= startDate and date <= endDate]
        lows = [float(details["low"]) for date, details in data.items() if date >= startDate and date <= endDate]
        closes = [float(details["close"]) for date, details in data.items() if date >= startDate and date <= endDate]
        # values = [data[date]['4. close'] for date in dates if date >= startDate and date <= endDate]
        # ERROR - An unexpected error occurred while generating or displaying the chart: 'float' object is not subscriptable
        # error fixed after modifying:
        # values = [data[date] for date in dates if date >= startDate and date <= endDate]

        logging.info(f"Opens: {opens}")

        #check for empty data
        if not dates or not opens or not highs or not lows or not closes:
            logging.error("No data available for the given date range.")
            return
        
        #set chart data
        chart.x_labels = dates
        # chart.add("Stock Price", values)
        chart.add("Open", opens)
        chart.add("High", highs)
        chart.add("Low", lows)
        chart.add("Close", closes)
        
        #render chart to file and open it
        svg_file_path = 'chart.svg'
        chart.render_to_file(svg_file_path)
        #webbrowser.open(svg_file_path)
        #logging.info("Chart generated and displayed successfully.")
         # Get the default browser command based on platform
    
        default_browser_cmd = get_default_browser()
        # Open the SVG file with the default browser
        command = f"{default_browser_cmd} {svg_file_path}"
        
        # Execute the command
        import subprocess
        subprocess.Popen(command, shell=True)
        
        logging.info("Chart generated and displayed successfully.")

        
    except IOError as e:
        logging.error(f"Failed to save the chart to {svg_file_path}: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while generating or displaying the chart: {e}")
