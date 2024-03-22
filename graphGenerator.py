import pygal
from pygal.style import Style
import webbrowser
import os
import logging

def generate_graph(data, chart_type, start_date, end_date):
    custom_style = Style(
        background='transparent',
        plot_background='lightgrey',
        foreground='black',  # Set the text color to black
        foreground_strong='black',  # Ensure stronger foreground elements like titles are also black
        foreground_subtle='black',  # Set subtle foreground elements to black (e.g., axis labels)
        opacity='1',
        opacity_hover='.9',
        transition='400ms ease-in',
        colors=('#FF5733', '#33FF57', '#3357FF', '#FF33FB', '#F3FF33', '#33FFF3')
    )
    
    # Extract the company symbol or name if available
    company_symbol = data.get("Meta Data", {}).get("2. Symbol", "Unknown Company")
    
    # Change x_label_rotation to 110 for a more pitched angle
    chart = pygal.Line(style=custom_style, x_label_rotation=80, show_legend=True, title=f"Stock Data for {company_symbol} ({start_date} to {end_date})") if chart_type == 'line' else pygal.Bar(style=custom_style, x_label_rotation=110, show_legend=True, title=f"Stock Data for {company_symbol} ({start_date} to {end_date})")
    
    # Assuming 'Weekly Time Series' is your data key
    time_series_data = data.get('Weekly Time Series', {})
    
    # Filter and sort data within the date range
    filtered_sorted_data = {date: details for date, details in sorted(time_series_data.items()) if start_date <= date <= end_date}

    if not filtered_sorted_data:
        logging.warning("No data available for the given date range.")
        return

    # Extract dates and metrics
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

    # Open the generated SVG file in the default web browser
    try:
        webbrowser.open('file://' + os.path.realpath(file_name))
        logging.info("The graph has been generated and opened in your web browser.")
    except Exception as e:
        logging.error(f"Failed to open the graph: {e}")


