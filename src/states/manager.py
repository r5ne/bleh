from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.states.state import State

state_dict: dict[str, State] = {}
state_stack: list[State] = []


def current_state() -> State:
    if state_stack:
        return state_stack[-1]
    msg = f"Attempted to access current state in empty state stack {state_stack}."
    raise IndexError(msg)


def state_exists(state_name: str) -> bool:
    return state_name in state_dict


def initialise_state(state_name: str) -> State:
    if state_exists(state_name):
        state_class = state_dict[state_name]
        return state_class()
    msg = (
        f"Initializing state {state_name!r} failed. State does not exist in"
        f" state dictionary {state_dict!r}."
    )
    raise KeyError(msg)


def append_state(state_name: str, *, initial_state: bool | None = None) -> None:
    if not initial_state:
        current_state().cleanup()
    state_stack.append(initialise_state(state_name))
    current_state().startup()


def pop_state() -> State:
    current_state().cleanup()
    popped_state = state_stack.pop()
    current_state().startup()
    return popped_state


def switch_state(state_name: str) -> State:
    current_state().cleanup()
    popped_state = state_stack.pop()
    state_stack.append(initialise_state(state_name))
    current_state().startup()
    return popped_state


def back_to_state(state_name: str) -> list[State]:
    if not state_exists(state_name):
        msg = (
            f"Cannot go back to state {state_name!r}. State does not exist in"
            f" state dictionary {state_dict!r}."
        )
        raise KeyError(msg)
    current_state().cleanup()
    popped_states = []
    while current_state() != state_dict[state_name]:
        popped_states.append(state_stack.pop())
    current_state().startup()
    return popped_states


def back() -> State | None:
    if current_state():
        return current_state().back()
    return None
