from __future__ import annotations
import math
from abc import ABC
from typing import override, Literal, TYPE_CHECKING


from src.data import rom_data
from src.entities.entity import PoolableEntity

if TYPE_CHECKING:
    from src.core.types import RectAlignments
    import pygame


class Bullet(PoolableEntity, ABC):
    def __init__(
        self,
        sprite: pygame.Surface,
        hitbox: pygame.Rect | None = None,
        sprite_hitbox_alignment: RectAlignments | str = "center",
    ):
        super().__init__(sprite, hitbox, sprite_hitbox_alignment)

    @override
    def _draw(self) -> None:
        self.draw_sprite()

    @override
    def _update(self) -> None:
        self.update_sprite_rect()

    @override
    def activate(self, *args, **kwargs) -> None:
        super().activate(args[0])


class StraightBullet(Bullet):
    def __init__(
        self,
        sprite: pygame.Surface,
        hitbox: pygame.Rect | None = None,
        sprite_hitbox_alignment: RectAlignments | str = "center",
    ):
        super().__init__(sprite, hitbox, sprite_hitbox_alignment)
        self.dx = 0
        self.dy = 0

    @override
    def _update(self) -> None:
        self.hitbox.move_ip(round(self.dx * rom_data.dt), round(self.dy * rom_data.dt))
        self.update_sprite_rect()
        if not rom_data.abs_window_rect.contains(self.sprite_rect):
            self.deactivate()

    @override
    def activate(
        self,
        spawnpoint: tuple[int, int],
        speed: int,
        direction: Literal[1, 2, 3, 4] = 1,
    ) -> None:
        super().activate(spawnpoint)
        match direction:
            case 1:
                self.dy = -speed
            case 2:
                self.dx = speed
            case 3:
                self.dy = speed
            case 4:
                self.dx = -speed


class LinearBullet(Bullet):
    def __init__(
        self,
        sprite: pygame.Surface,
        hitbox: pygame.Rect | None = None,
        sprite_hitbox_alignment: RectAlignments | str = "center",
        direction: float = 0,
    ):
        super().__init__(sprite, hitbox, sprite_hitbox_alignment)
        self.angle = math.radians(direction)
        self.dx = 0
        self.dy = 0

    @override
    def _update(self) -> None:
        self.hitbox.move_ip(round(self.dx * rom_data.dt), round(self.dy * rom_data.dt))
        self.update_sprite_rect()
        if not rom_data.abs_window_rect.contains(self.sprite_rect):
            self.deactivate()

    @override
    def activate(
        self, spawnpoint: tuple[int, int], speed: int, angle: float = 0
    ) -> None:
        super().activate(spawnpoint)
        self.dx = round(speed * math.sin(self.angle), 4)
        self.dy = round(-speed * math.cos(self.angle), 4)
