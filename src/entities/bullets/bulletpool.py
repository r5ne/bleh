class BulletPool:
    def __init__(self, bullet_class, max_size, *init_args, **init_kwargs):
        self.bullet_class = bullet_class
        self.pool = []
        self.max_size = max_size
        self.init_args = init_args
        self.init_kwargs = init_kwargs

    def aquire(self, *args, **kwargs):
        if self.pool:
            bullet = self.pool.pop()
        else:
            bullet = self.bullet_class(*self.init_args, **self.init_kwargs)
        bullet.activate(*args, **kwargs)
        return bullet

    def release(self, bullet):
        if len(self.pool) < self.max_size:
            bullet.deactivate()
            self.pool.append(bullet)
