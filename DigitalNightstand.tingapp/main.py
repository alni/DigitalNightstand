import tingbot
import pygame
from tingbot import *
import arrow

import time
import json
import string
import thread
import os
from multiprocessing.pool import ThreadPool

from defs.colors import *

from Alarm import Alarm
from Radio import Radio
import WebFrontend as web_frontend
from WebFrontend import WebFrontend
import gui
from gui import *
import config

# Intitalize global objects
frontend = None
alarm = None
radio_config = config.RADIO_STATIONS_PATH # "data/radio.json"
p = None
current_coding = None
if os.name == 'nt':
    # On windows platforms, current character encoding is never "utf-8".
    # Instead it is a special "windows/cp" encoding
    # We need to run and check the output of the "chcp" windows command to
    # check for the current encoding
    import subprocess
    # We need to split the output by ": " and choosing the last/second part.
    # Then, we appends the returned number to the "cp" prefix (could as well
    # have used "windows-" as prefix)
    current_coding = "cp" + subprocess.check_output("chcp", shell=True).split(": ")[1].strip()
print current_coding

# Create a thread pool to keep the number of running threads to a minimum
thread_pool = ThreadPool(4)

@every(seconds=0.5)
def update():
    # Every 500ms check for new alarms and update the
    # current_time and current_date variables
    alarm.run_alarm()
    gui.current_date = time.strftime("%d %B %Y")
    gui.current_time = time.strftime("%H %M")

@every(seconds=2)
def update_radio():
    # Every other second, update the 
    # - Radio Player info object, and the 
    # - Radio Player stream name
    # Do this async on another thread to prevent lock/freeze
    thread_pool.apply_async(p.player.get_info, ())
    thread_pool.apply_async(p.player.set_name, ())


# Radio Page Draw method
def draw_radio_page():
    screen.text(
        gui.current_time,
        xy=(160, 20),
        font_size=40,
        color=COLOR_BLUE_LIGHT,
    )
    if time.localtime().tm_sec%2 == 1:
        # Blink the time seperator every second by
        # display it every other second
        screen.text(
            ":",
            xy=(160, 20),
            font_size=40,
            color=COLOR_BLUE_LIGHT,
        )
    screen.text(
        gui.current_date,
        xy=(160, 50),
        font_size=20,
        color=COLOR_TAN
    )

    # Radio Info Panel outer border
    screen.rectangle(
        xy=(8,70),
        size=(304,108),
        color=COLOR_TAN,
        align="topleft"
    )

    # Radio Info Top Panel - playback buttons and info
    screen.rectangle(
        xy=(10,72),
        size=(300,69),
        color=COLOR_BLUE_DARK,
        align="topleft"
    )

    # Radio Info Bottom Panel - Stream info (stream name and title/info)
    screen.rectangle(
        xy=(10,143),
        size=(300,33),
        color=COLOR_BLUE_DARK,
        align="topleft"
    )

    # Setup of the Stream Name and Title/Info
    radio_info = '(none)' # Initial value of the Stream Info
    station_name = p.player.get_name() # Get the Stream Name from the player output
    if station_name is None:
        # If the Stream Name could not be set/not yet set from the player output,
        # then set the Station Name to the name from the station list instead
        station_name = p.get_active_channel()['name']
    if p.player.info is not None:
        # If the Player info is set, then try to get the latest StreamTitle (Info)
        radio_info = p.player.info.get("StreamTitle")
    else:
        # Otherwise, set the Info to the default "(none)" value
        radio_info = '(none)'
    if radio_info is None:
        # If the Player info was set but the latest StreamTitle (Info) was not,
        # then set the Info to the default "(none)" value
        radio_info = '(none)'

    if current_coding is not None:
        # try decode the radio_info with the current coding
        # This is necessary with Windows systems where the
        # encoding is not unicode or ascii
        radio_info = radio_info.decode(current_coding)
        try:
            station_name = station_name.decode(current_coding)
        except Exception:
            station_name = p.get_active_channel()['name']

    # Update the Web Frontend API Data with the current radio info
    web_frontend.api_data["radio"]["station"] = station_name
    # p.get_active_channel()['name']
    web_frontend.api_data["radio"]["info"] = radio_info
    # radio_info = filter(onlyascii, radio_info)
    # radio_info = ''.join(c if is_ascii(c) else onlyascii(c) for c in radio_info) 
    # radio_info = filter(lambda x: x in string.printable, radio_info)

    # Draw the Station Name at the start/top in the bottom info panel
    screen.text(
        station_name,
        xy=(13, 143),
        font_size=15,
        color=COLOR_TAN,
        align="topleft"
    )

    # Draw the Station Info at the end/bottom in the bottom info panel
    screen.text(
        radio_info,
        xy=(12, 159),
        font_size=15,
        color=COLOR_BLUE_LIGHT,
        align="topleft"
    )

    # Play Button - Drawn at the left in the top info panel
    screen.image(
        "res/icons/material-design-icons-2.0/av/2x_web/ic_play_circle_outline_white_24dp.png",
        xy=(21,81),
        align="topleft"
    )

    # Pause button - Drawn to the right of the Play button in the top info panel
    screen.image(
        "res/icons/material-design-icons-2.0/av/2x_web/ic_pause_circle_outline_white_24dp.png",
        xy=(81,81),
        align="topleft"
    )

    # Previous Station button - Drawn at the bottom left of the screen window
    screen.image(
        "res/icons/material-design-icons-2.0/av/2x_web/ic_skip_previous_white_24dp.png",
        xy=(11,181),
        align="topleft"
    )

    # Next Station button - Drawn to the right of the Previous Station button 
    #                       at the bottom of the screen window
    screen.image(
        "res/icons/material-design-icons-2.0/av/2x_web/ic_skip_next_white_24dp.png",
        xy=(71,181),
        align="topleft"
    )

    # Volume Down button - Drawn to the right of the Next Station button at 
    #                      the bottom center of the screen window
    screen.image(
        "res/icons/material-design-icons-2.0/av/2x_web/ic_volume_down_white_24dp.png",
        xy=(131,181),
        align="topleft"
    )

    # Volume Up button - Drawn to the right of the Volume Down button at 
    #                    the bottom of the screen window
    screen.image(
        "res/icons/material-design-icons-2.0/av/2x_web/ic_volume_up_white_24dp.png",
        xy=(191,181),
        align="topleft"
    )

    # Volume Mute button - Drawn at the bottom right of the screen window
    screen.image(
        "res/icons/material-design-icons-2.0/av/2x_web/ic_volume_mute_white_24dp.png",
        xy=(251,181),
        align="topleft"
    )

