from Page import *
from config import NUM_LEVELS
from controller.controller import level_select_level


class LevelSelect(Page):
    def __init__(self, view, state, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        label = tk.Label(self, text="Level Select")
        label.pack()

        for level in xrange(NUM_LEVELS):
            button = tk.Button(self, text="%s" % (level+1),
                               command=lambda lvl=level: level_select_level(view, state, lvl))
            button.pack()
