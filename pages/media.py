# Media Controls
# Volume, mute and track keys are standard media keys and work anywhere.
# Min/Max/Seek send F19/F24 (+Shift), which the computer turns into actions:
#   Windows: host/windows/macropad.ahk    Linux (KDE): host/linux/install-kde.sh
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
        (0x000000, 'Min', [Keycode.F19]),                   # volume 0%
        (0x000000, 'Lock', [Keycode.WINDOWS, Keycode.ALT, Keycode.L]),  # KDE lock; AHK on Windows
        (0x000000, 'Max', [Keycode.F24]),                   # unmute, volume 100%
        # 3rd row ----------
        (0x000020, 'Seek-', [Keycode.SHIFT, Keycode.F19]),  # Spotify back
        (0x000000, '', []),
        (0x000020, 'Seek+', [Keycode.SHIFT, Keycode.F24]),  # Spotify forward
        # 4th row ----------
        (0x202000, '|<', [[ConsumerControlCode.SCAN_PREVIOUS_TRACK]]),
        (0x002000, 'Play/Pause', [[ConsumerControlCode.PLAY_PAUSE]]),
        (0x202000, '>|', [[ConsumerControlCode.SCAN_NEXT_TRACK]]),
        # Encoder button ---
        (0x000000, '', [])
    ]
}
