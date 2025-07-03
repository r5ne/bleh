from src.data import rom_data
from src.entities.entity import PoolableEntity

class Bullet(PoolableEntity):
    def __init__(self, sprite, hitbox=None, sprite_hitbox_alignment="center"):
        super().__init__(sprite, hitbox, sprite_hitbox_alignment)
        self.speed = None

    def _update(self):
        self.hitbox.move_ip(0, round(-self.speed * rom_data.dt))
        if not rom_data.abs_window_rect.contains(self.hitbox):
            self.deactivate()

    def activate(self, spawnpoint, speed):
        super().activate(spawnpoint)
        self.speed = speed
