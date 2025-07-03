from collections import deque

class BulletPool:
    def __init__(self, bullet_class, max_size, *init_args, **init_kwargs):
        self.bullet_class = bullet_class
        self.max_size = max_size
        self.init_args = init_args
        self.init_kwargs = init_kwargs
        self.pool = [self.bullet_class(*self.init_args, **self.init_kwargs) for _ in range(max_size)]
        self.free = deque(self.pool)
        self.in_use = deque()

    def aquire(self, *args, **kwargs):
        if not self.free:
            oldest_bullet = self.in_use.popleft()
            oldest_bullet.active = False
            self.free.append(oldest_bullet)
        bullet = self.free.pop()
        bullet.activate(*args, **kwargs)
        self.in_use.append(bullet)
        return bullet

    def release(self, bullet):
        bullet.active = False
        self.in_use.remove(bullet)
        self.free.append(bullet)
