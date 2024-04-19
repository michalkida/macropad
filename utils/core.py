import displayio
import terminalio
import os
import time
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from utils.settings import PAGE_DIR, SCREEN_TIMEOUT_MINUTES

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
    """
    Returns page object, index within page list.
    """
    for page in pages:
        if page.name == target:
            return page, pages.index(page)

    return None, None


def scan_for_page_files():
    files = os.listdir(PAGE_DIR)
    files = [file for file in files if file.endswith('.py') and not file.startswith('_')]

    return files


def display_on(macropad):
    macropad.display.bus.send(int(0xAF), "")


def display_off(macropad):
    macropad.display.bus.send(int(0xAE), "")


class screensaver:
    def __init__(self, duration=60 * SCREEN_TIMEOUT_MINUTES):
        self.duration = duration
        self.off_time = time.monotonic() + self.duration
        self.on = True

    def poll(self):
        if self.on:
            now = time.monotonic()
            if now >= self.off_time:
                self.on = False

    def reset(self):
        self.off_time = time.monotonic() + self.duration
        if not self.on:
            self.on = True

