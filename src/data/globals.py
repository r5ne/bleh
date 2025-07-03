from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass
import json

import pygame
from pydantic import BaseModel, ValidationError, ConfigDict


class RWData(BaseModel):
    model_config = ConfigDict(extra="ignore")

    flags: dict[str, bool] = {"fullscreen": True, "noframe": True}
    resolution: tuple[int, int] = None  # will be defined after prepare.py is ran
    non_int_scaling: bool = True
    non_native_ratio: bool = False

    def save(self, directory):
        directory.touch()
        with directory.open("w") as file:
            file.write(self.model_dump_json())

    @classmethod
    def load(cls, directory) -> tuple[RWData, bool]:
        """The returned boolean indicates if the returned config is default or not."""
        directory.touch()
        with directory.open() as file:
            try:
                file_data = json.load(file)
                return cls.model_validate(file_data), False
            except (json.decoder.JSONDecodeError, ValidationError) as e:
                default_settings = cls()
                if e == ValidationError:
                    backup_path = directory.with_suffix(".backup.json")
                    directory.rename(backup_path)
                default_settings.save(directory)
                return default_settings, True


@dataclass(kw_only=True)
class ROMData:
    running: bool = False  # will be set to true when prepare.py called
    version: int = 0.1
    fps: int = 165
    dt: float = 1.0
    flags: int = pygame.SCALED
    # defined in after prepare.py is called
    abs_window: pygame.Surface = None
    abs_window_rect: pygame.Rect = None
    window: pygame.Surface = None
    window_rect: pygame.Rect = None
    screen_rect: pygame.Rect = None
    scale_factor: tuple[float, float] = None
    config_dir = Path("config.json")
    default_config: bool = None


rom_data = ROMData()
rw_data, rom_data.default_config = RWData.load(rom_data.config_dir)
