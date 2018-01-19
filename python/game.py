###############################################################################
#
# Flow - Web game based on smart phone app "Flow Free"
#
# Author: Nicholas Kosarek
# Python Version 2.7
#
###############################################################################

# TODO: [REFACTOR]
# TODO: split this file for god's sake
# TODO: move state logic out of controller functions
# TODO: space methods to deal with pipe continue instead of in event handler
# TODO: engine.py isn't an engine, just config
# TODO: Rename GameView.in_game and InGame
# TODO?: Space interface (dot space, bridge space, etc)

# TODO: [FEATURES]
# TODO: pipe autocomplete
# TODO: Game completion; perfect game
# TODO: next/restart/last buttons
# TODO: back to menu button in level select and game
# TODO: stats page
# TODO: Do not clear crossed pipe until mouse release

# TODO: [STRETCH]
# TODO: click and drag away from button doesn't click button
# TODO: bridges, walls, custom boards, custom board validation
# TODO: multiplayer (race?)

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
    if space is None or (not space.has_dot() and not space.has_pipe()):
        state.curr_selected_space = None
        state.curr_pipe_space = None
        return

    state.curr_pipe_space = space
    state.curr_selected_space = space
    if space.has_dot():
        if not space.has_pipe() or space.is_pipe_end():
            Board.clear_pipe(space.get_other_dot_space())
        else:
            Board.clear_pipe(space.get_next_pipe_space())

        space.set_pipe(space.get_dot_color(), None)

    elif space.has_pipe():
        Board.clear_pipe(space.get_next_pipe_space())

    view.redraw_in_game(state)


def mouse_drag(event, view, state):
    if not state.in_game:
        return

    dst_space = view.in_game.selected_space(event, state.board)

    if state.attempt_pipe_advance(dst_space):
        view.redraw_in_game(state)


def mouse_release(event, view, state):
    if state.in_game:
        if view.changing_window:
            view.changing_window = False
            view.redraw_in_game(state)
            return

        curr_pipe_space = state.curr_pipe_space
        release_space = view.in_game.selected_space(event, state.board)
        if curr_pipe_space is not None and\
                release_space == curr_pipe_space and release_space.has_dot():
            other = release_space.get_other_dot_space()
            if not other.has_pipe():
                Board.clear_pipe(release_space)
                state.curr_selected_space = None
                state.curr_pipe_space = None
                view.redraw_in_game(state)
            elif state.check_level_complete():
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
        if state.level_complete:
            InGame._draw_level_complete(self.canvas, state)

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
                InGame._draw_space(canvas, space, x0, y0, x1, y1)

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

    @staticmethod
    def _draw_space(canvas, space, x0, y0, x1, y1):
        if not space.has_pipe():
            canvas.create_rectangle(x0, y0, x1, y1,
                                    fill="black", outline="white")
        else:
            canvas.create_rectangle(x0, y0, x1, y1,
                                    fill=PIPE_COLORS[space.get_pipe_color()], outline="white")

        if space.has_dot():
            color = space.get_dot_color()
            canvas.create_oval(x0+2, y0+2, x1-2, y1-2, fill=DOT_COLORS[color])

    @staticmethod
    def _draw_level_complete(canvas, state):
        canvas = canvas
        x = canvas.winfo_width()/2
        y = canvas.winfo_height()/2
        font_size = min(x/6, y/6)
        canvas.create_text(x, y, text="AHHHHH", font=('Helvetica', font_size),
                           anchor=tk.CENTER)


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


class Pipe:
    def __init__(self, color, last_space):
        self.color = color
        self.next_space = None
        self.last_space = last_space


class Dot:
    def __init__(self, color, other):
        self.color = color
        self.other = other


class Space:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.dot = None
        self.pipe = None

    ### DOT METHODS ###
    def set_dot(self, color, other):
        self.dot = Dot(color, other)

    def has_dot(self):
        return self.dot is not None

    def get_dot_color(self):
        assert self.has_dot()
        return self.dot.color

    def get_other_dot_space(self):
        assert self.has_dot()
        return self.dot.other

    ### PIPE METHODS ###
    def set_pipe(self, color, last_space):
        self.pipe = Pipe(color, last_space)

    def has_pipe(self):
        return self.pipe is not None

    def get_pipe_color(self):
        if self.has_pipe():
            return self.pipe.color
        else:
            return None

    def is_pipe_start(self):
        if self.has_pipe() and self.get_last_pipe_space() is None:
            assert self.has_dot()
            return True
        else:
            return False

    def is_pipe_end(self):
        return self.has_pipe() and self.get_next_pipe_space() is None

    def get_next_pipe_space(self):
        assert self.has_pipe()
        return self.pipe.next_space

    def set_next_pipe_space(self, next_space):
        assert self.has_pipe()
        self.pipe.next_space = next_space

    def clear_next_pipe_space(self):
        assert self.has_pipe()
        self.pipe.next_space = None

    def get_last_pipe_space(self):
        assert self.has_pipe()
        return self.pipe.last_space

    def clear_last_next_pipe_space(self):
        if not self.has_pipe() or self.is_pipe_start():
            return
        assert self.get_last_pipe_space().has_pipe()
        self.get_last_pipe_space().clear_next_pipe_space()

    def clear_pipe(self):
        if not self.has_pipe():
            return None
        next_space = self.get_next_pipe_space()
        self.pipe = None
        return next_space


