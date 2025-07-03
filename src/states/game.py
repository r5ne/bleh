import pygame

from src.data import rom_data
from src.states.state import State
from src.entities import Player, EntityGroup, BulletPool, Bullet, SingleBulletPattern


class Game(State):
    def __init__(self):
        super().__init__()
        self.background = pygame.Surface(rom_data.abs_window_rect.size)
        temp = pygame.Surface((10, 10))
        temp.fill(pygame.Color("white"))
        self.player_bullets = EntityGroup()
        sprite = pygame.Surface((2, 2))
        sprite.fill(pygame.Color("white"))
        self.player_bullet_pool = BulletPool(Bullet, 200, sprite)
        self.player = Player(
            self.player_bullets, self.player_bullet_pool, SingleBulletPattern,
            temp,
            spawnpoint=[
                rom_data.abs_window_rect.centerx - 5,
                rom_data.abs_window_rect.centery + 5,
            ],
        )

    def update(self):
        self.player.update()
        self.player_bullets.update()
        
        for bullet in list(self.player_bullets):
            if not bullet.active:
                self.player_bullets.remove(bullet)
                self.player_bullet_pool.release(bullet)

    def render(self):
        super().render()
        self.player.blit()
        self.player_bullets.blit()
