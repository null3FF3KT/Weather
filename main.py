import weather_data
import location_utils
import weather_api
import weather_formatter
import weather_discussion
import print_utils

def main():
    wd = weather_data.WeatherData()
    lat, lon = location_utils.get_location()
    wd.set_location("", lat, lon)  # Initially set with empty location string
    
    weather_api.get_weather(wd)
    weather_formatter.print_weather(wd)
    
    discussion = weather_discussion.get_weather_discussion()
    summary = weather_discussion.summarize_report(discussion, wd)
    print("\nWeather Discussion Summary:")
    print_utils.print_wrapped(summary)

if __name__ == "__main__":
    main()