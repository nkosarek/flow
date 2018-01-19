from Board import Board
from config import BOARD_SETUP


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
