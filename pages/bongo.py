# Meow
import displayio
from utils.bongo.bongo import Bongo

# Built once at startup: loading the sprite sheet takes ~350 ms.
bongo = Bongo()
bongo.x = 40
bongo.y = 15
group = displayio.Group()
group.append(bongo.group)


def enter(macropad):
    macropad.display.root_group = group
    macropad.pixels.fill(0)


def update(macropad, key_event):
    if bongo.update(key_event):
        macropad.display.refresh()


page = {
    'name': 'Bongo',
    'macros': [],
    'enter': enter,
    'update': update,
}
