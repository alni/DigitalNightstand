import tingbot
import pygame
from tingbot import (
    button, every, screen, touch
)
import arrow

import atexit
import time
import json
import string
import thread
import os
import sys
import locale
import inspect
from multiprocessing.pool import ThreadPool

from defs.colors import *

from Alarm import Alarm
from Radio import Radio
import WebFrontend as web_frontend
from WebFrontend import WebFrontend
import gui
from gui import *
import config
import locales

from ScrollText import ScrollText

# Initialize global objects
frontend = None
alarm = None
radio_config = config.RADIO_STATIONS_PATH # "data/radio.json"
p = None
current_locale, current_coding = locale.getdefaultlocale()
if os.name == 'nt':
    # On windows platforms, current character encoding is never "utf-8".
    # Instead it is a special "windows/cp" encoding
    # We need to run and check the output of the "chcp" windows command to
    # check for the current encoding
    """
    FIXME: Is this really necessary when we get the current character encoding
           from the call to the "locale.getdefaultlocale()" method above?
    """
    import subprocess
    # We need to split the output by ": " and choosing the last/second part.
    # Then, we appends the returned number to the "cp" prefix (could as well
    # have used "windows-" as prefix)
    current_coding = "cp" + subprocess.check_output("chcp", shell=True).split(": ")[1].strip()
print current_coding

localized_strings = locales.get_locale(current_locale)
print localized_strings

# Create a thread pool to keep the number of running threads to a minimum
thread_pool = ThreadPool(4)

@atexit.register
def clean_up():
    frontend.stop()
    p.player.stop()
    config.save_last_state(
        last_radio_station=p.active_channel, 
        last_page=gui.current_page
    )
    thread_pool.close()
    pygame.quit()
    sys.exit()

@every(seconds=0.5)
def update():
    local = arrow.now()
    # Every 500ms check for new alarms and update the
    # current_time and current_date variables
    alarm.run_alarm()
    gui.current_date = local.format('D MMMM YYYY', current_locale)
    # time.strftime("%d %B %Y")
    gui.current_time = local.format("HH mm", current_locale)
    # time.strftime("%H %M")

@every(seconds=2)
def update_radio():
    # Every other second, update the 
    # - Radio Player info object, and the 
    # - Radio Player stream name
    # Do this async on another thread to prevent lock/freeze
    # thread_pool.apply_async(p.player.get_info, ())
    thread_pool.apply_async(p.player.set_title, ())
    thread_pool.apply_async(p.player.set_name, ())

    # Setup of the Stream Name and Title/Info
    radio_info = '(none)' # Initial value of the Stream Info
    station_name = p.player.get_name() # Get the Stream Name from the player output
    if station_name is None and 'name' in p.get_active_channel():
        # If the Stream Name could not be set/not yet set from the player output,
        # then set the Station Name to the name from the station list instead
        station_name = p.get_active_channel()['name']
    if p.player.title is not None:
        radio_info = p.player.title
    else:
        radio_info = '(none)'
    # if p.player.info is not None:
        # If the Player info is set, then try to get the latest StreamTitle (Info)
        # radio_info = p.player.info.get("StreamTitle")
    #else:
        # Otherwise, set the Info to the default "(none)" value
        #radio_info = '(none)'
    if radio_info is None:
        # If the Player info was set but the latest StreamTitle (Info) was not,
        # then set the Info to the default "(none)" value
        radio_info = '(none)'

    if current_coding is not None:
        # try decode the radio_info with the current coding
        # This is necessary with Windows systems where the
        # encoding is not Unicode or ASCII
        radio_info = radio_info.decode(current_coding)
        try:
            station_name = station_name.decode(current_coding)
        except Exception:
            station_name = p.get_active_channel()['name']

    gui.radio_station_name_text = station_name + ''
    gui.radio_station_info_text = radio_info + ''

    # Update the Web Frontend API Data with the current radio info
    web_frontend.api_data["radio"]["station"] = station_name
    # p.get_active_channel()['name']
    web_frontend.api_data["radio"]["info"] = radio_info


