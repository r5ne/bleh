from __future__ import annotations
from collections import deque

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.entities.bullets.bullet import Bullet


class BulletPool:
    def __init__(
        self, bullet_class: type[Bullet], max_size: int, *init_args, **init_kwargs
    ):
        self.bullet_class = bullet_class
        self.max_size = max_size
        self.init_args = init_args
        self.init_kwargs = init_kwargs
        self.pool = [
            self.bullet_class(*self.init_args, **self.init_kwargs)
            for _ in range(max_size)
        ]
        self.free = deque(self.pool)
        self.in_use = deque()

    def aquire(self, *args, **kwargs) -> Bullet:
        if not self.free:
            oldest_bullet = self.in_use.popleft()
            oldest_bullet.pool_despawn()
            self.free.append(oldest_bullet)
        bullet = self.free.pop()
        bullet.pool_respawn(*args, **kwargs)
        self.in_use.append(bullet)
        return bullet

    def release(self, bullet: Bullet) -> None:
        bullet.pool_despawn()
        self.in_use.remove(bullet)
        self.free.append(bullet)
