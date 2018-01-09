# TODO: base game, click and drag away from button, button click highlight
# TODO: multiple levels, bridges, walls, custom boards, custom board validation

# TODO?: Space interface (dot space, bridge space, etc)

import Tkinter as tk
from engine import *


##########################################
# Controller
##########################################


### Mouse Event Wrappers ###

def mouse_click_wrapper(event, view, state):
    if state.in_game:
        mouse_click(event, view, state)
        view.redraw_in_game(state)


def mouse_drag_wrapper(event, view, state):
    if state.in_game:
        mouse_drag(event, view, state)
        view.redraw_in_game(state)


def mouse_release_wrapper(event, view, state):
    if state.in_game:
        mouse_release(event, view, state)
        view.redraw_in_game(state)


### Mouse Events ###

def mouse_click(event, view, state):
    pass


def mouse_drag(event, view, state):
    pass


def mouse_release(event, view, state):
    pass


### Button Events ###

def menu_play_button(view):
    view.show_level_select()


def level_select_back_to_menu(view):
    view.show_menu()


def level_select_level(view, state, level):
    state.start_level(level)
    view.redraw_in_game(state)


### Window Events ###
# TODO: remove? maybe unnecessary

#def window_change_wrapper(event, view, state):
#    window_change(event, view)
#    if state.in_game:
#        view.redraw_in_game(state)


#def window_change(event, view):
#    view.window_width = event.width
#    view.window_height = event.height
#    view.resize_board()


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

        self.canvas_width = view.window_width/2
        self.canvas_height = view.window_height/2
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)
        self.visible = False

    def update_and_show(self, view, state):
        self.label.config(text="Level %d" % state.level)
        self.canvas.delete(tk.ALL)
        InGame._draw_board(self.canvas, view, state)
        self.canvas.update()
        if not self.visible:
            self.show()
            self.visible = True

    @staticmethod
    def _draw_board(canvas, view, state):
        space_width = 20
        canvas.create_rectangle(0,0,20,20, fill="black")


class GameView:
    def __init__(self, root, state, window_width, window_height):
        self.root = root
        self.window_width = window_width
        self.window_height = window_height

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
        self.in_game.update_and_show(self, state)



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
    @staticmethod
    def _create_spaces(height, width, dots):
        # Create board of spaces
        spaces = []
        for _ in xrange(height):
            row = []
            for _ in xrange(width):
                row.append(Space())
            spaces.append(row)

        # Place appropriate dots in board spaces
        for dotIndex in xrange(len(dots)):
            (dot_y0, dot_x0, dot_y1, dot_x1) = dots[dotIndex]
            spaces[dot_y0][dot_x0].set_dot(dotIndex)
            spaces[dot_y1][dot_x1].set_dot(dotIndex)

        return spaces

    def __init__(self, height, width, dots):
        self.spaces = Board._create_spaces(height, width, dots)


class GameState:
    def __init__(self):
        self.in_game = False
        self.board = None
        self.level = None

    def start_level(self, level):
        self.level = level
        height, width, dots = get_board_setup(level)
        self.board = Board(height, width, dots)


##########################################
# Main
##########################################


def main():

    root = tk.Tk()

    state = GameState()

    view = GameView(root, state, WINDOW_WIDTH, WINDOW_HEIGHT)

    root.bind("<Button-1>", lambda event: mouse_click_wrapper(event, view, state))
    root.bind("<B1-Motion>", lambda event: mouse_drag_wrapper(event, view, state))
    root.bind("<ButtonRelease-1>", lambda event: mouse_release_wrapper(event, view, state))
#    root.bind("<Configure>", lambda event: window_change_wrapper(event, view, state))

    root.wm_geometry("%sx%s" % (WINDOW_WIDTH, WINDOW_HEIGHT))
    root.mainloop()

main()