# Radio Page Draw method
def draw_radio_page():
    screen.text(
        gui.current_time,
        #xy=(160, 20),
        #font_size=40,
        #color=COLOR_BLUE_LIGHT,
        xy=PAGE_RADIO_TEXT_TIME["xy"],
        font_size=PAGE_RADIO_TEXT_TIME["font_size"],
        color=PAGE_RADIO_TEXT_TIME["color"],
        align=PAGE_RADIO_TEXT_TIME["align"]
    )
    if time.localtime().tm_sec%2 == 1:
        # Blink the time separator every second by
        # display it every other second
        screen.text(
            ":",
            #xy=(160, 20),
            #font_size=40,
            #color=COLOR_BLUE_LIGHT,
            xy=PAGE_RADIO_TEXT_TIME["xy"],
            font_size=PAGE_RADIO_TEXT_TIME["font_size"],
            color=PAGE_RADIO_TEXT_TIME["color"],
            align=PAGE_RADIO_TEXT_TIME["align"]
        )
    screen.text(
        gui.current_date,
        #xy=(160, 50),
        #font_size=20,
        #color=COLOR_TAN
        xy=PAGE_RADIO_TEXT_DATE["xy"],
        font_size=PAGE_RADIO_TEXT_DATE["font_size"],
        color=PAGE_RADIO_TEXT_DATE["color"],
        align=PAGE_RADIO_TEXT_DATE["align"]
    )

    # Radio Info Panel outer border
    screen.rectangle(
        #xy=(8,70),
        #size=(304,108),
        #color=COLOR_TAN,
        #align="topleft"
        xy=PAGE_RADIO_RECT_INFO_PANEL_OUTER["xy"],
        size=PAGE_RADIO_RECT_INFO_PANEL_OUTER["size"],
        color=PAGE_RADIO_RECT_INFO_PANEL_OUTER["color"],
        align=PAGE_RADIO_RECT_INFO_PANEL_OUTER["align"]
    )

    # Radio Info Top Panel - playback buttons and info
    screen.rectangle(
        #xy=(10,72),
        #size=(300,69),
        #color=COLOR_BLUE_DARK,
        #align="topleft"
        xy=PAGE_RADIO_RECT_INFO_PANEL_TOP["xy"],
        size=PAGE_RADIO_RECT_INFO_PANEL_TOP["size"],
        color=PAGE_RADIO_RECT_INFO_PANEL_TOP["color"],
        align=PAGE_RADIO_RECT_INFO_PANEL_TOP["align"]
    )

    # Radio Info Bottom Panel - Stream info (stream name and title/info)
    screen.rectangle(
        #xy=(10,143),
        #size=(300,33),
        #color=COLOR_BLUE_DARK,
        #align="topleft"
        xy=PAGE_RADIO_RECT_INFO_PANEL_BOTTOM["xy"],
        size=PAGE_RADIO_RECT_INFO_PANEL_BOTTOM["size"],
        color=PAGE_RADIO_RECT_INFO_PANEL_BOTTOM["color"],
        align=PAGE_RADIO_RECT_INFO_PANEL_BOTTOM["align"]
    )

    # Setup of the Stream Name and Title/Info
    radio_info = '(none)' # Initial value of the Stream Info
    station_name = p.player.get_name() # Get the Stream Name from the player output
    if station_name is None and 'name' in p.get_active_channel():
        # If the Stream Name could not be set/not yet set from the player output,
        # then set the Station Name to the name from the station list instead
        station_name = p.get_active_channel()['name']
    if p.player.title is not None:
        radio_info = p.player.title
    else:
        radio_info = '(none)'
    # if p.player.info is not None:
        # If the Player info is set, then try to get the latest StreamTitle (Info)
        # radio_info = p.player.info.get("StreamTitle")
    #else:
        # Otherwise, set the Info to the default "(none)" value
        #radio_info = '(none)'
    if radio_info is None:
        # If the Player info was set but the latest StreamTitle (Info) was not,
        # then set the Info to the default "(none)" value
        radio_info = '(none)'

    if current_coding is not None:
        # try decode the radio_info with the current coding
        # This is necessary with Windows systems where the
        # encoding is not Unicode or ASCII
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
        #xy=(13, 143),
        #font_size=15,
        #color=COLOR_TAN,
        #align="topleft"
        xy=PAGE_RADIO_TEXT_STATION_NAME["xy"],
        font_size=PAGE_RADIO_TEXT_STATION_NAME["font_size"],
        color=PAGE_RADIO_TEXT_STATION_NAME["color"],
        align=PAGE_RADIO_TEXT_STATION_NAME["align"]
    )

    # Draw the Station Info at the end/bottom in the bottom info panel
    if gui.radio_info_scroll_text is None:
        gui.radio_info_scroll_text = ScrollText(screen.surface, 
        radio_info, 159, COLOR_BLUE_LIGHT, (12,12), 15,
        font=os.path.join(os.path.dirname(inspect.getfile(tingbot)), 'Geneva.ttf'))
    else:
        gui.radio_info_scroll_text.update_text(radio_info)
        gui.radio_info_scroll_text.update()
        # pygame.display.flip()
    #screen.text(
    #    radio_info,
    #    xy=(12, 159),
    #    font_size=15,
    #    color=COLOR_BLUE_LIGHT,
    #    align="topleft"
    #)

    # Play Button - Drawn at the left in the top info panel
    screen.image(
        #"res/icons/material-design-icons-2.0/av/2x_web/ic_play_circle_outline_white_24dp.png",
        #xy=(21,81),
        #align="topleft"
        PAGE_RADIO_BUTTON_PLAY["src"],
        xy=PAGE_RADIO_BUTTON_PLAY["xy"],
        scale=PAGE_RADIO_BUTTON_PLAY["scale"],
        align=PAGE_RADIO_BUTTON_PLAY["align"]
    )

    # Pause button - Drawn to the right of the Play button in the top info panel
    screen.image(
        #"res/icons/material-design-icons-2.0/av/2x_web/ic_pause_circle_outline_white_24dp.png",
        #xy=(81,81),
        #align="topleft"
        PAGE_RADIO_BUTTON_PAUSE["src"],
        xy=PAGE_RADIO_BUTTON_PAUSE["xy"],
        scale=PAGE_RADIO_BUTTON_PAUSE["scale"],
        align=PAGE_RADIO_BUTTON_PAUSE["align"]
    )

    # Previous Station button - Drawn at the bottom left of the screen window
    screen.image(
        #"res/icons/material-design-icons-2.0/av/2x_web/ic_skip_previous_white_24dp.png",
        #xy=(11,181),
        #align="topleft"
        PAGE_RADIO_BUTTON_STATION_PREV["src"],
        xy=PAGE_RADIO_BUTTON_STATION_PREV["xy"],
        scale=PAGE_RADIO_BUTTON_STATION_PREV["scale"],
        align=PAGE_RADIO_BUTTON_STATION_PREV["align"]
    )

    # Next Station button - Drawn to the right of the Previous Station button 
    #                       at the bottom of the screen window
    screen.image(
        #"res/icons/material-design-icons-2.0/av/2x_web/ic_skip_next_white_24dp.png",
        #xy=(71,181),
        #align="topleft"
        PAGE_RADIO_BUTTON_STATION_NEXT["src"],
        xy=PAGE_RADIO_BUTTON_STATION_NEXT["xy"],
        scale=PAGE_RADIO_BUTTON_STATION_NEXT["scale"],
        align=PAGE_RADIO_BUTTON_STATION_NEXT["align"]
    )

    # Volume Down button - Drawn to the right of the Next Station button at 
    #                      the bottom center of the screen window
    screen.image(
        #"res/icons/material-design-icons-2.0/av/2x_web/ic_volume_down_white_24dp.png",
        #xy=(131,181),
        #align="topleft"
        PAGE_RADIO_BUTTON_VOL_DOWN["src"],
        xy=PAGE_RADIO_BUTTON_VOL_DOWN["xy"],
        scale=PAGE_RADIO_BUTTON_VOL_DOWN["scale"],
        align=PAGE_RADIO_BUTTON_VOL_DOWN["align"]
    )

    # Volume Up button - Drawn to the right of the Volume Down button at 
    #                    the bottom of the screen window
    screen.image(
        #"res/icons/material-design-icons-2.0/av/2x_web/ic_volume_up_white_24dp.png",
        #xy=(191,181),
        #align="topleft"
        PAGE_RADIO_BUTTON_VOL_UP["src"],
        xy=PAGE_RADIO_BUTTON_VOL_UP["xy"],
        scale=PAGE_RADIO_BUTTON_VOL_UP["scale"],
        align=PAGE_RADIO_BUTTON_VOL_UP["align"]
    )

    # Volume Mute button - Drawn at the bottom right of the screen window
    screen.image(
        #"res/icons/material-design-icons-2.0/av/2x_web/ic_volume_mute_white_24dp.png",
        #xy=(251,181),
        #align="topleft"
        PAGE_RADIO_BUTTON_VOL_MUTE["src"],
        xy=PAGE_RADIO_BUTTON_VOL_MUTE["xy"],
        scale=PAGE_RADIO_BUTTON_VOL_MUTE["scale"],
        align=PAGE_RADIO_BUTTON_VOL_MUTE["align"]
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
        # Draw the time separator every other second (blink the separator)
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
    # next_alarm = "(no current alarms)"
    next_alarm = localized_strings.get_alarm(None)
    if alarm.next_alarm() is not None:
        # Humanize the next alarm datetime to a string
        next_alarm = localized_strings.get_alarm(arrow.get(alarm.next_alarm()).humanize(locale=current_locale))
        # next_alarm = arrow.get(alarm.next_alarm()).humanize()
    # Draw the next alarm info on the bottom left of the the screen
    screen.text(
        next_alarm,
        xy=CLOCK_LABEL_ALARM_NEXT["xy"],
        color=CLOCK_LABEL_ALARM_NEXT["color"],
        font_size=CLOCK_LABEL_ALARM_NEXT["font_size"],
        align=CLOCK_LABEL_ALARM_NEXT["align"]
    )


def set_current_page(val):
    if gui.last_touch == -1 or time.time() - gui.last_touch > 1:
        # only switch page if there is more than 1 second since last page change
        gui.last_touch = time.time() # set last page change to current time
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
            p.player.unmute()

# Radio Page Play/Pause button touch event
#@touch(xy=(20,80),size=(50,50),align="topleft")
#@touch(xy=(80,80),size=(50,50),align="topleft")
@touch(
    xy=PAGE_RADIO_BUTTON_PLAY['touch_xy'],
    size=PAGE_RADIO_BUTTON_PLAY['touch_size'],
    align=PAGE_RADIO_BUTTON_PLAY['align'])
@touch(
    xy=PAGE_RADIO_BUTTON_PAUSE['touch_xy'],
    size=PAGE_RADIO_BUTTON_PAUSE['touch_size'],
    align=PAGE_RADIO_BUTTON_PAUSE['align'])
def on_touch_radio_play_pause(xy, action):
    # if action == 'down' and gui.current_page == 1:
    if gui.should_perform_radio_event(xy, action, alarm):
        p.player.play_pause()

# Radio Page Previous Channel button touch event
#@touch(
#    xy=RADIO_PLAYER_BUTTON_CHANNEL_PREV["xy"],
#    size=RADIO_PLAYER_BUTTON_CHANNEL_PREV["touch_size"],
#    align=RADIO_PLAYER_BUTTON_CHANNEL_PREV["align"]
#)
#@touch(xy=(10,180),size=(50,50),align="topleft")
@touch(
    xy=PAGE_RADIO_BUTTON_STATION_PREV['touch_xy'],
    size=PAGE_RADIO_BUTTON_STATION_PREV['touch_size'],
    align=PAGE_RADIO_BUTTON_STATION_PREV['align'])
@button.press("midright")
def on_touch_radio_prev(xy=None, action="down"):
    # if action == 'down' and gui.current_page == PAGE_INDEX_RADIO:
    if gui.should_perform_radio_event(xy, action, alarm):
        p.prev_channel()

# Radio Page Next Channel button touch event
#@touch(
#    xy=RADIO_PLAYER_BUTTON_CHANNEL_NEXT["xy"],
#    size=RADIO_PLAYER_BUTTON_CHANNEL_NEXT["touch_size"],
#    align=RADIO_PLAYER_BUTTON_CHANNEL_NEXT["align"]
#)
#@touch(xy=(70,180),size=(50,50),align="topleft")
@touch(
    xy=PAGE_RADIO_BUTTON_STATION_NEXT['touch_xy'],
    size=PAGE_RADIO_BUTTON_STATION_NEXT['touch_size'],
    align=PAGE_RADIO_BUTTON_STATION_NEXT['align'])
@button.press("right")
def on_touch_radio_next(xy=None, action="down"):
    # if action == 'down' and gui.current_page == PAGE_INDEX_RADIO:
    if gui.should_perform_radio_event(xy, action, alarm):
        p.next_channel()

# Radio Page Volume Down button touch event
# @touch(xy=(130,180),size=(50,50),align="topleft")
@touch(
    xy=PAGE_RADIO_BUTTON_VOL_DOWN['touch_xy'],
    size=PAGE_RADIO_BUTTON_VOL_DOWN['touch_size'],
    align=PAGE_RADIO_BUTTON_VOL_DOWN['align'])
def on_touch_radio_vol_down(xy, action):
    # if action == 'down' and gui.current_page == PAGE_INDEX_RADIO:
    if gui.should_perform_radio_event(xy, action, alarm):
        p.player.vol_down()

# Radio Page Volume Up button touch event
# @touch(xy=(190,180),size=(50,50),align="topleft")
@touch(
    xy=PAGE_RADIO_BUTTON_VOL_UP['touch_xy'],
    size=PAGE_RADIO_BUTTON_VOL_UP['touch_size'],
    align=PAGE_RADIO_BUTTON_VOL_UP['align'])
def on_touch_radio_vol_up(xy, action):
    # if action == 'down' and gui.current_page == PAGE_INDEX_RADIO:
    if gui.should_perform_radio_event(xy, action, alarm):
        p.player.vol_up()

# Radio Page Volume Mute button touch event
# @touch(xy=(250,180),size=(50,50),align="topleft")
@touch(
    xy=PAGE_RADIO_BUTTON_VOL_MUTE['touch_xy'],
    size=PAGE_RADIO_BUTTON_VOL_MUTE['touch_size'],
    align=PAGE_RADIO_BUTTON_VOL_MUTE['align'])
def on_touch_radio_mute(xy, action):
    # if action == 'down' and gui.current_page == PAGE_INDEX_RADIO:
    if gui.should_perform_radio_event(xy, action, alarm):
        p.player.toggle_mute()

# Radio Page DateTime touch event - switch to the Clock Page
# @touch(xy=(8,0),size=(304,68),align="topleft")
@touch(
    xy=PAGE_RADIO_TOUCH_TIME['touch_xy'],
    size=PAGE_RADIO_TOUCH_TIME['touch_size'],
    align=PAGE_RADIO_TOUCH_TIME['align'])
def on_touch_radio_datetime(xy, action):
    # if action == 'down' and gui.current_page == PAGE_INDEX_RADIO:
    if gui.should_perform_radio_event(xy, action, alarm):
        set_current_page(PAGE_INDEX_CLOCK)

# Clock Page DateTime touch event - switch to the Radio Page
#@touch(xy=(8,8),size=(304,224),align="topleft")
@touch(
    xy=CLOCK_RADIO_TOUCH_TIME['touch_xy'],
    size=CLOCK_RADIO_TOUCH_TIME['touch_size'],
    align=CLOCK_RADIO_TOUCH_TIME['align'])
def on_touch_clock_datetime(xy, action):
    if action == 'down' and gui.current_page == PAGE_INDEX_CLOCK:
        set_current_page(PAGE_INDEX_RADIO)


# BEGIN: loop()
def loop():
    if not gui.initialized:
        if config.MOUSE_VISIBLE:
            pygame.mouse.set_visible(config.MOUSE_VISIBLE)
        pygame.display.set_caption(localized_strings.title)
        gui.initialized = True
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
        p.player.mute()
    else:
        for child in gui.root[gui.current_page-1]:
            name = child.get("name")
            position = child.find("position")
            align = child.get("align")
            xy = None
            if position is not None:
                xy = (int(position.get("x")), int(position.get("y")))
            if child.tag in ["text", "rectangle", "scroll_text"]:
                color_node = child.find("color")
                color = (int(color_node.get("red")), int(color_node.get("green")), int(color_node.get("blue")))
                if child.tag == "text":
                    font_size = int(child.get("font_size"))
                    text = child.find("text").text
                    if name == "time":
                        text = gui.current_time
                    elif name == "date":
                        text = gui.current_date
                    elif name == "time_sep" and time.localtime().tm_sec%2 != 1:
                        continue
                    if gui.current_page == PAGE_INDEX_RADIO:
                        if child.get("name") == "station_name":
                            text = gui.radio_station_name_text + ''
                    screen.text(text, color=color, xy=xy, align=align, font_size=font_size)
                elif child.tag == "scroll_text":
                    font_size = int(child.get("font_size"))
                    text = child.find("text").text
                    hpos = int(child.get("hpos"))
                    margin_node = child.find("margin")
                    margin = (int(margin_node.get("left")), int(margin_node.get("right")))
                    if gui.current_page == PAGE_INDEX_RADIO:
                        if name == "station_info":
                            text = gui.radio_station_info_text + ''
                    if name not in gui.scroll_texts:
                        gui.scroll_texts[name] = ScrollText(screen.surface, 
                        text, hpos, color, margin, font_size,
                        font=os.path.join(os.path.dirname(inspect.getfile(tingbot)), 'Geneva.ttf'))
                    else:
                        gui.scroll_texts[name].update_text(text)
                        gui.scroll_texts[name].update()

                    
                elif child.tag == "rectangle":
                    size_node = child.find("size")
                    align = child.get("align")
                    size = (int(size_node.get("w")), int(size_node.get("h")))

                    screen.rectangle(xy=xy, size=size, color=color, align=align)
            elif child.tag == "image":
                scale = float(child.get("scale"))
                src = child.get("src")
                screen.image(src, xy=xy, scale=scale, align=align)
    #elif gui.current_page == PAGE_INDEX_RADIO:
    #    draw_radio_page()
    #elif gui.current_page == PAGE_INDEX_CLOCK:
    #    draw_clock_page()

# END: loop()

frontend = WebFrontend(port=config.WEB_FRONTENT_PORT)
frontend.serve()

settings_data = config.SETTINGS

with open(radio_config) as data_file:
    radio_data = json.load(data_file)

p = Radio(radio_channels=radio_data['channels'], mplayer_path=config.MPLAYER_PATH)
if "radio" in settings_data:
    _radio_settings = settings_data['radio']
    p.change_country(_radio_settings['country'])
    if "radio_stations" in _radio_settings and len(_radio_settings['radio_stations']) > 0:
        p.radio_channels.extend(_radio_settings['radio_stations'])

web_frontend.radio = p
alarm = Alarm("res/sounds/Argon_48k.wav", settings=settings_data)
alarm.create_alarms()

web_frontend.alarm = alarm

last_state = config.load_last_state()
if last_state is not None:
    p.set_channel(last_state["last_radio_station"])
    gui.current_page = last_state["last_page"]

tingbot.run(loop)
