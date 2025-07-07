from __future__ import annotations

import pygame

from src.data.globals import rom_data
from src.states import manager


class State:
    def __init__(self):
        self.background = pygame.Surface((1920, 1080))

    def startup(self) -> None: ...

    def cleanup(self) -> None: ...

    def render(self) -> None: ...

    def update(self) -> None:
        self.draw_background()

    def draw_background(self) -> None:
        rom_data.abs_window.blit(self.background, (0, 0))

    def back(self) -> State:
        return manager.pop_state()
