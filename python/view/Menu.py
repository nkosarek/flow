from Page import *
from controller.controller import menu_play_button


class Menu(Page):
    def __init__(self, state, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        label = Tk.Label(self, text="Flow")
        label.pack()

        button = Tk.Button(self, text="Play",
                           command=lambda: menu_play_button(state))
        button.pack()
