###############################################################################
#
# Flow - Web game based on smart phone app "Flow Free"
#
# Author: Nicholas Kosarek
# Python Version 2.7
#
###############################################################################

# TODO: [BUGS]
# TODO: Doesn't check game completion if mouse dragged past last dot

# TODO: [REFACTOR]
# TODO: move all 'can advance' logic into spaces for attempt_pipe_advance
# TODO: update display on timer instead of in event handlers
# TODO: Space interface (dot space, bridge space, etc)

# TODO: [FEATURES]
# TODO: Game completion; perfect game
# TODO: pipe autocomplete
# TODO: stats page
# TODO: Do not clear crossed pipe until mouse release

# TODO: [STRETCH]
# TODO: custom boards
# TODO: bridges
# TODO: walls
# TODO: multiplayer (race?)
# TODO?: board solver
# TODO?: custom board validation

import Tkinter as Tk

from config import *
from controller.controller import *
from state.GameState import GameState
from view.GameView import GameView


def main():

    root = Tk.Tk()

    state = GameState()

    view = GameView(root, state, WINDOW_WIDTH, WINDOW_HEIGHT)

    root.bind("<Button-1>", lambda event: mouse_click(event, view, state))
    root.bind("<B1-Motion>", lambda event: mouse_drag(event, view, state))
    root.bind("<ButtonRelease-1>", lambda event: mouse_release(event, view, state))
    root.bind("<Configure>", lambda event: window_change(view, state))

    root.wm_geometry("%sx%s" % (WINDOW_WIDTH, WINDOW_HEIGHT))
    root.mainloop()

main()
