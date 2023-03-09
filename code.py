from utils.core import setup_oled_group, find_page, scan_for_page_files, display_on, display_off, screensaver
from utils.settings import PAGE_DIR, DEFAULT_PAGE
import os
from adafruit_macropad import MacroPad


class Page:

    def __init__(self, data):
        self.name = data["name"]
        self.macros = data["macros"]
        if data.get("custom_func") and callable(data["custom_func"]):
            self.custom = data["custom_func"]
        else:
            self.custom = None

    def activate(self):
        if self.custom:
            macropad.display.refresh()
            self.custom(macropad, position)
            macropad.display.show(oled_group)

        else:
            oled_group[13].text = self.name  # Page name

            for i in range(12):
                if i < len(self.macros):  # Key in use, set label + LED color
                    macropad.pixels[i] = self.macros[i][0]
                    oled_group[i].text = self.macros[i][1]
                else:  # Key not in use, no label or LED
                    macropad.pixels[i] = 0
                    oled_group[i].text = ""

        macropad.keyboard.release_all()
        macropad.consumer_control.release()
        macropad.mouse.release_all()
        macropad.stop_tone()
        macropad.pixels.show()
        macropad.display.refresh()

# Setup pad and display
macropad = MacroPad()
oled_group = setup_oled_group(macropad)
macropad.display.auto_refresh = False
macropad.pixels.auto_write = False
macropad.display.show(oled_group)
display_on(macropad)
display_powered = True
screensaver = screensaver()


# Grab and import pages
pages = []
files = scan_for_page_files()
for file in files:
    try:
        module = __import__(PAGE_DIR + "/" + file[:-3])
        pages.append(Page(module.page))
    except Exception as err:
        print(f"Error in {file}.")
        import traceback
        traceback.print_exception(err, err, err.__traceback__)

if not pages:
    oled_group[13].text = "NO PAGES FOUND"
    macropad.display.refresh()
    while True:
        pass


last_position = 0
last_encoder_switch = macropad.encoder_switch_debounced.pressed
# Always default to home page on startup
home_idx = find_page(pages,'Home')[1]
page_index = home_idx
pages[page_index].activate()

# MAIN LOOP ----------------------------

while True:
    # Check whether to switch off the display
    screensaver.poll()
    if screensaver.on and not display_powered:
        display_on(macropad)
        display_powered = True
    elif not screensaver.on and display_powered:
        display_off(macropad)
        display_powered = False
    # Read encoder position. If it's changed, switch pages.
    position = macropad.encoder
    custom_function_flag = False
    if position != last_position:
        screensaver.reset()
        if position < last_position:
            # Previous page
            page_index = (page_index - 1) % len(pages)
        else:
            # Next page
            page_index = (page_index + 1) % len(pages)

        if pages[page_index].custom:
            print(f'{pages[page_index].name} HAS CUSTOM FUNC')
            custom_function_flag = True

        last_position = position
        pages[page_index].activate()
        if custom_function_flag:
            #TODO: fix weirdness jumping out of custom functions
            print('did we just jump out of a custom func?')
    # Handle encoder button. If state has changed, and if there's a
    # corresponding macro, set up variables to act on this just like
    # the keypad keys, as if it were a 13th key/macro.
    macropad.encoder_switch_debounced.update()
    encoder_switch = macropad.encoder_switch_debounced.pressed
    if encoder_switch != last_encoder_switch:
        screensaver.reset()
        last_encoder_switch = encoder_switch
        if len(pages[page_index].macros) < 13:
            continue  # No 13th macro, just resume main loop
        key_number = 12  # else process below as 13th macro
        pressed = encoder_switch
    else:
        event = macropad.keys.events.get()
        if not event or event.key_number >= len(pages[page_index].macros):
            continue  # No key events, or no corresponding macro, resume loop
        key_number = event.key_number
        pressed = event.pressed

    # If code reaches here, a key or the encoder button WAS pressed/released
    # and there IS a corresponding macro available for it...other situations
    # are avoided by 'continue' statements above which resume the loop.
    screensaver.reset()
    sequence = pages[page_index].macros[key_number][2]
    if pressed:
        # 'sequence' is an arbitrary-length list, each item is one of:
        # Positive integer (e.g. Keycode.KEYPAD_MINUS): key pressed
        # Negative integer: (absolute value) key released
        # Float (e.g. 0.25): delay in seconds
        # String (e.g. "Foo"): corresponding keys pressed & released
        # List []: one or more Consumer Control codes (can also do float delay)
        # Dict {}: mouse buttons/motion (might extend in future)

        # Home page will only point to other pages. Special handling done here to switch pages.
        if pages[page_index].name == "Home":
            for item in sequence:
                for idx, page in enumerate(pages):
                    if page.name.lower() == item[0]:
                        page_index = idx
                        pages[page_index].activate()
        elif key_number == 12:
            # If encoder pressed on non home page, and no macro sequence found,
            # go to home page.
            if not sequence:
                page_index = home_idx
                pages[page_index].activate()

        else:
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
                    if "buttons" in item:
                        if item["buttons"] >= 0:
                            macropad.mouse.press(item["buttons"])
                        else:
                            macropad.mouse.release(-item["buttons"])
                    macropad.mouse.move(
                        item["x"] if "x" in item else 0,
                        item["y"] if "y" in item else 0,
                        item["wheel"] if "wheel" in item else 0,
                    )
                    if "tone" in item:
                        if item["tone"] > 0:
                            macropad.stop_tone()
                            macropad.start_tone(item["tone"])
                        else:
                            macropad.stop_tone()
                    elif "play" in item:
                        macropad.play_file(item["play"])
    else:
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
                if "buttons" in item:
                    if item["buttons"] >= 0:
                        macropad.mouse.release(item["buttons"])
                elif "tone" in item:
                    macropad.stop_tone()
        macropad.consumer_control.release()
        if key_number < 12:  # No pixel for encoder button
            macropad.pixels[key_number] = pages[page_index].macros[key_number][0]
            macropad.pixels.show()
