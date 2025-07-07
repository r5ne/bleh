import sys

import pygame

from src.core import events, keybinds
from src.data.globals import rom_data, rw_data
from src.states import manager
from src import prepare

def main() -> None:
    _running = True
    clock = pygame.time.Clock()
    while _running:
        events.process_events(pygame.event.get())
        keybinds.notify()
        if not rom_data.running:
            rw_data.save(rom_data.config_dir)
            _running = False
        manager.current_state().update()
        manager.current_state().render()
        rom_data.dt = clock.tick(rom_data.fps) / 100
        rom_data.window.blit(
            pygame.transform.scale_by(
                rom_data.abs_window, rom_data.scale_factor
            ),
            (0, 0),
        )
        pygame.display.flip()


if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