# Clock Page Draw method
def draw_clock_page():
    screen.text(
        gui.current_time,
        xy=CLOCK_LABEL_TIME["xy"],
        color=CLOCK_LABEL_TIME["color"],
        font_size=CLOCK_LABEL_TIME["font_size"],
        align=CLOCK_LABEL_TIME["align"]
    )
    if time.localtime().tm_sec%2 == 1:
        # Draw the time seperator every other second (blink the separator)
        screen.text(
            ":",
            xy=CLOCK_LABEL_TIME["xy"],
            color=CLOCK_LABEL_TIME["color"],
            font_size=CLOCK_LABEL_TIME["font_size"],
            align=CLOCK_LABEL_TIME["align"]
        )

    screen.text(
        gui.current_date,
        xy=CLOCK_LABEL_DATE["xy"],
        color=CLOCK_LABEL_DATE["color"],
        font_size=CLOCK_LABEL_DATE["font_size"],
        align=CLOCK_LABEL_DATE["align"]
    )

    # Humanize the next alarm datetime to a string
    next_alarm = arrow.get(alarm.next_alarm()).humanize()
    # Draw the next alarm info on the bottom left of the the screen
    screen.text(
        CLOCK_LABEL_ALARM_NEXT["text"] % next_alarm,
        xy=CLOCK_LABEL_ALARM_NEXT["xy"],
        color=CLOCK_LABEL_ALARM_NEXT["color"],
        font_size=CLOCK_LABEL_ALARM_NEXT["font_size"],
        align=CLOCK_LABEL_ALARM_NEXT["align"]
    )


def set_current_page(val):
    gui.current_page = val

# Alarm Page touch event
# Stop the alarm if the alarm title is touched
@touch(
    xy=ALARM_LABEL_TITLE["xy"],
    size=ALARM_LABEL_TITLE["touch_size"],
    align=ALARM_LABEL_TITLE["align"]
)
def stop_alarm_clock(xy, action):
    if action == 'down':
        if alarm.current_alarm is not None:
            alarm.stop_alarm()

