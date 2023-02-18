# Media Controls
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keycode import Keycode

page = {
    'name' : "Media",
    'macros' : [
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x000020, 'Vol-', [[ConsumerControlCode.VOLUME_DECREMENT]]),
        (0x200000, 'Mute', [[ConsumerControlCode.MUTE]]),
        (0x000020, 'Vol+', [[ConsumerControlCode.VOLUME_INCREMENT]]),
        # 2nd row ----------
        (0x000000, 'Min', [45*[ConsumerControlCode.VOLUME_DECREMENT]]),
        (0x000000, 'Lock', [Keycode.WINDOWS, Keycode.L]),
        (0x000000, 'Max', [50*[ConsumerControlCode.VOLUME_INCREMENT]]),
        # 3rd row ----------
        (0x000000, '<', [Keycode.LEFT_ARROW]),
        (0x000000, 'Seek', []),
        (0x000000, '>', [Keycode.RIGHT_ARROW]),
        # 4th row ----------
        (0x202000, '|<', [[ConsumerControlCode.SCAN_PREVIOUS_TRACK]]),
        (0x002000, 'Play/Pause', [[ConsumerControlCode.PLAY_PAUSE]]),
        (0x202000, '>|', [[ConsumerControlCode.SCAN_NEXT_TRACK]]),
        # Encoder button ---
        (0x000000, '', [])
    ]
}
