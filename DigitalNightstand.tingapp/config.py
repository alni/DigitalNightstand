import json
import sys
import os

from appdirs import AppDirs

_dirs = AppDirs("DigitalNightstand.tingapp")

def load_settings(config_file="config.json"):
    with open(_dirs.user_config_dir + "/" + config_file) as data_file:
        settings_data = json.load(data_file)
    return settings_data

def save_settings(data, config_file="config.json"):
    filename = _dirs.user_config_dir + "/" + config_file
    if not os.path.exists(os.path.dirname(filename)):
        # If the folder path to the User Config Directory does not exists,
        # then create it + any non-existing parent folders
        os.makedirs(os.path.dirname(filename))
    with open(_dirs.user_config_dir + "/" + config_file, "w") as outfile:
        print os.path.abspath(outfile.name)
        json.dump(data, outfile)

CONFIG_FILE = "config.json"
MPLAYER_PATH = "D:/Personal/Downloads/Software/AudioVideo/MPlayer/MPlayer-x86_64-r37451+g531b0a3/mplayer.exe"
if sys.platform.startswith("linux"):
    MPLAYER_PATH = "mplayer"

RADIO_STATIONS_PATH = "data/radio/NO.json"

try:
    SETTINGS = load_settings(CONFIG_FILE)
except IOError:
    # If settings could not be loaded due to an IOError (e.x. file not found),
    # then we set the settings to default values and then saves the settings-
    # This ensures that the settings has been correctly set and saved to file
    SETTINGS = {
        "alarms": [],
        "radio_stations": []
    }
    save_settings(SETTINGS, CONFIG_FILE)

WEB_FRONTENT_PORT = 8000
