from typing import override

import pygame

from src.data.globals import rom_data
from src.states.state import State
from src.entities.players import player
from src.entities import entity
from src.entities.bullets import bullet
from src.entities.bullets import bulletpool
from src.entities.bullets.patterns import bulletpattern


class Game(State):
    def __init__(self):
        super().__init__()
        temp = pygame.Surface((10, 10))
        temp.fill(pygame.Color("white"))
        self.player_bullets = entity.EntityGroup()
        sprite = pygame.Surface((2, 2))
        sprite.fill(pygame.Color("white"))
        self.player_bullet_pool = bulletpool.BulletPool(
            bullet.LinearBullet, 200, sprite
        )
        self.player = player.Player(
            self.player_bullets,
            self.player_bullet_pool,
            bulletpattern.LineBulletPattern,
            temp,
            spawnpoint=(
                rom_data.abs_window_rect.centerx - 5,
                rom_data.abs_window_rect.centery + 5,
            ),
        )

    @override
    def update(self) -> None:
        self.player.update()
        self.player_bullets.update()
        for bullet in list(self.player_bullets):
            if not bullet.active:
                self.player_bullets.remove(bullet)
                self.player_bullet_pool.release(bullet)

    @override
    def render(self) -> None:
        self.draw_background()
        self.player.draw()
        self.player_bullets.draw_sprites()
