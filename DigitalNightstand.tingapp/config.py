import json
import sys
import os

from appdirs import AppDirs

_dirs = AppDirs("DigitalNightstand.tingapp")

USER_DATA_DIR = _dirs.user_data_dir
USER_CONFIG_DIR = _dirs.user_config_dir
USER_CACHE_DIR = _dirs.user_cache_dir
USER_LOG_DIR = _dirs.user_log_dir

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
    with open(filename, "w") as outfile:
        print os.path.abspath(outfile.name)
        json.dump(data, outfile)

def load_last_state(file="last_state.json"):
    filename = USER_DATA_DIR + "/" + file
    if not os.path.exists(filename):
        return None
    with open(USER_DATA_DIR + "/" + file) as data_file:
        last_state = json.load(data_file)
    return last_state

def save_last_state(last_radio_station=0, last_page=1, file="last_state.json"):
    filename = USER_DATA_DIR + "/" + file
    data = {
        "last_radio_station": last_radio_station,
        "last_page": last_page
    }
    if not os.path.exists(os.path.dirname(filename)):
        # If the folder path to the User Data Directory does not exists,
        # then create it + any non-existing parent folders
        os.makedirs(os.path.dirname(filename))
    with open(filename, "w") as outfile:
        print os.path.abspath(outfile.name)
        json.dump(data, outfile)

CONFIG_FILE = "config.json"
MPLAYER_PATH = "D:/Personal/Downloads/Software/AudioVideo/MPlayer/MPlayer-x86_64-r37451+g531b0a3/mplayer.exe"
if sys.platform.startswith("linux"):
    MPLAYER_PATH = "mplayer"

RADIO_STATIONS_PATH = USER_DATA_DIR + "/radio/NO.json" # "data/radio/NO.json"

try:
    SETTINGS = load_settings(CONFIG_FILE)
except IOError:
    # If settings could not be loaded due to an IOError (e.x. file not found),
    # then we set the settings to default values and then saves the settings
    # This ensures that the settings has been correctly set and saved to file
    SETTINGS = {
        "alarms": [],
        "radio": {
            "country": "NO",
            "radio_stations": []
        }
    }
    save_settings(SETTINGS, CONFIG_FILE)

WEB_FRONTENT_PORT = 8000
MOUSE_VISIBLE = True
DIRBLE_API_KEY = "<my-api-key>"
CLOCK_DATE_FORMAT = "DD MMMM YYYY"
CLOCK_TIME_FORMAT = "HH mm"

try:
    DIRBLE_API_KEY = load_settings("radio/private.json")["dirble_api_key"]
except Exception:
    DIRBLE_API_KEY = None
