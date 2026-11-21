# macropad
Code for my Adafruit RP2040 Macropad (CircuitPython 10.x).

The encoder switches pages (order set by `PAGE_ORDER` in `utils/settings.py`); pressing it goes to the Home page.

## Media page
Volume, mute, play/pause and previous/next are standard media keys and work on any computer.
Min/Max volume and Spotify seek send F19/F24 (with Shift for seek), which a small helper on the computer turns into actions:

| Key | Sends | Action |
|---|---|---|
| Min | F19 | volume 0% |
| Max | F24 | unmute, volume 100% |
| Seek- | Shift+F19 | Spotify seek back |
| Seek+ | Shift+F24 | Spotify seek forward |
| Lock | Win+Alt+L | lock screen (matches my KDE lock shortcut; the AHK script locks Windows) |

- **Windows:** run `host/windows/macropad.ahk` with AutoHotkey v1 (put a shortcut to it in `shell:startup`).
- **Linux (KDE Plasma):** run `host/linux/install-kde.sh` once (`--uninstall` removes it). Needs `wpctl` and `playerctl`.

## Updating
Copy `code.py`, `pages/`, `utils/` and `lib/` to the CIRCUITPY drive. Libraries are listed in `requirements.txt`; update them with `circup update`.
