# Meow
import random
import time
import displayio
import adafruit_imageload
from adafruit_display_shapes.line import Line
from utils.bongo.bongo import Bongo


def Loop(macropad, last_position):
    bongo = Bongo()

    bongo.x = 40
    bongo.y = 15

    group = displayio.Group()
    group.append(bongo.group)

    macropad.display.show(group)

    macropad.pixels.fill((0,0,0))
    macropad.pixels.show()

    last_position = last_position

    while True:
        key_event = macropad.keys.events.get()
        bongo.update(key_event)
        macropad.display.refresh()

        position = macropad.encoder
        if position != last_position:
            return


page = {
    'name': 'Bongo',
    'macros': [],
    'custom_func': Loop
}
