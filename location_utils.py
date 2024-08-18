import geocoder
from weather_config import get_location_preference

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