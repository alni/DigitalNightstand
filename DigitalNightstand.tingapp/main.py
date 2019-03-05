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

import defs.colors as colors
import defs.weather_icons as wx_icons

from Alarm import Alarm
import WebFrontend as web_frontend
from WebFrontend import WebFrontend
from Weather import Weather
import gui
from gui import (
    FORECAST_ICON_CONDITION,
    FORECAST_LABEL_SUMMARY,
    FORECAST_LABEL_TEMPERATURE,
    FORECAST_LABEL_POWERED_BY,
    FORECAST_LINE_SEPARATOR,
    CLOCK_LABEL_TIME,
    CLOCK_LABEL_TIME_AMPM,
    CLOCK_LABEL_DATE,
    CLOCK_LABEL_ALARM_NEXT,
    ALARM_LABEL_TITLE,
    PAGE_INDEX_CLOCK,
    PAGE_INDEX_FORECAST,
    FORECAST_PAGE_LABEL_DAY1,
    FORECAST_PAGE_LABEL_DAY2,
    FORECAST_PAGE_LABEL_DAY3,
    FORECAST_PAGE_LABEL_DAY4,
    FORECAST_PAGE_LABEL_DAY5,
    FORECAST_PAGE_ICON_CONDITION_DAY1,
    FORECAST_PAGE_ICON_CONDITION_DAY2,
    FORECAST_PAGE_ICON_CONDITION_DAY3,
    FORECAST_PAGE_ICON_CONDITION_DAY4,
    FORECAST_PAGE_ICON_CONDITION_DAY5,
    FORECAST_PAGE_LABEL_TEMPERATURE_DAY1,
    FORECAST_PAGE_LABEL_TEMPERATURE_DAY2,
    FORECAST_PAGE_LABEL_TEMPERATURE_DAY3,
    FORECAST_PAGE_LABEL_TEMPERATURE_DAY4,
    FORECAST_PAGE_LABEL_TEMPERATURE_DAY5,
    DEFAULT_FONT
)
import config
import locales

from ScrollText import ScrollText

# Initialize global objects
frontend = None
alarm = None
weather = None
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
# current_locale = "en" # use while testing (comment out otherwise)

localized_strings = locales.get_locale(current_locale)
print localized_strings

current_tz = arrow.now().tzinfo

# Create a thread pool to keep the number of running threads to a minimum
thread_pool = ThreadPool(4)

@atexit.register
def clean_up():
    frontend.stop()
    config.save_last_state(
        last_page=gui.current_page
    )
    thread_pool.close()
    #pygame.quit()
    sys.exit()

@every(seconds=0.5)
def update():
    #local = arrow.now()
    # Every 500ms check for new alarms and update the current_time and 
    # current_date variables
    alarm.run_alarm()
    #gui.current_date = local.format('D MMMM YYYY', current_locale)
    ## time.strftime("%d %B %Y")
    #gui.current_time = local.format("HH mm", current_locale)
    ## time.strftime("%H %M")
    #gui.current_am_pm = local.format("a", current_locale)
    #if gui.current_am_pm == "":
    #    gui.current_am_pm = local.format("a")


@every(seconds=30)
def update_minor():
    # Every 30 seconds update the next_alarm, current_time and current_date 
    # variables
    local = arrow.now()
   
    gui.current_date = local.format('D MMMM YYYY', current_locale)
    # time.strftime("%d %B %Y")
    gui.current_time = local.format(config.CLOCK_TIME_FORMAT, current_locale)
    # time.strftime("%H %M")
    gui.current_am_pm = local.format("a", current_locale)
    if gui.current_am_pm == "":
        gui.current_am_pm = local.format("a")

    gui.next_alarm = localized_strings.get_alarm(None)
    if alarm.next_alarm() is not None:
        # Humanize the next alarm datetime to a string
        next_alarm_dt = arrow.get(alarm.next_alarm(), local.tzinfo)
        next_alarm_hm = next_alarm_dt.humanize(locale=current_locale)
        gui.next_alarm = localized_strings.get_alarm(next_alarm_hm)


@every(minutes=30)
@touch(
    xy=FORECAST_ICON_CONDITION["xy"],
    size=FORECAST_ICON_CONDITION["touch_size"],
    align=FORECAST_ICON_CONDITION["align"])
