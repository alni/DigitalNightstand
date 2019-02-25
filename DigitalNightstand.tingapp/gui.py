import defs.colors as colors

current_page = 1
last_touch = -1
last_key_down = -1.0
last_key_pressed = None
initialized = False

forecast_scroll_text_summary = None

current_date = ""
current_time = ""
current_am_pm = ""
next_alarm = ""

PAGE_INDEX_CLOCK = 1
PAGE_INDEX_FORECAST = 2

_ICON_BASE_PATH = "res/icons/material-design-icons-2.0/"
_FONT_BASE_PATH = "res/fonts/"

DEFAULT_FONT = _FONT_BASE_PATH + "Open_Sans/OpenSans-Regular.ttf"


CLOCK_LABEL_TIME = {
    "type": "text",
    "xy": (160, 110),
    "color": colors.COLOR_WHITE, # COLOR_BLUE_LIGHT,
    "font_size": 85,
    "align": "center",
    "text": "%H %M",
    "touch_xy": (8, 0),
    "touch_size": (304, 68)
}

CLOCK_LABEL_TIME_AMPM = {
    "type": "text",
    "xy": (308, 152),
    "color": colors.COLOR_WHITE, # COLOR_BLUE_LIGHT,
    "font_size": 24,
    "align": "bottomright"
}

CLOCK_LABEL_DATE = {
    "type": "text",
    "xy": (160, 180),
    "color": colors.COLOR_WHITE, # COLOR_TAN,
    "font_size": 24,
    "align": "center",
    "text": "%d %B %Y"
}

CLOCK_LABEL_ALARM_NEXT = {
    "type": "text",
    "xy": (4, 238),
    "color": colors.COLOR_WHITE, # COLOR_BLUE_LIGHT,
    "font_size": 14,
    "align": "bottomleft",
    "text": "Next alarm %s"
}

ALARM_LABEL_TITLE = {
    "type": "text",
    "xy": (160, 110),
    "color": colors.COLOR_WHITE, # COLOR_BLUE_LIGHT,
    "font_size": 50,
    "align": "center",
    "touch_size": (160, 120),
    "text": "%s"
}


FORECAST_ICON_CONDITION = {
    "xy": (256,0),
    "scale": 0.4210526315789474,
    "align": "topleft",
    "touch_xy": (256, 0),
    "touch_size": (64, 64)
}

FORECAST_LABEL_SUMMARY = {
    "type": "text",
    "xy": (250, 16),
    "color": colors.COLOR_WHITE, # COLOR_BLUE_LIGHT,
    "font_size": 19,
    "hpos": 6,
    "margin": (6, 70),
    "align": "right",
    "text": u"%s"
}

FORECAST_LABEL_TEMPERATURE = {
    "type": "text",
    "xy": (250, 44),
    "color": colors.COLOR_WHITE, # COLOR_BLUE_LIGHT,
    "font_size": 24,
    "align": "right",
    "text": u"%d°"
}

FORECAST_LABEL_POWERED_BY = {
    "type": "text",
    "xy": (4, 60),
    "color": colors.COLOR_WHITE, # COLOR_BLUE_LIGHT,
    "font_size": 14,
    "align": "bottomleft",
    "text": "Powered by Dark Sky"
}

FORECAST_LINE_SEPARATOR = {
    "type": "line",
    "start_xy": (0, 64),
    "end_xy": (320, 64),
    "color": colors.COLOR_WHITE, # COLOR_BLUE_LIGHT,
    "width": 2,
    "align": "topleft",
}


FORECAST_PAGE_LABEL_DAY1 = {
    "type": "text",
    "xy": (32, 68),
    "color": colors.COLOR_WHITE, # COLOR_BLUE_LIGHT,
    "font_size": 19,
    "align": "top",
    "text": "Day 1"
}

