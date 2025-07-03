from abc import ABC, abstractmethod

import pygame.time


class BulletPattern(ABC):
    def __init__(self, pool, group):
        self.pool = pool
        self.group = group

    @abstractmethod
    def update(self): ...

    @abstractmethod
    def start(self, *args, **kwargs): ...


class SingleBulletPattern(BulletPattern):
    def __init__(self, pool, group, repeat_cooldown):
        super().__init__(pool, group)
        self.cooldown = repeat_cooldown
        self._current_time = 0
        self._previous_start_time = 0

    def update(self):
        self._current_time = pygame.time.get_ticks()

    def start(self, origin):
        if self._current_time - self._previous_start_time >= self.cooldown:
            bullet = self.pool.aquire(origin, 150)
            self.group.add(bullet)
            self._current_time = self._previous_start_time
