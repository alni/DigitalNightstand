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
    config.save_last_state(
        last_page=gui.current_page
    )
    thread_pool.close()
    pygame.quit()
    sys.exit()

@every(seconds=0.5)
def update():
    local = arrow.now()
    # Every 500ms check for new alarms and update the current_time and 
    # current_date variables
    alarm.run_alarm()
    gui.current_date = local.format('D MMMM YYYY', current_locale)
    # time.strftime("%d %B %Y")
    gui.current_time = local.format("HH mm", current_locale)
    # time.strftime("%H %M")

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

# Clock Page DateTime touch event - switch to the Forecast Page
@touch(
    xy=CLOCK_LABEL_TIME["touch_xy"],
    size=CLOCK_LABEL_TIME["touch_size"],
    align=CLOCK_LABEL_TIME["align"])
def on_touch_clock_datetime(xy, action):
    if action == 'down' and gui.current_page == PAGE_INDEX_CLOCK:
        set_current_page(PAGE_INDEX_FORECAST)


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
        "res/images/delicate-arch-960279_240p.jpg",
        xy=(160,0),
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
    elif gui.current_page == gui.PAGE_INDEX_CLOCK or True:
        draw_clock_page()
    elif gui.current_page == gui.PAGE_INDEX_FORECAST:
        # TODO: Implement Forecast Page
        draw_clock_page() # Forecast currently not implemented

# END: loop()

frontend = WebFrontend(port=config.WEB_FRONTENT_PORT)
frontend.serve()

settings_data = config.SETTINGS

alarm = Alarm("res/sounds/Argon_48k.wav", settings=settings_data)
alarm.create_alarms()

web_frontend.alarm = alarm

tingbot.run(loop)
