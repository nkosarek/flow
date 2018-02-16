# Default window dimensions

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

# Page constants

MENU = 0
LEVEL_SELECT = 1
LEVEL = 2

# Dot/Pipe Color Constants

DOT_COLORS = [
    "#f00",
    "#0f0",
    "#00f",
    "#ff0",
    "#0ff",
    "#f0f",
    "#fff"
]

PIPE_COLORS = [
    "#c00",
    "#0c0",
    "#00c",
    "#cc0",
    "#0cc",
    "#c0c",
    "#ccc"
]

CURR_PIPE_SPACE_COLORS = DOT_COLORS

OVERWRITE_PIPE_COLORS = [
    "#c00",
    "#0c0",
    "#00c",
    "#cc0",
    "#0cc",
    "#c0c",
    "#ccc"
]

# Board sizes and dot locations for each level

BOARD_SETUP = [
    (5, 5, [(0,0,3,1), (0,4,4,3), (1,2,1,4), (3,3,4,0)]),
    (6, 6, [(0,0,1,5), (1,4,4,4), (4,1,5,5), (4,3,5,4)]),
    (7, 7, [(0,1,5,4), (0,3,1,1), (0,4,2,4), (0,6,4,4), (1,4,5,1)]),
    (8, 8, [(0,0,6,1), (1,0,2,5), (1,6,6,6), (2,6,3,5), (5,4,7,3)]),
    (12, 12, [(2,2,3,7), (2,7,8,3), (4,5,11,7), (4,6,11,5), (4,7,11,4), (6,6,11,0), (8,2,10,5)])
]

NUM_LEVELS = len(BOARD_SETUP)

# Level complete constants

LEVEL_INCOMPLETE = 0
LEVEL_COMPLETE = 1
LEVEL_PERFECT = 2

# Delay constant for refresh_view

REFRESH_DELAY = 40  # ms
