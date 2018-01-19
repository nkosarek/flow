###############################################################################
#
# Flow - Web game based on smart phone app "Flow Free"
#
# Author: Nicholas Kosarek
# Python Version 2.7
#
###############################################################################

# TODO: [REFACTOR]
# TODO: move state logic out of controller functions
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

from config import *
from controller.controller import *
from state.GameState import GameState
from view.GameView import GameView


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
