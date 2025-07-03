from dataclasses import dataclass

import pygame

from src.core import events
from src.data import rom_data
from src.entities.entity import RespawnableEntity


@dataclass
class PlayerStats:
    health: int = 1
    speed: int = 30
    shoot_cooldown: int = 100


class Player(RespawnableEntity):
    def __init__(
        self,
        bullet_group,
        bullet_pool,
        bullet_pattern,
        surface,
        hitbox=None,
        spawnpoint=None,
        sprite_alignment="center",
        stats=None,
    ):
        super().__init__(surface, hitbox, spawnpoint, sprite_alignment)
        self.bullet_group = bullet_group
        self.bullet_pool = bullet_pool
        if stats is None:
            stats = PlayerStats()
        self.health = stats.health
        self.speed = stats.speed
        self.bullet_pattern = bullet_pattern(self.bullet_pool, self.bullet_group, stats.shoot_cooldown)
        self._press_counter = 0
        self._key_priority = {
            pygame.K_UP: 0,
            pygame.K_DOWN: 0,
            pygame.K_LEFT: 0,
            pygame.K_RIGHT: 0,
        }

    def update(self):
        for key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
            if events.is_key_down(key):
                self._press_counter += 1
                self._key_priority[key] = self._press_counter
            elif events.is_key_up(key):
                self._key_priority[key] = 0

        left = self._key_priority[pygame.K_LEFT]
        right = self._key_priority[pygame.K_RIGHT]
        if left == right == 0:
            dx = 0.0
        elif left > right:
            dx = -self.speed
        else:
            dx = self.speed

        up = self._key_priority[pygame.K_UP]
        down = self._key_priority[pygame.K_DOWN]
        if up == down == 0:
            dy = 0.0
        elif up > down:
            dy = -self.speed
        else:
            dy = self.speed

        self.hitbox.x += round(dx * rom_data.dt)
        self.hitbox.y += round(dy * rom_data.dt)
        self.hitbox.clamp_ip(rom_data.abs_window_rect)
        if events.is_key_held(pygame.K_z):
            self.bullet_pattern.start(self.sprite_rect.midtop)
        self.bullet_pattern.update()
