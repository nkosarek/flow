# TODO: base game, click and drag away from button, button click highlight
# TODO: multiple levels, bridges, walls, custom boards, custom board validation

# TODO?: Space interface (dot space, bridge space, etc)

import Tkinter as tk
from engine import *


##########################################
# Controller
##########################################


### Mouse Events ###

def mouse_click(event, view, state):
    if state.in_game:
        view.redraw_in_game(state)


# TODO: only redraw sometimes
def mouse_drag(event, view, state):
    if state.in_game:
        view.redraw_in_game(state)


def mouse_release(event, view, state):
    if state.in_game:
        if view.changing_window:
            view.changing_window = False
            view.redraw_in_game(state)
            return


### Button Events ###

def menu_play_button(view):
    view.show_level_select()


def level_select_back_to_menu(view):
    view.show_menu()


def level_select_level(view, state, level):
    state.start_level(level)
    view.redraw_in_game(state)


### Window Events ###

def window_change(view, state):
    if state.in_game:
        view.changing_window = True


##########################################
# View
##########################################


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class Menu(Page):
    def __init__(self, view, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        label = tk.Label(self, text="Flow")
        label.pack()

        button = tk.Button(self, text="Play",
                           command=lambda: menu_play_button(view))
        button.pack()


class LevelSelect(Page):
    def __init__(self, view, state, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        label = tk.Label(self, text="Level Select")
        label.pack()

        for level in xrange(NUM_LEVELS):
            button = tk.Button(self, text="%s" % level,
                               command=lambda lvl=level: level_select_level(view, state, lvl))
            button.pack()


class InGame(Page):
    def __init__(self, view, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.label = tk.Label(self)
        self.label.pack()

        self.canvas = tk.Canvas(self, bg="#888")
        self.canvas.pack(fill="both", expand=True)
        self.visible = False

    def update_and_show(self, state):
        self.label.config(text="Level %d" % state.level)
        self.canvas.delete(tk.ALL)

        InGame._draw_board(self.canvas, state)

        self.canvas.update()
        if not self.visible:
            self.show()
            self.visible = True

    @staticmethod
    def _draw_board(canvas, state):
        rows, cols = state.board.rows, state.board.cols
        board_dimen = InGame._get_board_dimensions(canvas.winfo_width(),
                                                   canvas.winfo_height(),
                                                   rows,
                                                   cols)
        board_x0, board_y0, space_width = board_dimen

        for row in xrange(rows):
            for col in xrange(cols):
                x0 = board_x0 + col * space_width
                y0 = board_y0 + row * space_width
                x1 = x0 + space_width
                y1 = y0 + space_width
                canvas.create_rectangle(x0, y0, x1, y1, fill="black", outline="white")

    @staticmethod
    def _get_board_dimensions(canvas_width, canvas_height, rows, cols):
        space_width = 50
        width_left = -1
        height_left = -1
        while (width_left < 0 or height_left < 0) and space_width >= 10:
            space_width -= 5
            board_width = space_width * cols
            board_height = space_width * rows
            width_left = canvas_width - board_width
            height_left = canvas_height - board_height

        board_x0 = width_left/2
        board_y0 = height_left/2
        return board_x0, board_y0, space_width


class GameView:
    def __init__(self, root, state, window_width, window_height):
        self.root = root
        self.window_width = window_width
        self.window_height = window_height
        self.changing_window = False

        self.menu = Menu(self, root)
        self.level_select = LevelSelect(self, state, root)
        self.in_game = InGame(self, root)

        self.menu.place(in_=root, x=0, y=0, relwidth=1, relheight=1)
        self.level_select.place(in_=root, x=0, y=0, relwidth=1, relheight=1)
        self.in_game.place(in_=root, x=0, y=0, relwidth=1, relheight=1)

        self.show_menu()

    def show_menu(self):
        self.in_game.visible = False
        self.menu.show()

    def show_level_select(self):
        self.in_game.visible = False
        self.level_select.show()

    def redraw_in_game(self, state):
        self.in_game.update_and_show(state)


##########################################
# Model
##########################################


class Space:
    def __init__(self):
        self.dot = None
        self.selected = False
        self.fill = None

    def set_dot(self, dot):
        self.dot = dot

    def has_dot(self):
        return self.dot is not None


class Board:
    def __init__(self, rows, cols, dots):
        self.rows = rows
        self.cols = cols
        self.spaces = Board._create_spaces(rows, cols, dots)

    @staticmethod
    def _create_spaces(rows, cols, dots):
        # Create board of spaces
        spaces = []
        for _ in xrange(rows):
            row = []
            for _ in xrange(cols):
                row.append(Space())
            spaces.append(row)

        # Place appropriate dots in board spaces
        for dotIndex in xrange(len(dots)):
            (dot_row0, dot_col0, dot_row1, dot_col1) = dots[dotIndex]
            spaces[dot_row0][dot_col0].set_dot(dotIndex)
            spaces[dot_row1][dot_col1].set_dot(dotIndex)

        return spaces


class GameState:
    def __init__(self):
        self.in_game = False
        self.board = None
        self.level = None

    def start_level(self, level):
        self.in_game = True
        self.level = level
        rows, cols, dots = get_board_setup(level)
        self.board = Board(rows, cols, dots)


##########################################
# Main
##########################################


def main():

    root = tk.Tk()

    state = GameState()

    view = GameView(root, state, WINDOW_WIDTH, WINDOW_HEIGHT)

    root.bind("<Button-1>", lambda event: mouse_click(event, view, state))
    root.bind("<B1-Motion>", lambda event: mouse_drag(event, view, state))
    root.bind("<ButtonRelease-1>", lambda event: mouse_release(event, view, state))
    root.bind("<Configure>", lambda event: window_change(view, state))

    root.wm_geometry("%sx%s" % (WINDOW_WIDTH, WINDOW_HEIGHT))
    root.mainloop()

main()
