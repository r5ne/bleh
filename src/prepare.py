import warnings

import pygame

from src.data.globals import rom_data, rw_data
from src.core.constants import DISPLAY_FLAG_NAMES_MAP
from src.core import keybinds
from src.states import title, game
from src.states import manager

pygame.init()
pygame.display.set_caption(f"bleh v{rom_data.version}")

# window config

for flag_name, enabled in rw_data.flags.items():
    if enabled:
        rom_data.flags |= DISPLAY_FLAG_NAMES_MAP.inverse[flag_name][0]

rom_data.screen_rect = pygame.Rect(
    0, 0, pygame.display.Info().current_w, pygame.display.Info().current_h
)
if rom_data.default_config or not rw_data.resolution:
    rw_data.resolution = rom_data.screen_rect.size

rom_data.window = pygame.display.set_mode(rw_data.resolution, rom_data.flags)
rom_data.window_rect = rom_data.window.get_rect()
rom_data.abs_window = pygame.Surface((1920, 1080))
rom_data.abs_window_rect = rom_data.abs_window.get_rect()


while rom_data.scale_factor is None or not all(rom_data.scale_factor):
    if rw_data.non_int_scaling:
        scalex = round(rom_data.window_rect.width / rom_data.abs_window_rect.width, 4)
        scaley = round(rom_data.window_rect.height / rom_data.abs_window_rect.height, 4)
        if rw_data.non_native_ratio:
            rom_data.scale_factor = (scalex, scaley)
        else:
            min_ratio = min(scalex, scaley)
            rom_data.scale_factor = (min_ratio, min_ratio)
    else:
        int_scalex = rom_data.window_rect.width // rom_data.abs_window_rect.width
        int_scaley = rom_data.window_rect.height // rom_data.abs_window_rect.height
        if rw_data.non_native_ratio:
            rom_data.scale_factor = (int_scalex, int_scaley)
        else:
            minimum_int_ratio = min(int_scalex, int_scaley)
            if minimum_int_ratio == 0:
                warnings.warn(
                    "Attempted to use only integer scaling and a native "
                    "ratio, but screen size is smaller than native ratio. "
                    "Forcing non integer scaling to be allowed, and "
                    "recalculating scale factor.",
                    stacklevel=2,
                )
                rw_data.non_int_scaling = True
            rom_data.scale_factor = (minimum_int_ratio, minimum_int_ratio)

# global keybindings

keybinds.register(
    ("keydown", pygame.K_END),
    action=lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)),
)
keybinds.register(("keydown", pygame.K_ESCAPE), action=manager.back)

manager.state_dict = {"title": title.Title, "game": game.Game}
manager.append_state("title", initial_state=True)

rom_data.running = True
