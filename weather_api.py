import requests
from bs4 import BeautifulSoup
import re

def clean_forecast_description(description):
    words = re.findall('[A-Z][^A-Z]*', description)
    cleaned = ' '.join(words)
    cleaned = re.sub(r'(\S)then', r'\1 then', cleaned)
    return cleaned

def get_weather(weather_data):
    lat, lon = weather_data.lat, weather_data.lon
    url = f"https://forecast.weather.gov/MapClick.php?lat={lat}&lon={lon}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    location = soup.find("h2", class_="panel-title").text.strip()
    weather_data.set_location(location, lat, lon)

    current_conditions = soup.find(id="current_conditions-summary")
    weather_data.current_conditions = {
        "temperature": current_conditions.find(class_="myforecast-current-lrg").text,
        "conditions": current_conditions.find(class_="myforecast-current").text,
    }

    details = soup.find(id="current_conditions_detail").find_all("td")
    weather_data.additional_details = [
        (details[i].text.strip(), details[i+1].text.strip())
        for i in range(0, len(details) - 1, 2)
    ]

    forecast = soup.find(id="seven-day-forecast-list")
    weather_data.forecast = [
        {
            "name": period.find(class_="period-name").text,
            "short_desc": clean_forecast_description(period.find(class_="short-desc").text),
            "temp": period.find(class_="temp").text if period.find(class_="temp") else "N/A"
        }
        for period in forecast.find_all(class_="forecast-tombstone")
    ]

    hazards = soup.find(class_="panel-danger")
    if hazards:
        weather_data.hazards = [hazard.text for hazard in hazards.find_all('a')]