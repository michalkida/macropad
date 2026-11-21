# Home page: one key per page, in PAGE_ORDER, that jumps to it.
from utils.settings import COLOURS, HOME_PAGE, PAGE_ORDER

targets = [name for name in PAGE_ORDER if name != HOME_PAGE]
macros = []

for i in range(12):
    if i < len(targets):
        macros.append((COLOURS['GREEN'], targets[i], [{"page": targets[i]}]))
    else:
        macros.append((COLOURS['RED'], '-', []))

page = {
    'name': HOME_PAGE,
    'macros': macros,
}
