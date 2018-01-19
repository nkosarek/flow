from state.Board import Board


################
# Mouse Events #
################

def mouse_click(event, view, state):
    if not state.in_game:
        return

    space = view.level.selected_space(event, state.board)
    if space is None or (not space.has_dot() and not space.has_pipe()):
        state.curr_selected_space = None
        state.curr_pipe_space = None
        return

    state.curr_pipe_space = space
    state.curr_selected_space = space
    if space.has_dot():
        if not space.has_pipe() or space.is_pipe_end():
            Board.clear_pipe(space.get_other_dot_space())
        else:
            Board.clear_pipe(space.get_next_pipe_space())

        space.set_pipe(space.get_dot_color(), None)

    elif space.has_pipe():
        Board.clear_pipe(space.get_next_pipe_space())

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


#################
# Window Events #
#################

def window_change(view, state):
    if state.in_game:
        view.changing_window = True
