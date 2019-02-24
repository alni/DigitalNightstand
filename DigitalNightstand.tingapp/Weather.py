import pygame
import forecastio # install with "pip install python-forecastio"
import urllib
import os
import json
import base64
import time


import config
import defs.weather_icons as wx_icons

_BASE_URL = "https://api.darksky.net/forecast/{api_key}/{lat},{lon}?"

class Weather(object):
    """description of class"""
    def __init__(self, config="data/weather.json", settings=None):
        self.last_update = -1
        self.forecast = None
        self.type = "currently" # supports "currently", "daily"
        self.currently = None
        self.hourly = None
        self.daily = None
        self.is_fetching = False
        self.settings = None
        if settings is None:
            self.settings = self.load_settings(config)
        elif "weather" in settings:
            self.settings = settings["weather"]
        
        if self.settings is not None:
            self.type = self.settings["type"]

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
            settings_changed = False
            if self.settings is None or (self.setting_is_different("latitude", settings)
                or self.setting_is_different("longitude", settings)
                or self.setting_is_different("units", settings)
                or self.setting_is_different("language", settings)):
                # Force re-creating of the forecast object if at-least one of 
                # the settings has changed (or if self.settings is not set)
                settings_changed = True
            self.settings = settings["weather"]
            if self.settings["type"] != self.type:
                self.type = self.settings["type"]
            if settings_changed:
                # Force re-creating of the forecast object and discard/disable
                # the cache temporarily
                self.create_forecast(cache_for=0, settings_changed=settings_changed)
            else:
                self.create_forecast()

    def setting_is_different(self, key, settings):
        """Checks if current setting from key is different than from input
        settings.
        """
        return settings["weather"][key] != self.settings[key]

    def _format_time(self, hour, minute):
        """Format hour and time as 'HH:MM'"""
        return "%02d:%02d" % (hour,minute)

    def create_forecast(self, cache_for=25, settings_changed=False):
        """Create forecast from settings
        
        Parameters:
        - cache_for : minutes to cache the request for (Defaults to 25).
                      Set to 0 or less to disable caching
        - settings_changed : whether the settings has been changed since last 
                             request and the request should be re-created.
                             (Defaults to False).
        """
        if self.settings is not None and config.DARK_SKY_API_KEY is not None:
            # Only create forecast if settings AND the Dark Sky API Key are
            # actually set
            if cache_for <= 0 or (
                self.last_update == -1 
                or time.time() - self.last_update > cache_for * 60):
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
                if self.forecast == None or settings_changed:
                    # Only (re)create the forecast if it is not set OR if the
                    # settings has been changed
                    self.forecast = forecastio.manual(self.create_url())
                else:
                    # Otherwise, just update the forecast
                    self.forecast.update()
                self.currently = self.forecast.currently()
                self.daily = self.forecast.daily()
                self.is_fetching = False

    def create_url(self):
        """Create Dark Sky API URL"""
        lat = self.settings["latitude"]
        lon = self.settings["longitude"]

        # Base64 decode the API Key before sending it with the request
        api_key = base64.b64decode(config.DARK_SKY_API_KEY)

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
        return wx_icons.ICON_PATH + wx_icons.DARK_SKY_ICONS[datapoint.icon]


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