def update_weather(xy=None, action=None):
    # weather.create_forecast()
    print(weather)
    thread_pool.apply_async(weather.create_forecast, (5,))


@button.right_button.hold
def take_screenshot():
    thread_pool.apply_async(_take_screenshot2, ())

def _take_screenshot2():
    time.sleep(1)
    pygame.image.save(pygame.display.get_surface(), "screenshot.jpg")

@button.midright_button.up
def snooze_alarm():
    if alarm.current_alarm is not None:
        alarm.snooze_alarm(alarm.current_alarm, 1)
        alarm.stop_alarm()

@button.midright_button.hold
def stop_alarm():
    if alarm.current_alarm is not None:
        alarm.stop_alarm()


# Weather Forecast Summary Draw method
def draw_forecast_summary():
    if weather.type == "currently" and weather.currently is not None:
        screen.image(
            weather.get_icon_path(weather.currently),
            xy=FORECAST_ICON_CONDITION["xy"],
            scale=FORECAST_ICON_CONDITION["scale"],
            align=FORECAST_ICON_CONDITION["align"]
        )
        if gui.forecast_scroll_text_summary == None:
            gui.forecast_scroll_text_summary = ScrollText(
                surface=tingbot.screen.surface, 
                text=FORECAST_LABEL_SUMMARY["text"] % (weather.currently.summary),
                hpos=FORECAST_LABEL_SUMMARY["hpos"],
                color=FORECAST_LABEL_SUMMARY["color"],
                margin=FORECAST_LABEL_SUMMARY["margin"],
                size=FORECAST_LABEL_SUMMARY["font_size"],
                speed=2,
                font=DEFAULT_FONT
            )
        else:
            gui.forecast_scroll_text_summary.update_text(
                FORECAST_LABEL_SUMMARY["text"] % (weather.currently.summary)
            )
        gui.forecast_scroll_text_summary.update()
        #screen.text(
        #    FORECAST_LABEL_SUMMARY["text"] % (weather.currently.summary),
        #    xy=FORECAST_LABEL_SUMMARY["xy"],
        #    color=FORECAST_LABEL_SUMMARY["color"],
        #    font_size=FORECAST_LABEL_SUMMARY["font_size"],
        #    align=FORECAST_LABEL_SUMMARY["align"],
        #    font=DEFAULT_FONT
        #)
        screen.text(
            FORECAST_LABEL_TEMPERATURE["text"] % (weather.currently.temperature),
            xy=FORECAST_LABEL_TEMPERATURE["xy"],
            color=FORECAST_LABEL_TEMPERATURE["color"],
            font_size=FORECAST_LABEL_TEMPERATURE["font_size"],
            align=FORECAST_LABEL_TEMPERATURE["align"],
            font=DEFAULT_FONT
        )
    elif weather.type == "daily" and weather.daily is not None:
        screen.image(
            weather.get_icon_path(weather.daily.data[0]),
            xy=FORECAST_ICON_CONDITION["xy"],
            scale=FORECAST_ICON_CONDITION["scale"],
            align=FORECAST_ICON_CONDITION["align"]
        )
        if gui.forecast_scroll_text_summary == None:
            gui.forecast_scroll_text_summary = ScrollText(
                surface=tingbot.screen.surface, 
                text=FORECAST_LABEL_SUMMARY["text"] % (weather.daily.data[0].summary),
                hpos=FORECAST_LABEL_SUMMARY["hpos"],
                color=FORECAST_LABEL_SUMMARY["color"],
                margin=FORECAST_LABEL_SUMMARY["margin"],
                size=FORECAST_LABEL_SUMMARY["font_size"],
                speed=2,
                font=DEFAULT_FONT
            )
        else:
            gui.forecast_scroll_text_summary.update_text(
                FORECAST_LABEL_SUMMARY["text"] % (weather.daily.data[0].summary)
            )
        gui.forecast_scroll_text_summary.update()


        #screen.text(
        #    FORECAST_LABEL_SUMMARY["text"] % (weather.daily.data[0].summary),
        #    xy=FORECAST_LABEL_SUMMARY["xy"],
        #    color=FORECAST_LABEL_SUMMARY["color"],
        #    font_size=FORECAST_LABEL_SUMMARY["font_size"],
        #    align=FORECAST_LABEL_SUMMARY["align"],
        #    font=DEFAULT_FONT
        #)
        screen.text(
            FORECAST_LABEL_TEMPERATURE["text"] % (weather.daily.data[0].temperatureMax),
            xy=FORECAST_LABEL_TEMPERATURE["xy"],
            color=FORECAST_LABEL_TEMPERATURE["color"],
            font_size=FORECAST_LABEL_TEMPERATURE["font_size"],
            align=FORECAST_LABEL_TEMPERATURE["align"],
            font=DEFAULT_FONT
        )
    
    screen.text(
        localized_strings.fetching_new_data if weather.is_fetching else FORECAST_LABEL_POWERED_BY["text"],
        xy=FORECAST_LABEL_POWERED_BY["xy"],
        color=FORECAST_LABEL_POWERED_BY["color"],
        font_size=FORECAST_LABEL_POWERED_BY["font_size"],
        align=FORECAST_LABEL_POWERED_BY["align"],
        font=DEFAULT_FONT
    )
    screen.line(
        start_xy=FORECAST_LINE_SEPARATOR["start_xy"],
        end_xy=FORECAST_LINE_SEPARATOR["end_xy"],
        color=FORECAST_LINE_SEPARATOR["color"],
        width=FORECAST_LINE_SEPARATOR["width"]
    )

