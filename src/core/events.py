from src import data

import pygame

_keydown_keys = {}
_keyup_keys = {}
_held_keys = {}
_mousedown_buttons = {}
_mouseup_buttons = {}
_held_buttons = {}
mouse_pos = (0, 0)


def is_key_down(key: int) -> bool:
    return key in _keydown_keys


def is_key_up(key: int) -> bool:
    return key in _keyup_keys


def is_key_held(key: int) -> bool:
    return key in _held_keys


def is_mouse_down(button: int) -> bool:
    return button in _mousedown_buttons


def is_mouse_up(button: int) -> bool:
    return button in _mouseup_buttons


def is_mouse_held(button: int) -> bool:
    return button in _held_buttons


def process_events(events: list[pygame.event.Event]) -> None:
    global mouse_pos

    _keydown_keys.clear()
    _keyup_keys.clear()
    _mousedown_buttons.clear()
    _mouseup_buttons.clear()

    for event in events:
        match event.type:
            case pygame.KEYDOWN:
                _keydown_keys[event.key] = True
                _held_keys[event.key] = True
            case pygame.KEYUP:
                _keyup_keys[event.key] = True
                del _held_keys[event.key]
            case pygame.MOUSEBUTTONDOWN:
                _mousedown_buttons[event.button] = True
                _held_buttons[event.button] = True
            case pygame.MOUSEBUTTONUP:
                _mouseup_buttons[event.button] = True
                del _held_buttons[event.button]
            case pygame.QUIT:
                data.rom_data.running = False

    mouse_pos = tuple(
        coord / data.rom_data.scale_factor[i]
        for i, coord in enumerate(pygame.mouse.get_pos())
    )
