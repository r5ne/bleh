from typing import override

import pygame

from src.data import rom_data


class Entity(pygame.sprite.Sprite):
    def __init__(self, image, hitbox=None, spawnpoint=None, image_alignment="center"):
        super().__init__()
        self.image = image
        self.image_rect = self.image.get_rect()
        if hitbox is not None:
            self.hitbox = hitbox
        else:
            self.hitbox = self.image.get_rect()
        if spawnpoint:
            self.spawnpoint = [0, 0]
        else:
            self.spawnpoint = spawnpoint
        self.image_alignment = image_alignment
        self.move_to_spawn()

    @override
    def update(self): ...

    def blit(self):
        setattr(
            self.image_rect,
            self.image_alignment,
            getattr(self.hitbox, self.image_alignment),
        )
        rom_data.abs_window.blit(self.image, self.image_rect)

    def move_to_spawn(self):
        setattr(self.hitbox, "topleft", self.spawnpoint)


class EntityGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def blit(self):
        super().draw(rom_data.abs_window)