# Clock Page Draw method
def draw_clock_page():
    draw_forecast_summary()
    screen.text(
        gui.current_time,
        xy=CLOCK_LABEL_TIME["xy"],
        color=CLOCK_LABEL_TIME["color"],
        font_size=CLOCK_LABEL_TIME["font_size"],
        align=CLOCK_LABEL_TIME["align"],
        font=DEFAULT_FONT
    )
    if time.localtime().tm_sec%2 == 1:
        # Draw the time separator every other second (blink the separator)
        screen.text(
            ":",
            xy=CLOCK_LABEL_TIME["xy"],
            color=CLOCK_LABEL_TIME["color"],
            font_size=CLOCK_LABEL_TIME["font_size"],
            align=CLOCK_LABEL_TIME["align"],
            font=DEFAULT_FONT
        )
    if config.CLOCK_12H:
        screen.text(
            gui.current_am_pm,
            xy=CLOCK_LABEL_TIME_AMPM["xy"],
            color=CLOCK_LABEL_TIME_AMPM["color"],
            font_size=CLOCK_LABEL_TIME_AMPM["font_size"],
            align=CLOCK_LABEL_TIME_AMPM["align"],
            font=DEFAULT_FONT
        )

    screen.text(
        gui.current_date,
        xy=CLOCK_LABEL_DATE["xy"],
        color=CLOCK_LABEL_DATE["color"],
        font_size=CLOCK_LABEL_DATE["font_size"],
        align=CLOCK_LABEL_DATE["align"],
        font=DEFAULT_FONT
    )
    # next_alarm = "(no current alarms)"
    # next_alarm = localized_strings.get_alarm(None)
    # if alarm.next_alarm() is not None:
        # Humanize the next alarm datetime to a string
        # next_alarm_dt = arrow.get(alarm.next_alarm(), current_tz)
        # next_alarm = localized_strings.get_alarm(next_alarm_dt.humanize(locale=current_locale))
        # next_alarm = arrow.get(alarm.next_alarm()).humanize()
    # Draw the next alarm info on the bottom left of the the screen
    screen.text(
        gui.next_alarm,
        xy=CLOCK_LABEL_ALARM_NEXT["xy"],
        color=CLOCK_LABEL_ALARM_NEXT["color"],
        font_size=CLOCK_LABEL_ALARM_NEXT["font_size"],
        align=CLOCK_LABEL_ALARM_NEXT["align"],
        font=DEFAULT_FONT
    )

