from utils.core import setup_oled_group, scan_for_page_files, display_on, display_off, screensaver
from utils.settings import PAGE_DIR, PAGE_ORDER, HOME_PAGE
import time
from adafruit_macropad import MacroPad


class Page:
    """
    A page is either a macro page (labels + LED colours + key sequences), or a
    custom page that provides 'enter' (called when switched to) and 'update'
    (called every main loop pass with that pass's key event, or None).
    """

    def __init__(self, data):
        self.name = data["name"]
        self.macros = data.get("macros", [])
        self.enter = data.get("enter")
        self.update = data.get("update")

    def activate(self):
        global hid_used
        if hid_used:  # Each release sends a USB report (~8 ms), so only when needed
            macropad.keyboard.release_all()
            macropad.consumer_control.release()
            macropad.mouse.release_all()
            hid_used = False
        macropad.stop_tone()

        if self.enter:
            self.enter(macropad)
        else:
            set_label(13, self.name)  # Page name
            for i in range(12):
                if i < len(self.macros):  # Key in use, set label + LED color
                    macropad.pixels[i] = self.macros[i][0]
                    set_label(i, self.macros[i][1])
                else:  # Key not in use, no label or LED
                    macropad.pixels[i] = 0
                    set_label(i, "")
            macropad.display.root_group = oled_group

        macropad.pixels.show()
        macropad.display.refresh()


def set_label(i, text):
    # Setting .text re-renders the label (~2 ms each), so skip unchanged ones
    if oled_group[i].text != text:
        oled_group[i].text = text


def load_pages():
    """Import every page file, return the pages listed in PAGE_ORDER, in that order."""
    by_name = {}
    for file in scan_for_page_files():
        try:
            module = __import__(PAGE_DIR + "/" + file[:-3])
            page = Page(module.page)
            by_name[page.name] = page
        except Exception as err:
            print(f"Error in {file}.")
            import traceback
            traceback.print_exception(err, err, err.__traceback__)

    ordered = []
    for name in PAGE_ORDER:
        if name in by_name:
            ordered.append(by_name.pop(name))
        else:
            print(f"PAGE_ORDER: no page named {name!r}")
    for name in by_name:
        print(f"Page {name!r} not in PAGE_ORDER, not shown")
    return ordered


def page_index_of(name):
    for idx, page in enumerate(pages):
        if page.name == name:
            return idx
    return None


def switch_to(idx):
    global page_index
    page_index = idx
    pages[page_index].activate()


def run_press(key_number, sequence):
    """
    'sequence' is an arbitrary-length list, each item is one of:
    Positive integer (e.g. Keycode.KEYPAD_MINUS): key pressed
    Negative integer: (absolute value) key released
    Float (e.g. 0.25): delay in seconds
    String (e.g. "Foo"): corresponding keys pressed & released
    List []: one or more Consumer Control codes (can also do float delay)
    Dict {}: mouse buttons/motion, tone, play file, or {"page": name} to switch page
    """
    global hid_used
    hid_used = True
    if key_number < 12:  # No pixel for encoder button
        macropad.pixels[key_number] = 0xFFFFFF
        macropad.pixels.show()
    for item in sequence:
        if isinstance(item, int):
            if item >= 0:
                macropad.keyboard.press(item)
            else:
                macropad.keyboard.release(-item)
        elif isinstance(item, float):
            time.sleep(item)
        elif isinstance(item, str):
            macropad.keyboard_layout.write(item)
        elif isinstance(item, list):
            for code in item:
                if isinstance(code, int):
                    macropad.consumer_control.release()
                    macropad.consumer_control.press(code)
                if isinstance(code, float):
                    time.sleep(code)
        elif isinstance(item, dict):
            if "page" in item:
                idx = page_index_of(item["page"])
                if idx is None:
                    print(f"No page named {item['page']!r}")
                else:
                    switch_to(idx)
                return  # Page changed; rest of this sequence no longer applies
            if "buttons" in item:
                if item["buttons"] >= 0:
                    macropad.mouse.press(item["buttons"])
                else:
                    macropad.mouse.release(-item["buttons"])
            if "x" in item or "y" in item or "wheel" in item:
                macropad.mouse.move(item.get("x", 0), item.get("y", 0), item.get("wheel", 0))
            if "tone" in item:
                if item["tone"] > 0:
                    macropad.stop_tone()
                    macropad.start_tone(item["tone"])
                else:
                    macropad.stop_tone()
            elif "play" in item:
                macropad.play_file(item["play"])


def run_release(key_number, sequence):
    # Release any still-pressed keys, consumer codes, mouse buttons
    # Keys and mouse buttons are individually released this way (rather
    # than release_all()) because pad supports multi-key rollover, e.g.
    # could have a meta key or right-mouse held down by one macro and
    # press/release keys/buttons with others. Navigate popups, etc.
    for item in sequence:
        if isinstance(item, int):
            if item >= 0:
                macropad.keyboard.release(item)
        elif isinstance(item, dict):
            if "buttons" in item and item["buttons"] >= 0:
                macropad.mouse.release(item["buttons"])
            if "tone" in item:
                macropad.stop_tone()
    macropad.consumer_control.release()
    if key_number < 12:  # No pixel for encoder button
        macropad.pixels[key_number] = pages[page_index].macros[key_number][0]
        macropad.pixels.show()


def handle_key(key_number, pressed):
    """Key 0-11 is a keypad key, 12 is the encoder button."""
    page = pages[page_index]
    if key_number < len(page.macros):
        sequence = page.macros[key_number][2]
    else:
        sequence = []

    # Encoder press with nothing assigned goes home
    if key_number == 12 and not sequence:
        if pressed and home_idx is not None and page_index != home_idx:
            switch_to(home_idx)
        return

    if key_number >= len(page.macros):
        return  # No macro for this key
    if pressed:
        run_press(key_number, sequence)
    else:
        run_release(key_number, sequence)


# Setup pad and display
macropad = MacroPad()
oled_group = setup_oled_group(macropad)
macropad.display.auto_refresh = False
macropad.pixels.auto_write = False
macropad.display.root_group = oled_group
display_on(macropad)
display_powered = True
saver = screensaver()
hid_used = False  # Set once a macro has sent anything over USB HID

pages = load_pages()

if not pages:
    oled_group[13].text = "NO PAGES FOUND"
    macropad.display.refresh()
    while True:
        pass

home_idx = page_index_of(HOME_PAGE)
page_index = home_idx if home_idx is not None else 0
pages[page_index].activate()
last_position = macropad.encoder
encoder_switch = macropad.encoder_switch_debounced

# MAIN LOOP ----------------------------

while True:
    # Check whether to switch off the display
    saver.poll()
    if saver.on and not display_powered:
        display_on(macropad)
        display_powered = True
    elif not saver.on and display_powered:
        display_off(macropad)
        display_powered = False

    # Encoder turned: move as many pages as it moved detents.
    position = macropad.encoder
    if position != last_position:
        saver.reset()
        switch_to((page_index + position - last_position) % len(pages))
        last_position = position

    # Encoder button, handled like a 13th key
    encoder_switch.update()
    if encoder_switch.fell:  # Pin goes low when pressed
        saver.reset()
        handle_key(12, True)
    elif encoder_switch.rose:
        saver.reset()
        handle_key(12, False)

    event = macropad.keys.events.get()
    if event:
        saver.reset()

    page = pages[page_index]
    if page.update:
        page.update(macropad, event)
    elif event:
        handle_key(event.key_number, event.pressed)
