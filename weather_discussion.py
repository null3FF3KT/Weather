import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from config import OPENAI_API_KEY

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
        model="gpt-4o-2024-08-06",
        messages=[{"role": "system", "content": "You are an informative weatherman."}, {"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content.strip()