def init_forecast_page():
    day_format = u"ddd"
    temperature_format = u"%d°\n%d°"
    language = current_locale + ""
    if weather.settings is not None and "language" in weather.settings:
        language = weather.settings["language"]
        try:
            arrow.locales.get_locale(language)
        except Exception as err:
            print(err.message)
            language = current_locale + ""
    
    if weather.daily is not None:
        daily = weather.daily.data
        label_day1_text = ""
        label_day2_text = ""
        label_day3_text = ""
        label_day4_text = ""
        label_day5_text = ""

        label_temp_day1_text = ""
        label_temp_day2_text = ""
        label_temp_day3_text = ""
        label_temp_day4_text = ""
        label_temp_day5_text = ""

        icon_day1 = ""
        icon_day2 = ""
        icon_day3 = ""
        icon_day4 = ""
        icon_day5 = ""

        day1_time = weather.get_local_time(daily[0])
        day1_temp_min = daily[0].temperatureMin
        day1_temp_max = daily[0].temperatureMax

        label_day1_text = day1_time.format(day_format, language)
        FORECAST_PAGE_LABEL_DAY1["text"] = label_day1_text

        label_temp_day1_text = temperature_format % (day1_temp_min, day1_temp_max)
        FORECAST_PAGE_LABEL_TEMPERATURE_DAY1["text"] = label_temp_day1_text
        
        icon_day1 = daily[0].icon
        FORECAST_PAGE_ICON_CONDITION_DAY1["icon"] = icon_day1


        day2_time = weather.get_local_time(daily[1])
        day2_temp_min = daily[1].temperatureMin
        day2_temp_max = daily[1].temperatureMax

        label_day2_text = day2_time.format(day_format, language)
        FORECAST_PAGE_LABEL_DAY2["text"] = label_day2_text

        label_temp_day2_text = temperature_format % (day2_temp_min, day2_temp_max)
        FORECAST_PAGE_LABEL_TEMPERATURE_DAY2["text"] = label_temp_day2_text
        
        icon_day2 = daily[1].icon
        FORECAST_PAGE_ICON_CONDITION_DAY2["icon"] = icon_day2


        day3_time = weather.get_local_time(daily[2])
        day3_temp_min = daily[2].temperatureMin
        day3_temp_max = daily[2].temperatureMax

        label_day3_text = day3_time.format(day_format, language)
        FORECAST_PAGE_LABEL_DAY3["text"] = label_day3_text

        label_temp_day3_text = temperature_format % (day3_temp_min, day3_temp_max)
        FORECAST_PAGE_LABEL_TEMPERATURE_DAY3["text"] = label_temp_day3_text
        
        icon_day3 = daily[2].icon
        FORECAST_PAGE_ICON_CONDITION_DAY3["icon"] = icon_day3


        day4_time = weather.get_local_time(daily[3])
        day4_temp_min = daily[3].temperatureMin
        day4_temp_max = daily[3].temperatureMax

        label_day4_text = day4_time.format(day_format, language)
        FORECAST_PAGE_LABEL_DAY4["text"] = label_day4_text

        label_temp_day4_text = temperature_format % (day4_temp_min, day4_temp_max)
        FORECAST_PAGE_LABEL_TEMPERATURE_DAY4["text"] = label_temp_day4_text
        
        icon_day4 = daily[3].icon
        FORECAST_PAGE_ICON_CONDITION_DAY4["icon"] = icon_day4


        day5_time = weather.get_local_time(daily[4])
        day5_temp_min = daily[4].temperatureMin
        day5_temp_max = daily[4].temperatureMax

        label_day5_text = day5_time.format(day_format, language)
        FORECAST_PAGE_LABEL_DAY5["text"] = label_day5_text

        label_temp_day5_text = temperature_format % (day5_temp_min, day5_temp_max)
        FORECAST_PAGE_LABEL_TEMPERATURE_DAY5["text"] = label_temp_day5_text
        
        icon_day5 = daily[4].icon
        FORECAST_PAGE_ICON_CONDITION_DAY5["icon"] = icon_day5

