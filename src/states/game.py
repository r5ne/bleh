import pygame

from src.data import rom_data
from src.states.state import State
from src.entities.players.player import Player


class Game(State):
    def __init__(self):
        super().__init__()
        self.background = pygame.Surface((1920, 1080))
        temp = pygame.Surface((10, 10))
        temp.fill(pygame.Color("white"))
        self.player = Player(
            self,
            temp,
            spawnpoint=[
                rom_data.abs_window_rect.centerx - 5,
                rom_data.abs_window_rect.centery + 5,
            ],
        )

    def update(self):
        self.player.update()

    def render(self):
        super().render()
        self.player.blit()
