from typing import List, TYPE_CHECKING

from change_theme import ThemeApi

if TYPE_CHECKING:
    from ghosts.core import MainGhost

coop = 0
instant_win = 0
god = 0
debug = 0
datetime_format = "%d.%m.%Y %H:%M:%S"
orange_trigger = 0
blue_trigger = 0
difficulty = 1
easter = 0
dots = 0
pacs = []
cell_size = 16
ghosts: List["MainGhost"] = []
theme_api = ThemeApi()
