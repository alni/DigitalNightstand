import xml.etree.ElementTree as ET

from defs.colors import *

current_page = 1
last_touch = -1
last_key_down = -1.0
last_key_pressed = None
initialized = False

current_date = ""
current_time = ""

scroll_texts = {}

radio_station_name_text = ''
radio_station_info_text = ''
radio_info_scroll_text = None

tree = ET.parse("data/gui/pages.xml")
root = tree.getroot()

def get_event_node(name, page_index=1, node_name="touch"):
    node = root[page_index-1].findall(".//*[@name='{0}']/{1}".format(name, node_name))
    if node and len(node) > 0:
        node = node[0]
    else:
        node  = None
    return node


def gen_event_object(node_name, page_index=1):
    event_object = {}
    touch_node = get_event_node(node_name, page_index, "touch")
    align = touch_node.get("align")
    position = touch_node.find("position")
    touch_xy = (int(position.get("x")), int(position.get("y")))
    size = touch_node.find("size")
    touch_size = (int(size.get("w")), int(size.get("h")))

    event_object["touch_xy"] = touch_xy
    event_object["touch_size"] = touch_size
    event_object["align"] = align

    button_node = get_event_node(node_name, page_index, "button")
    if button_node is not None:
        button = button_node.get("name")
        event_object["button"] = button

    return event_object


def should_perform_radio_event(xy, action, alarm):
    # Default action: only perform if touch event "down" and at the radio page
    should_perform = action == 'down' and current_page == PAGE_INDEX_RADIO
    # Alternative action: if xy is not set (physical button press) then always perform
    should_perform = (should_perform) or xy is None
    # Condition: only perform if no current alarm is running (includes both default and
    # alternative actions)
    should_perform = (should_perform) and alarm.current_alarm is None
    return should_perform

PAGE_INDEX_RADIO = 1
PAGE_INDEX_CLOCK = 2

_ICON_BASE_PATH = "res/icons/material-design-icons-2.0/"

PAGE_RADIO_TOUCH_TIME = gen_event_object("time", PAGE_INDEX_RADIO)

PAGE_RADIO_BUTTON_PLAY = gen_event_object("btn_play", PAGE_INDEX_RADIO)
PAGE_RADIO_BUTTON_PAUSE = gen_event_object("btn_pause", PAGE_INDEX_RADIO)
PAGE_RADIO_BUTTON_STATION_PREV = gen_event_object("btn_station_prev", PAGE_INDEX_RADIO)
PAGE_RADIO_BUTTON_STATION_NEXT = gen_event_object("btn_station_next", PAGE_INDEX_RADIO)
PAGE_RADIO_BUTTON_VOL_DOWN = gen_event_object("btn_vol_down", PAGE_INDEX_RADIO)
PAGE_RADIO_BUTTON_VOL_UP = gen_event_object("btn_vol_up", PAGE_INDEX_RADIO)
PAGE_RADIO_BUTTON_VOL_MUTE = gen_event_object("btn_vol_mute", PAGE_INDEX_RADIO)


CLOCK_RADIO_TOUCH_TIME = gen_event_object("time", PAGE_INDEX_CLOCK)


PAGE_RADIO_TEXT_TIME = {
    "xy"         : (160, 20),
    "text"       :  "%H %M", 
    "color"      : COLOR_BLUE_LIGHT, 
    "font_size"  : 40, 
    "align"      : "center"
}

PAGE_RADIO_TEXT_DATE = {
    "xy"         : (160, 50),
    "text"       : "%d %B %Y", 
    "color"      : COLOR_TAN, 
    "font_size"  : 20, 
    "align"      : "center"
}

#PAGE_RADIO_TOUCH_TIME = {
#    "align"      : "topleft",
#    "touch_xy"   : (8,0),
#    "touch_size" : (304,68)
#}

PAGE_RADIO_RECT_INFO_PANEL_OUTER = {
    "xy"         : (8, 70),
    "size"       : (304, 108), 
    "color"      : COLOR_TAN, 
    "align"      : "topleft"
}

PAGE_RADIO_RECT_INFO_PANEL_TOP = {
    "xy"         : (10, 72),
    "size"       : (300, 69), 
    "color"      : COLOR_BLUE_DARK, 
    "align"      : "topleft"
}

PAGE_RADIO_RECT_INFO_PANEL_BOTTOM = {
    "xy"         : (10, 143),
    "size"       : (300, 33), 
    "color"      : COLOR_BLUE_DARK, 
    "align"      : "topleft"
}

PAGE_RADIO_TEXT_STATION_NAME = {
    "xy"         : (13, 143),
    "text"       : "", 
    "color"      : COLOR_TAN, 
    "font_size"  : 15, 
    "align"      : "topleft"
}

#PAGE_RADIO_BUTTON_PLAY = {
#    "xy"         : (21,81),
#    "scale"      : 1.0,
#    "align"      : "topleft",
#    "touch_xy"   : (20,80),
#    "touch_size" : (50,50),
#    "src"        : _ICON_BASE_PATH + "av/2x_web/ic_play_circle_outline_white_24dp.png"
#}

#PAGE_RADIO_BUTTON_PAUSE = {
#    "xy"         : (81,81),
#    "scale"      : 1.0,
#    "align"      : "topleft",
#    "touch_xy"   : (80,80),
#    "touch_size" : (50,50),
#    "src"        : _ICON_BASE_PATH + "av/2x_web/ic_pause_circle_outline_white_24dp.png"
#}

#PAGE_RADIO_BUTTON_STATION_PREV = {
#    "xy"         : (11,181),
#    "scale"      : 1.0,
#    "align"      : "topleft",
#    "touch_xy"   : (10,180),
#    "touch_size" : (50,50),
#    "src"        : _ICON_BASE_PATH + "av/2x_web/ic_skip_previous_white_24dp.png"
#}

#PAGE_RADIO_BUTTON_STATION_NEXT = {
#    "xy"         : (71,181),
#    "scale"      : 1.0,
#    "align"      : "topleft",
#    "touch_xy"   : (70,180),
#    "touch_size" : (50,50),
#    "src"        : _ICON_BASE_PATH + "av/2x_web/ic_skip_next_white_24dp.png"
#}

#PAGE_RADIO_BUTTON_VOL_DOWN = {
#    "xy"         : (131,181),
#    "scale"      : 1.0,
#    "align"      : "topleft",
#    "touch_xy"   : (130,180),
#    "touch_size" : (50,50),
#    "src"        : _ICON_BASE_PATH + "av/2x_web/ic_volume_down_white_24dp.png"
#}

#PAGE_RADIO_BUTTON_VOL_UP = {
#    "xy"         : (191,181),
#    "scale"      : 1.0,
#    "align"      : "topleft",
#    "touch_xy"   : (190,180),
#    "touch_size" : (50,50),
#    "src"        : _ICON_BASE_PATH + "av/2x_web/ic_volume_up_white_24dp.png"
#}

#PAGE_RADIO_BUTTON_VOL_MUTE = {
#    "xy"         : (251,181),
#    "scale"      : 1.0,
#    "align"      : "topleft",
#    "touch_xy"   : (250,180),
#    "touch_size" : (50,50),
#    "src"        : _ICON_BASE_PATH + "av/2x_web/ic_volume_mute_white_24dp.png"
#}


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
