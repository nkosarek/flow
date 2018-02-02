from config import NUM_LEVELS


################
# Mouse Events #
################

def mouse_click(event, view, state):
    if not state.in_game:
        return

    space = view.level.selected_space(event, state.board)

    state.new_selected_space(space)


def mouse_drag(event, view, state):
    if not state.in_game:
        return

    dst_space = view.level.selected_space(event, state.board)

    state.attempt_pipe_advance(dst_space)


def mouse_release(event, view, state):
    if not state.in_game:
        return

    release_space = view.level.selected_space(event, state.board)

    state.unselect_space(release_space)


#################
# Button Events #
#################

def menu_play_button(state):
    state.go_to_level_select()


def level_select_level(state, level):
    state.start_level(level)


def level_back_to_level_select(state):
    state.go_to_level_select()


def last_level(state):
    level = state.level
    if level > 0:
        state.start_level(level-1)


def reset_level(state):
    state.restart_level()


def next_level(state):
    level = state.level
    if level < NUM_LEVELS-1:
        state.start_level(level+1)
