from defs.colors import *

current_page = 1
last_touch = -1
last_key_down = -1.0
last_key_pressed = None
initialized = False

current_date = ""
current_time = ""

PAGE_INDEX_CLOCK = 1
PAGE_INDEX_FORECAST = 2

_ICON_BASE_PATH = "res/icons/material-design-icons-2.0/"
_FONT_BASE_PATH = "res/fonts/"

DEFAULT_FONT = _FONT_BASE_PATH + "Open_Sans/OpenSans-Regular.ttf"


CLOCK_LABEL_TIME = {
    "type": "text",
    "xy": (160, 110),
    "color": COLOR_WHITE, # COLOR_BLUE_LIGHT,
    "font_size": 85,
    "align": "center",
    "text": "%H %M",
    "touch_xy": (8, 0),
    "touch_size": (304, 68)
}

CLOCK_LABEL_DATE = {
    "type": "text",
    "xy": (160, 180),
    "color": COLOR_WHITE, # COLOR_TAN,
    "font_size": 24,
    "align": "center",
    "text": "%d %B %Y"
}

CLOCK_LABEL_ALARM_NEXT = {
    "type": "text",
    "xy": (20, 220),
    "color": COLOR_WHITE, # COLOR_BLUE_LIGHT,
    "font_size": 14,
    "align": "topleft",
    "text": "Next alarm %s"
}

ALARM_LABEL_TITLE = {
    "type": "text",
    "xy": (160, 110),
    "color": COLOR_WHITE, # COLOR_BLUE_LIGHT,
    "font_size": 50,
    "align": "center",
    "touch_size": (160, 120),
    "text": "%s"
}


FORECAST_ICON_CONDITION = {
    "xy": (256,0),
    "scale": 0.4210526315789474,
    "align": "topleft"
}

FORECAST_LABEL_SUMMARY = {
    "type": "text",
    "xy": (256, 32),
    "color": COLOR_WHITE, # COLOR_BLUE_LIGHT,
    "font_size": 24,
    "align": "right",
    "text": u"%s : %d°"
}

FORECAST_LINE_SEPARATOR = {
    "type": "line",
    "start_xy": (0, 64),
    "end_xy": (320, 64),
    "color": COLOR_WHITE, # COLOR_BLUE_LIGHT,
    "width": 2,
    "align": "topleft",
}