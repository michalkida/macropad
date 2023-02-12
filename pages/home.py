# Test home page
from adafruit_hid.consumer_control_code import ConsumerControlCode
from utils.core import scan_for_page_files
from utils.settings import COLOURS

files = scan_for_page_files()
print(files)
files.remove("home.py")
macros = []

for i in range(0,12):
    if i < len(files):
        macros.append((COLOURS['GREEN'], files[i][:-3], [[files[i][:-3]]]))
    else:
        macros.append((COLOURS['RED'], '-', []))

page = {
    'name' : "Home",
    'macros': macros,

}
