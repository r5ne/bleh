from __future__ import annotations
from abc import ABC, abstractmethod
from typing import override, TYPE_CHECKING

import pygame.time

if TYPE_CHECKING:
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
    def start(self, *args, **kwargs) -> None:
        if self._current_time - self._previous_start_time >= self.cooldown:
            bullet = self.pool.aquire(*args, **kwargs)
            self.group.add(bullet)
            self._previous_start_time = self._current_time
