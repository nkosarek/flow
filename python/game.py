# TODO: Dot select then immediate unselect, dots block pipes
# TODO: No pipe continue after correct dot, pipe autocomplete after dot block
# TODO: Game completion, perfect game, next/restart/last buttons
# TODO: back to menu button in level select and game, stats page

# TODO?: Space interface (dot space, bridge space, etc)

# TODO: click and drag away from button doesn't click button
# TODO: bridges, walls, custom boards, custom board validation


import Tkinter as tk
from engine import *


##########################################
# Controller
##########################################


### Mouse Events ###

def mouse_click(event, view, state):
    if not state.in_game:
        return

    space = view.in_game.selected_space(event, state.board)
    if space is None or (space.dot is None and space.fill is None):
        state.curr_selected_space = None
        return

    state.curr_selected_space = space
    if space.dot is not None:
        if space.fill is None or space.fill.next_space is None:
            Board.clear_pipe(space.dot.other)
        else:
            Board.clear_pipe(space)

        space.set_fill(space.dot.index)

    elif space.fill is not None:
        color = space.fill.color
        Board.clear_pipe(space)
        space.set_fill(color)

    view.redraw_in_game(state)


# TODO: only redraw sometimes
def mouse_drag(event, view, state):
    if not state.in_game:
        return

    new_space = view.in_game.selected_space(event, state.board)
    old_space = state.curr_selected_space
    if new_space is None or old_space is None or\
            new_space == old_space or old_space.fill is None or\
            (new_space.row != old_space.row and
             new_space.col != old_space.col):
        return

    old_space.set_next_space(new_space)
    color = old_space.fill.color
    Board.clear_pipe(new_space)
    new_space.set_fill(color)
    state.curr_selected_space = new_space

    view.redraw_in_game(state)


def mouse_release(event, view, state):
    if state.in_game:
        if view.changing_window:
            view.changing_window = False
            view.redraw_in_game(state)
            return

        curr_sel = state.curr_selected_space
        release_space = view.in_game.selected_space(event, state.board)
        if curr_sel is not None and release_space == curr_sel and\
                release_space.dot is not None:
            dot = release_space.dot
            if dot.other.fill is None:
                Board.clear_pipe(release_space)
                state.curr_selected_space = None
                view.redraw_in_game(state)


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
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.label = tk.Label(self)
        self.label.pack()

        self.canvas = tk.Canvas(self, bg="#888")
        self.canvas.pack(fill="both", expand=True)
        self.visible = False

        self.board_x0 = 0
        self.board_y0 = 0
        self.space_width = 50

    def selected_space(self, event, board):
        row = (event.y - self.board_y0)/self.space_width
        col = (event.x - self.board_x0)/self.space_width
        if row < 0 or row >= board.rows or col < 0 or col >= board.cols:
            return None
        else:
            return board.spaces[row][col]

    def update_and_show(self, state):
        self.label.config(text="Level %d" % state.level)
        self.canvas.delete(tk.ALL)

        self._draw_board(self.canvas, state)

        self.canvas.update()
        if not self.visible:
            self.show()
            self.visible = True

    def _draw_board(self, canvas, state):
        rows, cols = state.board.rows, state.board.cols
        board_dimen = InGame._get_board_dimensions(canvas.winfo_width(),
                                                   canvas.winfo_height(),
                                                   rows,
                                                   cols)
        self.board_x0, self.board_y0, self.space_width = board_dimen

        for row in xrange(rows):
            for col in xrange(cols):
                space = state.board.spaces[row][col]
                x0 = self.board_x0 + col * self.space_width
                y0 = self.board_y0 + row * self.space_width
                x1 = x0 + self.space_width
                y1 = y0 + self.space_width

                fill = space.fill
                if fill is None:
                    canvas.create_rectangle(x0, y0, x1, y1,
                                            fill="black", outline="white")
                else:
                    canvas.create_rectangle(x0, y0, x1, y1,
                                            fill=FILL_COLORS[fill.color], outline="white")

                dot = space.dot
                if dot is not None:
                    canvas.create_oval(x0+2, y0+2, x1-2, y1-2, fill=DOT_COLORS[dot.index])

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
        self.in_game = InGame(root)

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


class Fill:
    def __init__(self, color):
        self.color = color
        self.next_space = None


class Dot:
    def __init__(self, index, other):
        self.index = index
        self.other = other


class Space:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.dot = None
        self.fill = None

    def set_dot(self, index, other):
        self.dot = Dot(index, other)

    def set_fill(self, color):
        self.fill = Fill(color)

    def set_next_space(self, next_space):
        assert self.fill is not None
        self.fill.next_space = next_space

    def clear_fill(self):
        if self.fill is None:
            return None
        next_space = self.fill.next_space
        self.fill = None
        return next_space


class Board:
    def __init__(self, rows, cols, dots):
        self.rows = rows
        self.cols = cols
        self.spaces = Board._create_spaces(rows, cols, dots)

    @staticmethod
    def clear_pipe(start_space):
        curr_space = start_space
        while curr_space is not None:
            curr_space = curr_space.clear_fill()

    @staticmethod
    def _create_spaces(rows, cols, dots):
        # Create board of spaces
        spaces = []
        for r in xrange(rows):
            row = []
            for c in xrange(cols):
                row.append(Space(r, c))
            spaces.append(row)

        # Place appropriate dots in board spaces
        for dot_index in xrange(len(dots)):
            (dot_row0, dot_col0, dot_row1, dot_col1) = dots[dot_index]
            dot_space0 = spaces[dot_row0][dot_col0]
            dot_space1 = spaces[dot_row1][dot_col1]
            dot_space0.set_dot(dot_index, dot_space1)
            dot_space1.set_dot(dot_index, dot_space0)

        return spaces


class GameState:
    def __init__(self):
        self.in_game = False
        self.board = None
        self.level = None
        self.curr_selected_space = None

    def start_level(self, level):
        self.in_game = True
        self.level = level
        (rows, cols, dots) = BOARD_SETUP[level]
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
