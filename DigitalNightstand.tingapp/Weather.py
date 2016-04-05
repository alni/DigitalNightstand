import pygame
import forecastio # install with "pip install python-forecastio"
import urllib
import os
import json
import base64
import time


import config
import defs.weather_icons as wx_icons

_BASE_URL = "https://api.forecast.io/forecast/{api_key}/{lat},{lon}?"

class Weather(object):
    """description of class"""
    def __init__(self, config="data/weather.json", settings=None):
        self.last_update = -1
        self.forecast = None
        self.currently = None
        self.is_fetching = False
        if settings is None:
            self.settings = self.load_settings(config)
        elif "weather" in settings:
            self.settings = settings["weather"]

    def load_settings(self, config):
        """Load settings from config"""
        if config is not None and os.path.exists(config):
            # Only load settings if config is actually set and the file exists
            with open(config) as data_file:
                data = json.load(data_file)
            return data
        else:
            # Otherwise, return None
            return None

    def set_settings(self, settings):
        """Set the current settings"""
        if settings is not None and "weather" in settings:
            # Only set settings if settings is actually set and "weather" exists
            # within settings
            self.settings = settings["weather"]
            self.create_forecast()

    def _format_time(self, hour, minute):
        """Format hour and time as 'HH:MM'"""
        return "%02d:%02d" % (hour,minute)

    def create_forecast(self, cache_for=25):
        """Create forecast from settings"""
        if self.settings is not None and config.FORECASTIO_API_KEY is not None:
            # Only create forecast if settings actually set
            if cache_for <= 0 or (
                self.last_update == -1 or time.time() - self.last_update > cache_for * 60
            ):
                # only update forecast if 
                # - "cache_for" is less than or equal to "0" minutes (cache
                #   disabled) 
                # - OR there is more than "cache_for" minutes since last 
                #   forecast update
                self.last_update = time.time() # set last update to current time
                
                lat = self.settings["latitude"]
                lon = self.settings["longitude"]
                units = self.settings["units"]
                lang = self.settings["language"]
                self.is_fetching = True
                self.forecast = forecastio.manual(self.create_url())
                self.currently = self.forecast.currently()
                self.is_fetching = False

    def create_url(self):
        """Create Forecast IO API URL"""
        lat = self.settings["latitude"]
        lon = self.settings["longitude"]

        # Base64 decode the API Key before sending it with the request
        api_key = base64.b64decode(config.FORECASTIO_API_KEY)

        url = _BASE_URL.format(api_key=api_key, lat=lat, lon=lon)
        params = {
            "units": self.settings["units"],
            "lang": self.settings["language"]
        }
        
        return url + urllib.urlencode(params)

    def get_icon_path(self, datapoint):
        """Get Icon Path from datapoint
        
        Parameters:
        - datapoint : the datapoint (for example self.currently)
        """
        return wx_icons.ICON_PATH + wx_icons.FORECAST_IO_ICONS[datapoint.icon]


def test():
    settings = {
        "latitude": 51.5001,
        "longitude": -0.1262,
        "units": "si",
        "language": "nb"
    }
    weather = Weather(settings=settings)
    weather.create_forecast()
    print weather.currently.summary
    print weather.currently.icon
    print "%d C" % weather.currently.temperature

    while 1:
        continue

if __name__ == '__main__':
    test()