class Board:
    def __init__(self, rows, cols, dots):
        self.rows = rows
        self.cols = cols
        self.spaces = Board._create_spaces(rows, cols, dots)

    def autocomplete_pipe(self, src_space, dst_space):
        assert src_space != dst_space
        assert not src_space.has_dot() or src_space.is_pipe_start()
        if Board.adjacent_spaces(src_space, dst_space):
            if not dst_space.has_dot():
                Board.clear_pipe(dst_space)
                src_space.set_next_pipe_space(dst_space)
                dst_space.set_pipe(src_space.get_pipe_color(), src_space)
                return True, dst_space
            elif Board.compatible_dot(dst_space, src_space):
                src_space.set_next_pipe_space(dst_space)
                dst_space.set_pipe(src_space.get_pipe_color(), src_space)
                return True, dst_space
        return False, src_space

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
        for color_index in xrange(len(dots)):
            (dot_row0, dot_col0, dot_row1, dot_col1) = dots[color_index]
            dot_space0 = spaces[dot_row0][dot_col0]
            dot_space1 = spaces[dot_row1][dot_col1]
            dot_space0.set_dot(color_index, dot_space1)
            dot_space1.set_dot(color_index, dot_space0)

        return spaces

    @staticmethod
    def clear_pipe(start_space):
        curr_space = start_space
        if curr_space is not None:
            curr_space.clear_last_next_pipe_space()
        while curr_space is not None:
            curr_space = curr_space.clear_pipe()

    @staticmethod
    def adjacent_spaces(space0, space1):
        if space0.row == space1.row:
            col_diff = space0.col - space1.col
            if col_diff == 1 or col_diff == -1:
                return True
        elif space0.col == space1.col:
            row_diff = space0.row - space1.row
            if row_diff == 1 or row_diff == -1:
                return True
        else:
            return False

    @staticmethod
    def compatible_dot(dot_space, curr_space):
        assert dot_space is not None
        assert curr_space is not None
        assert curr_space.has_pipe()

        if dot_space.has_dot() and\
                curr_space.get_pipe_color() != dot_space.get_dot_color():
            return False
        else:
            return True

    @staticmethod
    def illegal_space_after_dot(new_space, old_space):
        if new_space is None or old_space is None or not old_space.has_dot() or\
                not old_space.has_pipe() or old_space.is_pipe_start():
            return False

        # If pipe has reached second dot, it cannot continue past that dot.
        if old_space.get_last_pipe_space() != new_space:
            return True
        else:
            return False


class GameState:
    def __init__(self):
        self.in_game = False
        self.board = None
        self.level = None
        self.curr_selected_space = None
        self.curr_pipe_space = None
        self.level_complete = False

    def start_level(self, level):
        self.in_game = True
        self.level = level
        (rows, cols, dots) = BOARD_SETUP[level]
        self.board = Board(rows, cols, dots)

    def attempt_pipe_advance(self, dst_space):
        last_selected_space = self.curr_selected_space
        src_pipe_space = self.curr_pipe_space

        pipe_modified = False
        # Not currently advancing a pipe
        if src_pipe_space is None:
            self.curr_selected_space = None

        # Mouse hasn't moved to a different space
        elif dst_space == last_selected_space:
            pass

        # Mouse is outside of board
        elif dst_space is None:
            self.curr_selected_space = None
            self.curr_pipe_space = None

        # Mouse has returned to a space in the currently advancing pipe
        elif dst_space.get_pipe_color() == src_pipe_space.get_pipe_color():
            assert dst_space.has_pipe()
            if not dst_space.is_pipe_end():
                Board.clear_pipe(dst_space.get_next_pipe_space())
            self.curr_pipe_space = dst_space
            self.curr_selected_space = dst_space
            pipe_modified = True

        # Mouse has gone past the second dot space after completing a pipe
        elif src_pipe_space.has_dot() and not src_pipe_space.is_pipe_start():
            pass

        # Attempt to connect the pipe to the destination space
        else:
            should_redraw, last_pipe_space =\
                self.board.autocomplete_pipe(src_pipe_space, dst_space)
            self.curr_pipe_space = last_pipe_space
            self.curr_selected_space = dst_space
            pipe_modified = True

        return pipe_modified

    def check_level_complete(self):
        for row in self.board.spaces:
            for space in row:
                if not space.has_pipe():
                    return False
        self.level_complete = True
        return True


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
