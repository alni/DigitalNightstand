import inspect, os, sys

import xml.etree.ElementTree as ET

import tingbot
from tingbot import screen

sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from ScrollText import ScrollText

tree = ET.parse(os.path.dirname(inspect.getfile(inspect.currentframe())) +  "/pages.xml")
root = tree.getroot()

scroll_texts = {}

def loop():
    for child in root[0]:
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

                screen.text(text, color=color, xy=xy, align=align, font_size=font_size)
            elif child.tag == "scroll_text":
                font_size = int(child.get("font_size"))
                text = child.find("text").text
                hpos = int(child.get("hpos"))
                margin_node = child.find("margin")
                margin = (int(margin_node.get("left")), int(margin_node.get("right")))
                if name not in scroll_texts:
                    scroll_texts[name] = ScrollText(screen.surface, 
                    text, hpos, color, margin, font_size,
                    font=os.path.join(os.path.dirname(inspect.getfile(tingbot)), 'Geneva.ttf'))
                else:
                    scroll_texts[name].update_text(text)
                    scroll_texts[name].update()
            elif child.tag == "rectangle":
                size_node = child.find("size")
                align = child.get("align")
                size = (int(size_node.get("w")), int(size_node.get("h")))

                screen.rectangle(xy=xy, size=size, color=color, align=align)
        elif child.tag == "image":
            scale = float(child.get("scale"))
            src = child.get("src")
            screen.image(src, xy=xy, scale=scale, align=align)

tingbot.run(loop)
