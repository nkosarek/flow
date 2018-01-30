from state.Board import Board
from config import NUM_LEVELS


################
# Mouse Events #
################

def mouse_click(event, view, state):
    if not state.in_game:
        return

    space = view.level.selected_space(event, state.board)

    if state.new_selected_space(space):
        view.redraw_level(state)


def mouse_drag(event, view, state):
    if not state.in_game:
        return

    dst_space = view.level.selected_space(event, state.board)

    if state.attempt_pipe_advance(dst_space):
        view.redraw_level(state)


def mouse_release(event, view, state):
    if state.in_game:
        if view.changing_window:
            view.changing_window = False
            view.redraw_level(state)
            return

        curr_pipe_space = state.curr_pipe_space
        release_space = view.level.selected_space(event, state.board)
        if curr_pipe_space is not None and\
                release_space == curr_pipe_space and release_space.has_dot():
            other = release_space.get_other_dot_space()
            if not other.has_pipe():
                Board.clear_pipe(release_space)
                state.curr_selected_space = None
                state.curr_pipe_space = None
                view.redraw_level(state)
            elif state.check_level_complete():
                view.redraw_level(state)


#################
# Button Events #
#################

def menu_play_button(view):
    view.show_level_select()


def level_select_back_to_menu(view):
    view.show_menu()


def level_select_level(view, state, level):
    state.start_level(level)
    view.redraw_level(state)


def level_back_to_level_select(view, state):
    state.in_game = False
    view.show_level_select()


def last_level(view, state):
    level = state.level
    if level > 0:
        state.start_level(level-1)
        view.redraw_level(state)


def reset_level(view, state):
    state.start_level(state.level)
    view.redraw_level(state)


def next_level(view, state):
    level = state.level
    if level < NUM_LEVELS-1:
        state.start_level(level+1)
        view.redraw_level(state)


#################
# Window Events #
#################

def window_change(view, state):
    if state.in_game:
        view.changing_window = True
