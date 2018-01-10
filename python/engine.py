WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

# Screens
MENU = 0
LEVEL_SELECT = 1
IN_GAME = 2

NUM_LEVELS = 5

DOT_COLORS = [
    "#f00",
    "#0f0",
    "#00f",
    "#ff0",
    "#0ff",
    "#f0f",
    "#fff"
]

FILL_COLORS = [
    "#e00",
    "#0e0",
    "#00e",
    "#ee0",
    "#0ee",
    "#e0e",
    "#eee"
]


def get_board_setup(level=0):
    return 5, 10, [(0,0,1,1), (0,1,0,9)]
