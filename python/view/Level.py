from Page import *
from config import PIPE_COLORS, OVERWRITE_PIPE_COLORS, DOT_COLORS
from controller.controller import level_back_to_level_select, last_level, reset_level, next_level


class Level(Page):
    def __init__(self, view, state, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.label = Tk.Label(self)
        self.label.pack()

        self.back = Tk.Button(self, text="<- Back",
                              command=lambda: level_back_to_level_select(view, state))
        self.back.pack()

        self.canvas = Tk.Canvas(self, bg="#888")
        self.canvas.pack(fill="both", expand=True)

        self.last_level = Tk.Button(self, text="<",
                                    command=lambda: last_level(view, state))
        self.reset = Tk.Button(self, text="RESET",
                               command=lambda: reset_level(view, state))
        self.next_level = Tk.Button(self, text=">",
                                    command=lambda: next_level(view, state))
        self.last_level.pack(side="left")
        self.next_level.pack(side="right")
        self.reset.pack()

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
        self.label.config(text="Level %d" % (state.level+1))
        self.canvas.delete(Tk.ALL)

        self._draw_board(self.canvas, state)
        if state.level_complete:
            Level._draw_level_complete(self.canvas, state)

        self.canvas.update()
        if not self.visible:
            self.show()
            self.visible = True

    def _draw_board(self, canvas, state):
        rows, cols = state.board.rows, state.board.cols
        board_dimen = Level._get_board_dimensions(canvas.winfo_width(),
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
                Level._draw_space(canvas, space, x0, y0, x1, y1)

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
                           anchor=Tk.CENTER)
