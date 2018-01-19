from Page import *
from controller.controller import menu_play_button


class Menu(Page):
    def __init__(self, view, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        label = tk.Label(self, text="Flow")
        label.pack()

        button = tk.Button(self, text="Play",
                           command=lambda: menu_play_button(view))
        button.pack()
