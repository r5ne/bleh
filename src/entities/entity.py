from typing import override, final

import pygame

from src.data import rom_data


class Entity(pygame.sprite.Sprite):
    def __init__(self, sprite, hitbox=None, spawnpoint=None, sprite_hitbox_alignment="center"):
        super().__init__()
        self.sprite = sprite
        self.sprite_rect = self.sprite.get_rect()
        if hitbox is not None:
            self.hitbox = hitbox
        else:
            self.hitbox = self.sprite.get_rect()
        self.sprite_hitbox_alignment = sprite_hitbox_alignment
        if spawnpoint is not None:
            self.hitbox.topleft = spawnpoint

        self.image = self.sprite
        self.rect = self.hitbox

    @override
    def update(self): ...

    def blit(self):
        setattr(
            self.sprite_rect,
            self.sprite_hitbox_alignment,
            getattr(self.hitbox, self.sprite_hitbox_alignment),
        )
        rom_data.abs_window.blit(self.sprite, self.sprite_rect)


class RespawnableEntity(Entity):
    def __init__(self, sprite, hitbox=None, spawnpoint=None, sprite_hitbox_alignment="center"):
        self.spawnpoint = spawnpoint if spawnpoint is not None else [0, 0]
        super().__init__(sprite, hitbox, self.spawnpoint, sprite_hitbox_alignment)

    def respawn(self):
        self.hitbox.topleft = self.spawnpoint


class PoolableEntity(Entity):
    def __init__(self, sprite, hitbox=None, sprite_hitbox_alignment="center"):
        super().__init__(sprite, hitbox, sprite_hitbox_alignment=sprite_hitbox_alignment)
        self.spawnpoint = None
        self.active = True

    @final
    def blit(self):
        if self.active:
            self._blit()

    @final
    def update(self):
        if self.active:
            self._update()

    def _blit(self):
        super().blit()

    def _update(self): ...

    def deactivate(self):
        self.active = False

    def activate(self, spawnpoint, *args, **kwargs):
        self.hitbox.topleft = spawnpoint
        self.active = True


class EntityGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def blit(self):
        super().draw(rom_data.abs_window)
