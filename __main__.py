import sys

import pygame

import src


def main():
    _running = True
    clock = pygame.time.Clock()
    while _running:
        src.core.events.process_events(pygame.event.get())
        src.core.keybinds.notify()
        if not src.data.rom_data.running:
            src.data.rw_data.save(src.data.rom_data.config_dir)
            _running = False
        src.states.manager.current_state().update()
        src.states.manager.current_state().render()
        src.data.rom_data.dt = clock.tick(src.data.rom_data.fps) / 100
        src.data.rom_data.window.blit(
            pygame.transform.scale_by(
                src.data.rom_data.abs_window, src.data.rom_data.scale_factor
            ),
            (0, 0),
        )
        pygame.display.flip()

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