def draw_forecast_page():
    draw_forecast_summary()

    screen.text(
        FORECAST_PAGE_LABEL_DAY1["text"],
        xy=FORECAST_PAGE_LABEL_DAY1["xy"],
        color=FORECAST_PAGE_LABEL_DAY1["color"],
        font_size=FORECAST_PAGE_LABEL_DAY1["font_size"],
        align=FORECAST_PAGE_LABEL_DAY1["align"],
        font=DEFAULT_FONT
    )

    screen.text(
        FORECAST_PAGE_LABEL_DAY2["text"],
        xy=FORECAST_PAGE_LABEL_DAY2["xy"],
        color=FORECAST_PAGE_LABEL_DAY2["color"],
        font_size=FORECAST_PAGE_LABEL_DAY2["font_size"],
        align=FORECAST_PAGE_LABEL_DAY2["align"],
        font=DEFAULT_FONT
    )

    screen.text(
        FORECAST_PAGE_LABEL_DAY3["text"],
        xy=FORECAST_PAGE_LABEL_DAY3["xy"],
        color=FORECAST_PAGE_LABEL_DAY3["color"],
        font_size=FORECAST_PAGE_LABEL_DAY3["font_size"],
        align=FORECAST_PAGE_LABEL_DAY3["align"],
        font=DEFAULT_FONT
    )

    screen.text(
        FORECAST_PAGE_LABEL_DAY4["text"],
        xy=FORECAST_PAGE_LABEL_DAY4["xy"],
        color=FORECAST_PAGE_LABEL_DAY4["color"],
        font_size=FORECAST_PAGE_LABEL_DAY4["font_size"],
        align=FORECAST_PAGE_LABEL_DAY4["align"],
        font=DEFAULT_FONT
    )

    screen.text(
        FORECAST_PAGE_LABEL_DAY5["text"],
        xy=FORECAST_PAGE_LABEL_DAY5["xy"],
        color=FORECAST_PAGE_LABEL_DAY5["color"],
        font_size=FORECAST_PAGE_LABEL_DAY5["font_size"],
        align=FORECAST_PAGE_LABEL_DAY5["align"],
        font=DEFAULT_FONT
    )

    screen.image(
        # weather.get_icon_path(weather.currently),
        weather.get_icon_path(icon=FORECAST_PAGE_ICON_CONDITION_DAY1["icon"]),
        xy=FORECAST_PAGE_ICON_CONDITION_DAY1["xy"],
        scale=FORECAST_PAGE_ICON_CONDITION_DAY1["scale"],
        align=FORECAST_PAGE_ICON_CONDITION_DAY1["align"]
    )

    screen.image(
        # weather.get_icon_path(weather.currently),
        weather.get_icon_path(icon=FORECAST_PAGE_ICON_CONDITION_DAY2["icon"]),
        xy=FORECAST_PAGE_ICON_CONDITION_DAY2["xy"],
        scale=FORECAST_PAGE_ICON_CONDITION_DAY2["scale"],
        align=FORECAST_PAGE_ICON_CONDITION_DAY2["align"]
    )

    screen.image(
        # weather.get_icon_path(weather.currently),
        weather.get_icon_path(icon=FORECAST_PAGE_ICON_CONDITION_DAY3["icon"]),
        xy=FORECAST_PAGE_ICON_CONDITION_DAY3["xy"],
        scale=FORECAST_PAGE_ICON_CONDITION_DAY3["scale"],
        align=FORECAST_PAGE_ICON_CONDITION_DAY3["align"]
    )

    screen.image(
        # weather.get_icon_path(weather.currently),
        weather.get_icon_path(icon=FORECAST_PAGE_ICON_CONDITION_DAY4["icon"]),
        xy=FORECAST_PAGE_ICON_CONDITION_DAY4["xy"],
        scale=FORECAST_PAGE_ICON_CONDITION_DAY4["scale"],
        align=FORECAST_PAGE_ICON_CONDITION_DAY4["align"]
    )

    screen.image(
        # weather.get_icon_path(weather.currently),
        weather.get_icon_path(icon=FORECAST_PAGE_ICON_CONDITION_DAY5["icon"]),
        xy=FORECAST_PAGE_ICON_CONDITION_DAY5["xy"],
        scale=FORECAST_PAGE_ICON_CONDITION_DAY5["scale"],
        align=FORECAST_PAGE_ICON_CONDITION_DAY5["align"]
    )

    screen.text(
        FORECAST_PAGE_LABEL_TEMPERATURE_DAY1["text"],
        xy=FORECAST_PAGE_LABEL_TEMPERATURE_DAY1["xy"],
        color=FORECAST_PAGE_LABEL_TEMPERATURE_DAY1["color"],
        font_size=FORECAST_PAGE_LABEL_TEMPERATURE_DAY1["font_size"],
        align=FORECAST_PAGE_LABEL_TEMPERATURE_DAY1["align"],
        font=DEFAULT_FONT
    )

    screen.text(
        FORECAST_PAGE_LABEL_TEMPERATURE_DAY2["text"],
        xy=FORECAST_PAGE_LABEL_TEMPERATURE_DAY2["xy"],
        color=FORECAST_PAGE_LABEL_TEMPERATURE_DAY2["color"],
        font_size=FORECAST_PAGE_LABEL_TEMPERATURE_DAY2["font_size"],
        align=FORECAST_PAGE_LABEL_TEMPERATURE_DAY2["align"],
        font=DEFAULT_FONT
    )

    screen.text(
        FORECAST_PAGE_LABEL_TEMPERATURE_DAY3["text"],
        xy=FORECAST_PAGE_LABEL_TEMPERATURE_DAY3["xy"],
        color=FORECAST_PAGE_LABEL_TEMPERATURE_DAY3["color"],
        font_size=FORECAST_PAGE_LABEL_TEMPERATURE_DAY3["font_size"],
        align=FORECAST_PAGE_LABEL_TEMPERATURE_DAY3["align"],
        font=DEFAULT_FONT
    )

    screen.text(
        FORECAST_PAGE_LABEL_TEMPERATURE_DAY4["text"],
        xy=FORECAST_PAGE_LABEL_TEMPERATURE_DAY4["xy"],
        color=FORECAST_PAGE_LABEL_TEMPERATURE_DAY4["color"],
        font_size=FORECAST_PAGE_LABEL_TEMPERATURE_DAY4["font_size"],
        align=FORECAST_PAGE_LABEL_TEMPERATURE_DAY4["align"],
        font=DEFAULT_FONT
    )

    screen.text(
        FORECAST_PAGE_LABEL_TEMPERATURE_DAY5["text"],
        xy=FORECAST_PAGE_LABEL_TEMPERATURE_DAY5["xy"],
        color=FORECAST_PAGE_LABEL_TEMPERATURE_DAY5["color"],
        font_size=FORECAST_PAGE_LABEL_TEMPERATURE_DAY5["font_size"],
        align=FORECAST_PAGE_LABEL_TEMPERATURE_DAY5["align"],
        font=DEFAULT_FONT
    )

