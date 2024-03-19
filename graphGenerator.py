import pygal
from pygal.style import Style
import logging
import webbrowser


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_data(api_response, start_date, end_date):
    """Extract and reformat data from Alpha Vantage API response."""
    time_series_key = next(key for key in api_response.keys() if "Time Series" in key)
    raw_data = api_response[time_series_key]
    
    #filter data within the specified date range and reformat
    data = {date: float(details['4. close']) for date, details in raw_data.items() if start_date <= date <= end_date}
    
    return data

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
        values = [data[date]['4. close'] for date in dates if date >= startDate and date <= endDate]

        #check for empty data
        if not dates or not values:
            logging.error("No data available for the given date range.")
            return
        
        #set chart data
        chart.x_labels = dates
        chart.add("Stock Price", values)
        
        #render chart to file and open it
        svg_file_path = 'chart.svg'
        chart.render_to_file(svg_file_path)
        webbrowser.open(svg_file_path)
        logging.info("Chart generated and displayed successfully.")
    
    except IOError as e:
        logging.error(f"Failed to save the chart to {svg_file_path}: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while generating or displaying the chart: {e}")
