from abc import ABC, abstractmethod
from typing import override

import pygame.time

from src.entities.entity import EntityGroup
from src.entities.bullets.bulletpool import BulletPool


class BulletPattern(ABC):
    def __init__(self, pool: BulletPool, group: EntityGroup, *args, **kwargs):
        self.pool = pool
        self.group = group

    @abstractmethod
    def update(self) -> None: ...

    @abstractmethod
    def start(self, *args, **kwargs) -> None: ...


class LineBulletPattern(BulletPattern):
    def __init__(self, pool: BulletPool, group: EntityGroup, repeat_cooldown: int):
        super().__init__(pool, group)
        self.cooldown = repeat_cooldown
        self._current_time = 0
        self._previous_start_time = 0

    @override
    def update(self) -> None:
        self._current_time = pygame.time.get_ticks()

    @override
    def start(self, origin: tuple[int, int]) -> None:
        if self._current_time - self._previous_start_time >= self.cooldown:
            bullet = self.pool.aquire(origin, 150)
            self.group.add(bullet)
            self._previous_start_time = self._current_time
