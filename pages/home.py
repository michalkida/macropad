# Test home page
from adafruit_hid.consumer_control_code import ConsumerControlCode
from utils.core import scan_for_page_files

files = scan_for_page_files()
print(files)
files.remove("home.py")
macros = []

for i in range(0,12):
    if i < len(files):
        macros.append((0x000020, files[i][:-3], [[files[i][:-3]]]))
    else:
        macros.append((0x000040, '-', []))

page = {
    'name' : "Home",
    'macros': macros,

}
