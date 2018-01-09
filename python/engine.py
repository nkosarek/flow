WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

# Screens
MENU = 0
LEVEL_SELECT = 1
IN_GAME = 2

NUM_LEVELS = 5


def get_board_setup(level=0):
    print level
    return 5, 5, [(0,0,1,1)]
