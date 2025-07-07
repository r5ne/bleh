from __future__ import annotations
from typing import override, final, TYPE_CHECKING
from abc import ABC, abstractmethod

import pygame

from src.data.globals import rom_data

if TYPE_CHECKING:
    from src.core.types import RectAlignments


class Entity(pygame.sprite.Sprite, ABC):
    def __init__(
        self,
        sprite: pygame.Surface,
        hitbox: pygame.Rect | None = None,
        spawnpoint: tuple[int, int] | None = None,
        spawnpoint_sprite_alignment: RectAlignments | str = "topleft",
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
            setattr(self.hitbox, spawnpoint_sprite_alignment, spawnpoint)

    @abstractmethod
    @override
    def update(self) -> None: ...

    @final
    def _update_sprite_rect(self) -> None:
        setattr(
            self.sprite_rect,
            self.sprite_hitbox_alignment,
            getattr(self.hitbox, self.sprite_hitbox_alignment),
        )

    @abstractmethod
    def draw(self) -> None: ...

    @final
    def _draw_sprite(self) -> None:
        rom_data.abs_window.blit(self.sprite, self.sprite_rect)


class RespawnableEntity(Entity, ABC):
    def __init__(
        self,
        sprite: pygame.Surface,
        hitbox: pygame.Rect | None = None,
        spawnpoint: tuple[int, int] | None = None,
        spawnpoint_sprite_alignment: RectAlignments | str = "topleft",
        sprite_hitbox_alignment: RectAlignments | str = "center",
    ) -> None:
        self.spawnpoint = spawnpoint if spawnpoint is not None else (0, 0)
        self.spawnpoint_sprite_alignment = spawnpoint_sprite_alignment
        super().__init__(
            sprite,
            hitbox,
            self.spawnpoint,
            self.spawnpoint_sprite_alignment,
            sprite_hitbox_alignment,
        )

    def respawn(self) -> None:
        setattr(self.hitbox, self.spawnpoint_sprite_alignment, self.spawnpoint)


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

    def pool_despawn(self) -> None:
        self.active = False

    @abstractmethod
    def pool_respawn(self, *args, **kwargs) -> None: ...

    @final
    def _reset_hitbox(
        self,
        spawnpoint: tuple[int, int],
        spawnpoint_sprite_alignment: RectAlignments | str = "topleft",
    ) -> None:
        setattr(self.hitbox, spawnpoint_sprite_alignment, spawnpoint)


class EntityGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def draw_sprites(self) -> None:
        for entity in self.sprites():
            entity.draw()
