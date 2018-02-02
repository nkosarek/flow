from Menu import Menu
from LevelSelect import LevelSelect
from Level import Level
from config import MENU, LEVEL_SELECT, LEVEL


class GameView:
    def __init__(self, root, state, window_width, window_height):
        self.root = root
        self.window_width = window_width
        self.window_height = window_height
        self.changing_window = False

        self.menu = Menu(state, root)
        self.level_select = LevelSelect(state, root)
        self.level = Level(state, root)

        self.menu.place(in_=root, x=0, y=0, relwidth=1, relheight=1)
        self.level_select.place(in_=root, x=0, y=0, relwidth=1, relheight=1)
        self.level.place(in_=root, x=0, y=0, relwidth=1, relheight=1)

        self._show_menu()

    def _show_menu(self):
        self.level.visible = False
        self.menu.show()

    def _show_level_select(self):
        self.level.visible = False
        self.level_select.show()

    def _redraw_level(self, state):
        self.level.update_and_show(state)

    def refresh_view(self, state):
        if state.modified:
            # TODO?: This is a race...
            state.modified = False
            if state.page == MENU:
                self._show_menu()
            elif state.page == LEVEL_SELECT:
                self._show_level_select()
            elif state.page == LEVEL:
                self._redraw_level(state)
        self.root.after(REFRESH_DELAY, self.refresh_view, state)
