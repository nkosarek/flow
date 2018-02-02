from Board import Board
from config import BOARD_SETUP, LEVEL_INCOMPLETE, LEVEL_COMPLETE, LEVEL_PERFECT


class GameState:
    def __init__(self):
        self.in_game = False
        self.board = None
        self.level = None
        self.curr_selected_space = None
        self.curr_pipe_space = None
        self.building_pipe = False
        self.last_pipe_advanced = None
        self.move_count = 0
        self.level_complete = LEVEL_INCOMPLETE

    def start_level(self, level):
        self._clear_in_level_fields()
        self.level = level
        (rows, cols, dots) = BOARD_SETUP[level]
        self.board = Board(rows, cols, dots)
        self.in_game = True

    def restart_level(self):
        self._clear_in_level_fields()
        self.board.reset_board()
        self.in_game = True

    def _clear_in_level_fields(self):
        self.in_game = False
        self.curr_selected_space = None
        self.curr_pipe_space = None
        self.building_pipe = False
        self.last_pipe_advanced = None
        self.move_count = 0
        self.level_complete = LEVEL_INCOMPLETE

    def new_selected_space(self, space):
        # No space selected, or has no pipe to advance/create
        if space is None or (not space.has_dot() and not space.has_pipe()):
            self.curr_selected_space = None
            self.curr_pipe_space = None
            self.building_pipe = False
            # Board not updated
            return False

        self.curr_pipe_space = space
        self.curr_selected_space = space
        self.building_pipe = True
        self.level_complete = LEVEL_INCOMPLETE
        # Is dot space
        if space.has_dot():
            # Is the dot space opposite the pipe start dot space
            if not space.has_pipe() or space.is_pipe_end():
                Board.clear_pipe(space.get_other_dot_space())
            # Is the dot space with the pipe start
            else:
                Board.clear_pipe(space.get_next_pipe_space())

            # Start the pipe from the current dot space
            space.set_pipe(space.get_dot_color(), None)

            self._check_new_move(space)

        # Is non-dot space but has pipe
        elif space.has_pipe():
            Board.clear_pipe(space.get_next_pipe_space())

            self._check_new_move(space)

        # Board updated
        return True

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
            should_redraw, last_pipe_space = \
                self.board.autocomplete_pipe(src_pipe_space, dst_space)
            self.curr_pipe_space = last_pipe_space
            self.curr_selected_space = dst_space
            pipe_modified = True

        return pipe_modified

    def unselect_space(self, release_space):
        board_modified = False

        # Pipe was being built during this mouse select sequence
        if self.building_pipe:
            # Mouse released on dot at beginning of current pipe
            if release_space is not None and \
                    release_space == self.curr_pipe_space and \
                    release_space.is_pipe_start():
                Board.clear_pipe(release_space)
                self.curr_selected_space = None
                self.curr_pipe_space = None
                board_modified = True

            elif self._check_level_complete():
                board_modified = True

            self.building_pipe = False

        return board_modified

    def _check_new_move(self, space):
        color = space.get_pipe_color()
        if color != self.last_pipe_advanced:
            self.move_count += 1
            self.last_pipe_advanced = color

    def _check_level_complete(self):
        for row in self.board.spaces:
            for space in row:
                if not space.has_pipe():
                    return False

        if self.move_count == self.board.num_dots:
            self.level_complete = LEVEL_PERFECT
        else:
            self.level_complete = LEVEL_COMPLETE

        return True
