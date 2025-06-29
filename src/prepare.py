import pygame

from src.data import rom_data, rw_data
from src.core import DISPLAY_FLAG_NAMES_MAP
from src.core import keybinds
import src.states

pygame.init()
pygame.display.set_caption(f"bleh v{rom_data.version}")

# window config

for flag_name, enabled in rw_data.flags.items():
    if enabled:
        rom_data.flags |= DISPLAY_FLAG_NAMES_MAP.inverse[flag_name][0]

rom_data.window = pygame.display.set_mode(rw_data.resolution, rom_data.flags)
rom_data.window_rect = rom_data.window.get_rect()
rom_data.abs_window = pygame.Surface((1920, 1080))
rom_data.abs_window_rect = rom_data.abs_window.get_rect()
rom_data.screen_rect = pygame.Rect(
    0, 0, pygame.display.Info().current_w, pygame.display.Info().current_h
)

if rw_data.non_int_scaling:
    scalex = rom_data.window_rect.width / rom_data.abs_window_rect.width
    scaley = rom_data.window_rect.height / rom_data.abs_window_rect.height
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
        rom_data.scale_factor = minimum_int_ratio

# global keybindings

keybinds.register(("keydown", pygame.K_END), action=lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)))
keybinds.register(("keydown", pygame.K_ESCAPE), action=src.states.manager.back)

src.states.manager.state_dict = {"title": src.states.Title, "game": src.states.Game}
src.states.manager.append_state("title", initial_state=True)

rom_data.running = True
