import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from colorama import init, Fore, Back, Style
import geocoder
from weather_config import get_location_preference

# Initialize colorama
init(autoreset=True)

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
    
def print_header(text):
    print(f"\n{Back.CYAN}{Fore.YELLOW}{Style.BRIGHT}{text}{Style.RESET_ALL}")

def print_subheader(text):
    print(f"{Fore.YELLOW}{Style.BRIGHT}{text}{Style.RESET_ALL}")

def print_info(label, value):
    print(f"{Fore.LIGHTGREEN_EX}{label}:{Style.RESET_ALL} {value}")

def print_warning(text):
    print(f"{Back.RED}{Fore.WHITE}{Style.BRIGHT}{text}{Style.RESET_ALL}")

def print_highlight(text, color=Fore.LIGHTYELLOW_EX):
    print(f"{color}{Style.BRIGHT}{text}{Style.RESET_ALL}")

def get_weather():
    lat, lon = get_location()
    url = f"https://forecast.weather.gov/MapClick.php?lat={lat}&lon={lon}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    print_header(f"🌦️  Weather Report for {lat:.4f}, {lon:.4f} as of {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 🌦️")
    
    print_subheader("\n📍 Current Conditions:")
    
    # Extract current conditions
    current_conditions = soup.find(id="current_conditions-summary")
    location = soup.find("h2", class_="panel-title").text.strip()
    temperature = current_conditions.find(class_="myforecast-current-lrg").text
    conditions = current_conditions.find(class_="myforecast-current").text

    print_info("Location", location)
    print_info("Temperature", f"{Back.RED}{Fore.WHITE}{Style.BRIGHT}{temperature}{Style.RESET_ALL}")
    print_info("Conditions", conditions)

    # Extract additional details
    print_subheader("\n📊 Additional Details:")
    details = soup.find(id="current_conditions_detail").find_all("td")
    for i in range(0, len(details) - 1, 2):
        print_info(details[i].text.strip(), details[i+1].text.strip())

    # Extract and print forecast
    print_subheader("\n🗓️  7-Day Forecast:")
    forecast = soup.find(id="seven-day-forecast-list")
    for period in forecast.find_all(class_="forecast-tombstone"):
        name = period.find(class_="period-name").text
        short_desc = period.find(class_="short-desc").text
        temp = period.find(class_="temp").text if period.find(class_="temp") else "N/A"
        print(f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}{name}:{Style.RESET_ALL} {short_desc}, {Back.LIGHTRED_EX}{Fore.WHITE}{Style.BRIGHT}{temp}{Style.RESET_ALL}")

    # Extract any hazardous conditions
    hazards = soup.find(class_="panel-danger")
    if hazards:
        print_warning("\n⚠️  Hazardous Conditions:")
        for hazard in hazards.find_all('a'):
            print_warning(f"  • {hazard.text}")

    print(f"\n{Back.CYAN}{Fore.BLACK}{Style.BRIGHT}{'=' * 50}{Style.RESET_ALL}\n")
    
get_weather()
# Run the function every 15 minutes
# while True:
#    try:
#         get_weather()
#         time.sleep(900)  # Sleep for 15 minutes
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         time.sleep(60)  # Wait a minute before trying again