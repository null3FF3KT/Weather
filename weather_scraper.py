import textwrap
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from colorama import init, Fore, Back, Style
from openai import OpenAI
import geocoder
from weather_config import get_location_preference
from config import OPENAI_API_KEY

# Initialize colorama
init(autoreset=True)

# Print helper functions
def print_header(text):
    print(f"\n{Back.CYAN}{Fore.YELLOW}{Style.BRIGHT}{text:^60}{Style.RESET_ALL}")

def print_subheader(text):
    print(f"{Fore.YELLOW}{Style.BRIGHT}{text.center(60)}{Style.RESET_ALL}")

def print_info(label, value):
    label_width = 20
    value_width = 38
    print(f"{Fore.LIGHTGREEN_EX}{label:<{label_width}}{Style.RESET_ALL}"
          f"{value:<{value_width}}")

def print_warning(text):
    print(f"{Back.RED}{Fore.WHITE}{Style.BRIGHT}{text:^60}{Style.RESET_ALL}")

def print_highlight(text, color=Fore.LIGHTYELLOW_EX):
    print(f"{color}{Style.BRIGHT}{text:^60}{Style.RESET_ALL}")

class WeatherData:
    def __init__(self):
        self.location = ""
        self.lat = 0
        self.lon = 0
        self.current_conditions = {}
        self.additional_details = []
        self.forecast = []
        self.hazards = []

    def set_location(self, location, lat, lon):
        self.location = location
        self.lat = lat
        self.lon = lon

def get_location():
    config = get_location_preference()
    if config['use_geocoder']:
        g = geocoder.ip('me')
        if g.latlng:
            return g.latlng
        else:
            print("Failed to retrieve location. Using default coordinates.")
            return 30.251176, -87.6912539  # Default coordinates
    else:
        return config['lat'], config['lon']

def get_weather(weather_data):
    lat, lon = weather_data.lat, weather_data.lon
    url = f"https://forecast.weather.gov/MapClick.php?lat={lat}&lon={lon}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract location
    location = soup.find("h2", class_="panel-title").text.strip()
    weather_data.set_location(location, lat, lon)

    # Extract current conditions
    current_conditions = soup.find(id="current_conditions-summary")
    weather_data.current_conditions = {
        "temperature": current_conditions.find(class_="myforecast-current-lrg").text,
        "conditions": current_conditions.find(class_="myforecast-current").text,
    }

	# Extract additional details
    details = soup.find(id="current_conditions_detail").find_all("td")
    weather_data.additional_details = [
        (details[i].text.strip(), details[i+1].text.strip())
        for i in range(0, len(details) - 1, 2)
    ]

    # Extract forecast
    forecast = soup.find(id="seven-day-forecast-list")
    weather_data.forecast = [
        {
            "name": period.find(class_="period-name").text,
            "short_desc": period.find(class_="short-desc").text,
            "temp": period.find(class_="temp").text if period.find(class_="temp") else "N/A"
        }
        for period in forecast.find_all(class_="forecast-tombstone")
    ]

    # Extract hazards
    hazards = soup.find(class_="panel-danger")
    if hazards:
        weather_data.hazards = [hazard.text for hazard in hazards.find_all('a')]

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

def get_weather_discussion():
    url = "https://www.nhc.noaa.gov/text/MIATWDAT.shtml"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    discussion = soup.find('pre').text.strip()
    return discussion

def summarize_report(discussion, weather_data):
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    prompt = f"""Summarize the following Atlantic Tropical Weather Discussion, focusing on any considerations for {weather_data.location} (latitude {weather_data.lat}, longitude {weather_data.lon}). Be very concise:

    {discussion}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are an informative weatherman."}, {"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content.strip()

def main():
    weather_data = WeatherData()
    lat, lon = get_location()
    weather_data.set_location("", lat, lon)  # Initially set with empty location string
    
    get_weather(weather_data)
    print_weather(weather_data)
    
    discussion = get_weather_discussion()
    summary = summarize_report(discussion, weather_data)
    print("\nWeather Discussion Summary:")
    print(textwrap.fill(summary, width=60))

if __name__ == "__main__":
    main()