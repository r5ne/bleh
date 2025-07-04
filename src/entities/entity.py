from __future__ import annotations
from typing import override, final, TYPE_CHECKING
from abc import ABC, abstractmethod

import pygame

from src.data import rom_data

if TYPE_CHECKING:
    from src.core import RectAlignments


class Entity(pygame.sprite.Sprite, ABC):
    def __init__(
        self,
        sprite: pygame.Surface,
        hitbox: pygame.Rect | None = None,
        spawnpoint: tuple[int, int] | None = None,
        sprite_hitbox_alignment: RectAlignments | str = "center",
    ):
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

    @abstractmethod
    @override
    def update(self) -> None: ...

    @final
    def update_sprite_rect(self) -> None:
        setattr(
            self.sprite_rect,
            self.sprite_hitbox_alignment,
            getattr(self.hitbox, self.sprite_hitbox_alignment),
        )

    @abstractmethod
    def draw(self) -> None: ...

    @final
    def draw_sprite(self) -> None:
        rom_data.abs_window.blit(self.sprite, self.sprite_rect)


class RespawnableEntity(Entity, ABC):
    def __init__(
        self,
        sprite: pygame.Surface,
        hitbox: pygame.Rect | None = None,
        spawnpoint: tuple[int, int] | None = None,
        sprite_hitbox_alignment: RectAlignments | str = "center",
    ) -> None:
        self.spawnpoint = spawnpoint if spawnpoint is not None else (0, 0)
        super().__init__(sprite, hitbox, self.spawnpoint, sprite_hitbox_alignment)

    def respawn(self) -> None:
        self.hitbox.topleft = self.spawnpoint


class PoolableEntity(Entity, ABC):
    def __init__(
        self,
        sprite: pygame.Surface,
        hitbox: pygame.Rect | None = None,
        sprite_hitbox_alignment: RectAlignments | str = "center",
    ):
        super().__init__(
            sprite, hitbox, sprite_hitbox_alignment=sprite_hitbox_alignment
        )
        self.spawnpoint: tuple[int, int] | None = None
        self.active = True

    @final
    @override
    def draw(self) -> None:
        if self.active:
            self._draw()

    @final
    @override
    def update(self) -> None:
        if self.active:
            self._update()

    @abstractmethod
    def _draw(self) -> None: ...

    @abstractmethod
    def _update(self) -> None: ...

    def deactivate(self) -> None:
        self.active = False

    def activate(self, spawnpoint: tuple[int, int], *args, **kwargs) -> None:
        self.hitbox.topleft = spawnpoint
        self.active = True


class EntityGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def draw_sprites(self) -> None:
        for entity in self.sprites():
            entity.draw()
