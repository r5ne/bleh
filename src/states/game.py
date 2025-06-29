import pygame

from src.states.state import State

class Game(State):
    def __init__(self):
        super().__init__()
        self.background = pygame.Surface((1920, 1080))
