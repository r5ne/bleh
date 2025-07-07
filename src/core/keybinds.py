import warnings
from collections import defaultdict
from typing import Callable, Any

from src.core.types import EventTypes
from src.core import events
from src.data.globals import rom_data


observers = defaultdict(list)
input_checks = {
    "keydown": events.is_key_down,
    "keyup": events.is_key_up,
    "key": events.is_key_held,
    "mousebuttondown": events.is_mouse_down,
    "mousebuttonup": events.is_mouse_up,
    "mouse": events.is_mouse_held,
    "quit": lambda: rom_data.running,
}
sorted_bindings_cache = []


def register(*inputs: tuple[EventTypes, int], action: Callable[[], Any]) -> None:
    observers[inputs].append(action)
    sorted_bindings_cache.clear()


def deregister(*inputs: tuple[EventTypes, int], action: Callable[[], Any]) -> None:
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


def notify() -> None:
    global sorted_bindings_cache
    if not sorted_bindings_cache:
        sorted_bindings_cache = sorted(
            observers.items(), key=lambda binding: len(binding[0]), reverse=True
        )
    used_inputs = set()
    for inputs, actions in sorted_bindings_cache:
        for input_type, value in inputs:
            check_func = input_checks.get(input_type)
            if (
                (input_type, value) not in used_inputs
                and check_func is not None
                and check_func(value)
            ):
                for action in actions:
                    action()
                used_inputs.update(inputs)


def is_registered(*inputs: int, handler: Callable[[], Any]) -> bool:
    return inputs in observers and handler in observers[events]