def set_current_page(val):
    if gui.last_touch == -1 or time.time() - gui.last_touch > 1:
        # only switch page if there is more than 1 second since last page change
        gui.last_touch = time.time() # set last page change to current time
        gui.current_page = val
        return True
    return False

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
    xy=FORECAST_LABEL_SUMMARY["touch_xy"],
    size=FORECAST_LABEL_SUMMARY["touch_size"],
    align=FORECAST_LABEL_SUMMARY["align"])
def on_touch_clock_datetime(xy, action):
    print(action + " | " + str(gui.current_page) + " (" + str(PAGE_INDEX_CLOCK) + ")")
    if action == 'down':
        if gui.current_page == PAGE_INDEX_CLOCK:
            if set_current_page(PAGE_INDEX_FORECAST):
                init_forecast_page()
        else:
            set_current_page(PAGE_INDEX_CLOCK)

# BEGIN: loop()
@every(seconds=0.100)
def loop():
    if not gui.initialized:
        if config.MOUSE_VISIBLE:
            pygame.mouse.set_visible(config.MOUSE_VISIBLE)
        pygame.display.set_caption(localized_strings.title)
        gui.initialized = True

    screen.fill(
        color=colors.COLOR_BLUE_DARK
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
            align=ALARM_LABEL_TITLE["align"],
            font=DEFAULT_FONT
        )
    elif gui.current_page == gui.PAGE_INDEX_CLOCK:
        draw_clock_page()
    elif gui.current_page == gui.PAGE_INDEX_FORECAST:
        # TODO: Implement Forecast Page
        draw_forecast_page()
        # draw_clock_page() # Forecast currently not implemented

# END: loop()

frontend = WebFrontend(port=config.WEB_FRONTEND_PORT)
frontend.serve()

settings_data = config.SETTINGS

alarm = Alarm("res/sounds/Argon_48k.wav", settings=settings_data)
alarm.create_alarms()

weather = Weather(settings=settings_data)
# weather = Weather() # use while testing (comment out otherwise)
# update_weather()

web_frontend.alarm = alarm
web_frontend.weather = weather

def run_loop(): return

tingbot.run(run_loop)
# tingbot.run(loop)
