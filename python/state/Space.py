from Dot import Dot
from Pipe import Pipe


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
