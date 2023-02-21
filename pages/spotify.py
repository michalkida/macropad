# Spotify Controls
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keycode import Keycode

"""
Spotify has different volume control. Thats about it.
If I can add current song stats on the macropad here one day,
that'd be pretty neat.
"""

page = {
    'name' : "Spotify",
    'macros' : [
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x000000, '', []),
        (0x000000, '', []),
        (0x000000, '', []),
        # 2nd row ----------
        (0x000020, 'Vol-', [Keycode.F15]),
        (0x200000, 'Mute', [[ConsumerControlCode.MUTE]]),
        (0x000020, 'Vol+', [Keycode.F14]),
        # 3rd row ----------
        (0x000000, '<', [Keycode.CONTROL, Keycode.SHIFT, Keycode.LEFT_ARROW]),
        (0x000000, 'Seek', []),
        (0x000000, '>', [Keycode.CONTROL, Keycode.SHIFT, Keycode.RIGHT_ARROW]),
        # 4th row ----------
        (0x202000, '|<', [[ConsumerControlCode.SCAN_PREVIOUS_TRACK]]),
        (0x002000, 'Play/Pause', [Keycode.F16]),
        (0x202000, '>|', [[ConsumerControlCode.SCAN_NEXT_TRACK]]),
        # Encoder button ---
        (0x000000, '', [])
    ]

}
