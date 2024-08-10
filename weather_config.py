import json
import os
from datetime import datetime, timedelta

CONFIG_FILE = 'weather_config.json'
DEFAULT_CONFIG = {
    'use_geocoder': None,
    'lat': None,
    'lon': None,
    'last_confirmation': None,
    'agreed_to_eula': False
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def get_user_input(prompt, valid_responses=None):
    while True:
        response = input(prompt).strip().lower()
        if valid_responses is None or response in valid_responses:
            return response
        print("Invalid input. Please try again.")

def confirm_geocoder_use(config):
    if config['use_geocoder'] is None or (config['last_confirmation'] and 
        (datetime.now() - datetime.fromisoformat(config['last_confirmation'])) > timedelta(days=30)):
        print("\nPrivacy Notice:")
        print("\nThis application can use your device's location to provide local weather information.")
        print("If you opt to use automatic location detection, we do not store your location data.")
        print("We cannot guarantee that the third-party geocoding library does not track usage.")
        print("For your convenience, we will store the most recent latitude and longitude you provide manually.")
        print("All data we store is stored on your local system (weather_config.json), and we do not have access to it.")
        response = get_user_input("\nDo you want to use automatic location detection? (yes/no): ", ['yes', 'no'])
        config['use_geocoder'] = (response == 'yes')
        config['last_confirmation'] = datetime.now().isoformat()
        save_config(config)

def is_valid_lat_lon(lat, lon):
    return -90 <= lat <= 90 and -180 <= lon <= 180

def get_manual_location(config):
    print("\nPlease provide your latitude and longitude:")
    attempts = 0
    max_attempts = 3
    default_lat, default_lon = 30.281, -89.7777  # Default coordinates

    while attempts < max_attempts:
        try:
            lat = float(input("Latitude (-90 to 90): "))
            lon = float(input("Longitude (-180 to 180): "))
            
            if is_valid_lat_lon(lat, lon):
                config['lat'] = lat
                config['lon'] = lon
                save_config(config)
                print("Location saved successfully.")
                return
            else:
                print("Invalid latitude or longitude. Please try again.")
        except ValueError:
            print("Invalid input. Please enter numeric values.")
        
        attempts += 1
        if attempts < max_attempts:
            print(f"You have {max_attempts - attempts} more attempts.")
    
    print(f"Maximum attempts reached. Using default location: {default_lat}, {default_lon}")
    config['lat'] = default_lat
    config['lon'] = default_lon
    save_config(config)

def check_eula_agreement(config):
    if not config['agreed_to_eula']:
        print("\nEnd User License Agreement (EULA):")
        print("1. By using this application, you agree to indemnify the developer against any privacy violations")
        print("   that may occur through the use of this application or its associated geocoding services.")
        print("2. You acknowledge that while we take precautions to protect your privacy, we cannot guarantee")
        print("   the actions of third-party services used by this application.")
        print("3. This application retrieves weather data from NOAA.gov. By using this application, you agree")
        print("   to comply with NOAA's data usage policies and any applicable terms of service.")
        print("4. You agree to use this application responsibly, including respecting rate limits and not")
        print("   overloading NOAA's servers with excessive requests.")
        print("5. The developers of this application are not responsible for any misuse or violation of")
        print("   NOAA's terms of service by users of this application.")
        
        agreement = get_user_input("\nDo you agree to these terms? (yes/no): ", ['yes', 'no'])
        if agreement == 'yes':
            config['agreed_to_eula'] = True
            save_config(config)
        else:
            print("You must agree to the EULA to use this application.")
            exit()

def get_location_preference():
    config = load_config()
    
    check_eula_agreement(config)
    
    if config['use_geocoder'] is False and config['lat'] is not None and config['lon'] is not None:
        response = get_user_input(f"Do you want to use the previous location (Lat: {config['lat']}, Lon: {config['lon']})? (yes/no): ", ['yes', 'no'])
        if response == 'no':
            get_manual_location(config)
    elif config['use_geocoder'] is None or config['use_geocoder'] is True:
        confirm_geocoder_use(config)
        if not config['use_geocoder']:
            get_manual_location(config)
    
    return config