from datetime import datetime
import textwrap
from print_utils import print_header, print_subheader, print_info, print_warning

def print_weather(weather_data):
    print_header("Weather Report")
    print_info("Location", weather_data.location)
    print_info("As of", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    print_subheader("Current Conditions")
    print_info("Temperature", weather_data.current_conditions['temperature'])
    print_info("Conditions", weather_data.current_conditions['conditions'])

    print_subheader("Additional Details")
    for label, value in weather_data.additional_details:
        print_info(label, value)

    print_subheader("7-Day Forecast")
    for period in weather_data.forecast:
        print_info(period['name'], 
                   f"{period['short_desc']}, {period['temp']}")

    if weather_data.hazards:
        print_warning("Hazardous Conditions")
        for hazard in weather_data.hazards:
            print(textwrap.fill(f"• {hazard}", width=60))