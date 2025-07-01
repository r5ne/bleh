import pygame

from src.states.state import State
from src.states.manager import append_state


class Title(State):
    def __init__(self):
        super().__init__()
        background = pygame.Surface((1920, 1080))
        background.fill((255, 100, 100))
        self.background = background

    def back(self):
        append_state("game")
