import warnings
from collections import defaultdict

from src.core.events import (
    is_key_down,
    is_key_up,
    is_key_held,
    is_mouse_down,
    is_mouse_up,
    is_mouse_held,
)
from src.data import rom_data

observers = defaultdict(list)
input_checks = {
    "keydown": is_key_down,
    "keyup": is_key_up,
    "key": is_key_held,
    "mousebuttondown": is_mouse_down,
    "mousebuttonup": is_mouse_up,
    "mouse": is_mouse_held,
    "quit": lambda: rom_data.running,
}
sorted_bindings_cache = []


def register(*inputs, action):
    observers[inputs].append(action)
    sorted_bindings_cache.clear()


def deregister(*inputs, action):
    if action is not None and action in observers[inputs]:
        observers[inputs].remove(action)
        if not observers[inputs]:
            del observers[inputs]
    else:
        warnings.warn(
            f"Attempted to deregister inputs {inputs} that haven't"
            f"been registered to the observers dict {observers}",
            stacklevel=2,
        )
    sorted_bindings_cache.clear()


def notify():
    global sorted_bindings_cache
    if not sorted_bindings_cache:
        sorted_bindings_cache = sorted(
            observers.items(), key=lambda binding: len(binding[0]), reverse=True
        )
    used_inputs = set()
    for inputs, actions in sorted_bindings_cache:
        for input_type, value in inputs:
            check_func = input_checks.get(input_type)
            if (input_type, value) not in used_inputs and check_func(value):
                for action in actions:
                    action()
                used_inputs.update(inputs)


def is_registered(*events, handler):
    return events in observers and handler in observers[events]
