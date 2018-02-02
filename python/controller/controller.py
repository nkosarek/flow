from config import NUM_LEVELS, MENU, LEVEL_SELECT, LEVEL


################
# Mouse Events #
################

def mouse_click(event, view, state):
    if not state.in_game:
        return

    space = view.level.selected_space(event, state.board)

    if state.new_selected_space(space):
        state.modified = True
        #view.redraw_level(state)


def mouse_drag(event, view, state):
    if not state.in_game:
        return

    dst_space = view.level.selected_space(event, state.board)

    if state.attempt_pipe_advance(dst_space):
        state.modified = True
        #view.redraw_level(state)


def mouse_release(event, view, state):
    if not state.in_game:
        return

    if view.changing_window:
        view.changing_window = False
        state.modified = True
        #view.redraw_level(state)
        return

    release_space = view.level.selected_space(event, state.board)

    if state.unselect_space(release_space):
        state.modified = True
        #view.redraw_level(state)


#################
# Button Events #
#################

def menu_play_button(state):
    state.page = LEVEL_SELECT
    state.modified = True
    #view.show_level_select()


#def level_select_back_to_menu(state, view):
#    state.page = MENU
#    state.modified = True
    #view.show_menu()


def level_select_level(state, level):
    state.start_level(level)
    state.modified = True
    #view.redraw_level(state)


def level_back_to_level_select(state):
    state.in_game = False
    state.page = LEVEL_SELECT
    state.modified = True
    #view.show_level_select()


def last_level(state):
    level = state.level
    if level > 0:
        state.start_level(level-1)
        state.modified = True
        #view.redraw_level(state)


def reset_level(state):
    state.restart_level()
    state.modified = True
    #view.redraw_level(state)


def next_level(state):
    level = state.level
    if level < NUM_LEVELS-1:
        state.start_level(level+1)
        state.modified = True
        #view.redraw_level(state)


#################
# Window Events #
#################

def window_change(view, state):
    if state.in_game:
        view.changing_window = True
