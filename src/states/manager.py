state_dict = {}
state_stack = []

def current_state():
    if state_stack:
        return state_stack[-1]
    msg = (
        f"Attempted to access current state in empty state stack "
        f"{state_stack}."
    )
    raise IndexError(msg)

def state_exists(state_name):
    return state_name in state_dict

def initialise_state(state_name):
    if state_exists(state_name):
        state_class = state_dict[state_name]
        return state_class()
    msg = (
        f"Initializing state {state_name!r} failed. State does not exist in"
        f" state dictionary {state_dict!r}."
    )
    raise KeyError(msg)

def append(state_name, *, initial_state):
    if not initial_state:
        current_state().cleanup()
    state_stack.append(initialise_state(state_name))
    current_state().startup()

def pop():
    current_state().cleanup()
    state_stack.pop()
    current_state().startup()

def switch(state_name):
    current_state().cleanup()
    state_stack.pop()
    state_stack.append(initialise_state(state_name))
    current_state().startup()

def back_to(state_name):
    if not state_exists(state_name):
        msg = (
            f"Cannot go back to state {state_name!r}. State does not exist in"
            f" state dictionary {state_dict!r}."
        )
        raise KeyError(msg)
    current_state().cleanup()
    while current_state() != state_dict[state_name]:
        state_stack.pop()
    current_state().startup()

def back():
    if current_state():
        current_state().back()
