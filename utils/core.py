import displayio
import terminalio
import os
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from utils.settings import PAGE_DIR

def setup_oled_group(macropad):
    group = displayio.Group()
    for key_index in range(12):
        x = key_index % 3
        y = key_index // 3
        group.append(
            label.Label(
                terminalio.FONT,
                text="",
                color=0xFFFFFF,
                anchored_position=(
                    (macropad.display.width - 1) * x / 2,
                    macropad.display.height - 1 - (3 - y) * 12,
                ),
                anchor_point=(x / 2, 1.0),
            )
        )
    group.append(Rect(0, 0, macropad.display.width, 12, fill=0xFFFFFF))
    group.append(
        label.Label(
            terminalio.FONT,
            text="",
            color=0x000000,
            anchored_position=(macropad.display.width // 2, -2),
            anchor_point=(0.5, 0.0),
        )
    )

    return group


def find_page(pages, target):
    for page in pages:
        if page.name == target:
            return page

    return None


def scan_for_page_files():
    files = os.listdir(PAGE_DIR)
    for file in files:
        if not file.endswith(".py"):
            files.pop(file)

    return files
