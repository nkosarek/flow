from Menu import Menu
from LevelSelect import LevelSelect
from Level import Level


class GameView:
    def __init__(self, root, state, window_width, window_height):
        self.root = root
        self.window_width = window_width
        self.window_height = window_height
        self.changing_window = False

        self.menu = Menu(self, root)
        self.level_select = LevelSelect(self, state, root)
        self.level = Level(root)

        self.menu.place(in_=root, x=0, y=0, relwidth=1, relheight=1)
        self.level_select.place(in_=root, x=0, y=0, relwidth=1, relheight=1)
        self.level.place(in_=root, x=0, y=0, relwidth=1, relheight=1)

        self.show_menu()

    def show_menu(self):
        self.level.visible = False
        self.menu.show()

    def show_level_select(self):
        self.level.visible = False
        self.level_select.show()

    def redraw_level(self, state):
        self.level.update_and_show(state)
