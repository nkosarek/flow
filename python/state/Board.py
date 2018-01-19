from Space import Space


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
