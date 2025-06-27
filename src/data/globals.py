from dataclasses import dataclass
import pygame


@dataclass(kw_only=True)
class ROMData:
    running: bool = False  # will be set to true when prepare.py called
    version: int = 0.1
    # defined in after prepare.py is called
    screen: pygame.Surface = ...
    screen_rect: pygame.Rect = ...


rom_data = ROMData()