FORECAST_PAGE_LABEL_DAY2 = {
    "type": "text",
    "xy": (96, 68),
    "color": colors.COLOR_WHITE, # COLOR_BLUE_LIGHT,
    "font_size": 19,
    "align": "top",
    "text": "Day 2"
}

FORECAST_PAGE_LABEL_DAY3 = {
    "type": "text",
    "xy": (160, 68),
    "color": colors.COLOR_WHITE, # COLOR_BLUE_LIGHT,
    "font_size": 19,
    "align": "top",
    "text": "Day 3"
}

FORECAST_PAGE_LABEL_DAY4 = {
    "type": "text",
    "xy": (224, 68),
    "color": colors.COLOR_WHITE, # COLOR_BLUE_LIGHT,
    "font_size": 19,
    "align": "top",
    "text": "Day 4"
}

FORECAST_PAGE_LABEL_DAY5 = {
    "type": "text",
    "xy": (288, 68),
    "color": colors.COLOR_WHITE, # COLOR_BLUE_LIGHT,
    "font_size": 19,
    "align": "top",
    "text": "Day 5"
}


FORECAST_PAGE_ICON_CONDITION_DAY1 = {
    "xy": (32,95),
    "scale": 0.31578947368421052631578947368421,
    "align": "top",
    "touch_xy": (256, 0),
    "touch_size": (64, 64),
    "icon": "clear-day"
}

FORECAST_PAGE_ICON_CONDITION_DAY2 = {
    "xy": (96,95),
    "scale": 0.31578947368421052631578947368421,
    "align": "top",
    "touch_xy": (256, 0),
    "touch_size": (64, 64),
    "icon": "clear-day"
}

FORECAST_PAGE_ICON_CONDITION_DAY3 = {
    "xy": (160,95),
    "scale": 0.31578947368421052631578947368421,
    "align": "top",
    "touch_xy": (256, 0),
    "touch_size": (64, 64),
    "icon": "clear-day"
}

FORECAST_PAGE_ICON_CONDITION_DAY4 = {
    "xy": (224,95),
    "scale": 0.31578947368421052631578947368421,
    "align": "top",
    "touch_xy": (256, 0),
    "touch_size": (64, 64),
    "icon": "clear-day"
}

FORECAST_PAGE_ICON_CONDITION_DAY5 = {
    "xy": (288,95),
    "scale": 0.31578947368421052631578947368421,
    "align": "top",
    "touch_xy": (256, 0),
    "touch_size": (64, 64),
    "icon": "clear-day"
}


FORECAST_PAGE_LABEL_TEMPERATURE_DAY1 = {
    "type": "text",
    "xy": (32, 151),
    "color": colors.COLOR_WHITE, # COLOR_BLUE_LIGHT,
    "font_size": 16,
    "align": "top",
    "text": u"20°\n100°"
}

FORECAST_PAGE_LABEL_TEMPERATURE_DAY2 = {
    "type": "text",
    "xy": (96, 151),
    "color": colors.COLOR_WHITE, # COLOR_BLUE_LIGHT,
    "font_size": 16,
    "align": "top",
    "text": u"20°\n100°"
}

FORECAST_PAGE_LABEL_TEMPERATURE_DAY3 = {
    "type": "text",
    "xy": (160, 151),
    "color": colors.COLOR_WHITE, # COLOR_BLUE_LIGHT,
    "font_size": 16,
    "align": "top",
    "text": u"20°\n100°"
}

FORECAST_PAGE_LABEL_TEMPERATURE_DAY4 = {
    "type": "text",
    "xy": (224, 151),
    "color": colors.COLOR_WHITE, # COLOR_BLUE_LIGHT,
    "font_size": 16,
    "align": "top",
    "text": u"20°\n100°"
}

FORECAST_PAGE_LABEL_TEMPERATURE_DAY5 = {
    "type": "text",
    "xy": (288, 151),
    "color": colors.COLOR_WHITE, # COLOR_BLUE_LIGHT,
    "font_size": 16,
    "align": "top",
    "text": u"20°\n100°"
}
