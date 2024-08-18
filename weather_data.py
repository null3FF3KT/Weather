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