from defs.colors import *

current_page = 1
last_touch = -1

current_date = ""
current_time = ""

radio_info_scroll_text = None

PAGE_INDEX_RADIO = 1
PAGE_INDEX_CLOCK = 2

RADIO_PAGE_CLOCK_LABEL_TIME = {
    "type": "text",
    "xy": (160, 20),
    "color": COLOR_BLUE_LIGHT,
    "font_size": 40,
    "align": "center",
    "text": "%H %M"
}

RADIO_PAGE_CLOCK_LABEL_DATE = {
    "type": "text",
    "xy": (160, 50),
    "color": COLOR_TAN,
    "font_size": 20,
    "align": "center",
    "text": "%d %B %Y"
}

RADIO_PAGE_INFO_RECTANGLE_BORDER = {
    "type": "rectangle",
    "xy": (8, 70),
    "size": (304, 108),
    "color": COLOR_TAN,
    "align": "topleft"
}

RADIO_PLAYER_BUTTON_CHANNEL_PREV = {
    "type": "image",
    "xy": (24,32),
    "scale": 0.75,
    "align": "left",
    "touch_size": (32,32),
    "src": "res/icons/material-design-icons-2.0/navigation/2x_web/ic_chevron_left_white_18dp.png"
}

RADIO_PLAYER_BUTTON_CHANNEL_NEXT = {
    "type": "image",
    "xy": (272,32),
    "scale": 0.75,
    "align": "left",
    "touch_size": (32,32),
    "src": "res/icons/material-design-icons-2.0/navigation/2x_web/ic_chevron_right_white_18dp.png"
}


RADIO_PLAYER_LABEL_CHANNEL = {
    "type": "text",
    "xy": (160, 32),
    "color": COLOR_WHITE,
    "font_size": 16,
    "align": "center",
    "text": "%s"
}

RADIO_PLAYER_LABEL_INFO = {
    "type": "text",
    "xy": (160, 52),
    "color": COLOR_TAN,
    "font_size": 16,
    "align": "center",
    "text": " %s"
}


CLOCK_LABEL_TIME = {
    "type": "text",
    "xy": (160, 110),
    "color": COLOR_BLUE_LIGHT,
    "font_size": 85,
    "align": "center",
    "text": "%H %M"
}

CLOCK_LABEL_DATE = {
    "type": "text",
    "xy": (160, 180),
    "color": COLOR_TAN,
    "font_size": 24,
    "align": "center",
    "text": "%d %B %Y"
}

CLOCK_LABEL_ALARM_NEXT = {
    "type": "text",
    "xy": (20, 220),
    "color": COLOR_BLUE_LIGHT,
    "font_size": 14,
    "align": "topleft",
    "text": "Next alarm %s"
}

ALARM_LABEL_TITLE = {
    "type": "text",
    "xy": (160, 110),
    "color": COLOR_BLUE_LIGHT,
    "font_size": 50,
    "align": "center",
    "touch_size": (160, 120),
    "text": "%s"
}