# Radio Page Play/Pause button touch event
@touch(xy=(20,80),size=(50,50),align="topleft")
@touch(xy=(80,80),size=(50,50),align="topleft")
def on_touch_radio_play_pause(xy, action):
    if action == 'down' and gui.current_page == 1:
        p.player.play_pause()

# Radio Page Previous Channel button touch event
@touch(
    xy=RADIO_PLAYER_BUTTON_CHANNEL_PREV["xy"],
    size=RADIO_PLAYER_BUTTON_CHANNEL_PREV["touch_size"],
    align=RADIO_PLAYER_BUTTON_CHANNEL_PREV["align"]
)
@touch(xy=(10,180),size=(50,50),align="topleft")
@button.press("midright")
def on_touch_radio_prev(xy=None, action="down"):
    if action == 'down' and gui.current_page == 1:
        p.prev_channel()

# Radio Page Next Channel button touch event
@touch(
    xy=RADIO_PLAYER_BUTTON_CHANNEL_NEXT["xy"],
    size=RADIO_PLAYER_BUTTON_CHANNEL_NEXT["touch_size"],
    align=RADIO_PLAYER_BUTTON_CHANNEL_NEXT["align"]
)
@touch(xy=(70,180),size=(50,50),align="topleft")
@button.press("right")
def on_touch_radio_next(xy=None, action="down"):
    if action == 'down' and gui.current_page == 1:
        p.next_channel()

# Radio Page Volume Down button touch event
@touch(xy=(130,180),size=(50,50),align="topleft")
def on_touch_radio_vol_down(xy, action):
    if action == 'down' and gui.current_page == 1:
        p.player.vol_down()

# Radio Page Volume Up button touch event
@touch(xy=(190,180),size=(50,50),align="topleft")
def on_touch_radio_vol_up(xy, action):
    if action == 'down' and gui.current_page == 1:
        p.player.vol_up()

# Radio Page Volume Mute button touch event
@touch(xy=(250,180),size=(50,50),align="topleft")
def on_touch_radio_mute(xy, action):
    if action == 'down' and gui.current_page == 1:
        p.player.mute()

# Radio Page DateTime touch event - switch to the Clock Page
@touch(xy=(8,0),size=(304,68),align="topleft")
def on_touch_radio_datetime(xy, action):
    if action == 'down' and gui.current_page == 1:
        if gui.last_touch == -1 or time.time() - gui.last_touch > 1:
            # only switch page if there is more than 1 second since last page change
            gui.last_touch = time.time() # set last page change to current time
            set_current_page(2)

# Clock Page DateTime touch event - switch to the Radio Page
@touch(xy=(8,8),size=(304,224),align="topleft")
def on_touch_clock_datetime(xy, action):
    if action == 'down' and gui.current_page == 2:
        if gui.last_touch == -1 or time.time() - gui.last_touch > 1:
            # only switch page if there is more than 1 second since last page change
            gui.last_touch = time.time() # set last page change to current time
            set_current_page(1)


# BEGIN: loop()
def loop():
    if config.MOUSE_VISIBLE:
        pygame.mouse.set_visible(config.MOUSE_VISIBLE)
    screen.fill(
        color=COLOR_BLUE_DARK
    )

    screen.image(
        "res/images/banner-911778_1280.jpg",
        xy=(0,0),
        align="top"
    )

    if alarm.current_alarm is not None:
        # Alarm currently firing - Show the Alarm Page
        screen.text(
            ALARM_LABEL_TITLE["text"] % alarm.current_alarm,
            xy=ALARM_LABEL_TITLE["xy"],
            color=ALARM_LABEL_TITLE["color"],
            font_size=ALARM_LABEL_TITLE["font_size"],
            align=ALARM_LABEL_TITLE["align"]
        )
    elif gui.current_page == 1:
        draw_radio_page()
    elif gui.current_page == 2:
        draw_clock_page()

# END: loop()

frontend = WebFrontend(port=config.WEB_FRONTENT_PORT)
frontend.serve()

settings_data = config.SETTINGS

with open(radio_config) as data_file:
    radio_data = json.load(data_file)

p = Radio(radio_channels=radio_data['channels'], mplayer_path=config.MPLAYER_PATH)
if "radio_stations" in settings_data and len(settings_data['radio_stations']) > 0:
    p.radio_channels.extend(settings_data['radio_stations'])

web_frontend.radio = p
alarm = Alarm("res/sounds/Argon_48k.wav", settings=settings_data)
alarm.create_alarms()

tingbot.run(loop)
