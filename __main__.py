import sys

import pygame

import src


def main():
    _running = True
    clock = pygame.time.Clock()
    while _running:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    src.rom_data.running = False
        if not src.rom_data.running:
            print("quitting safely...")
            _running = False
        src.rom_data.dt = clock.tick(src.rom_data.fps) / 100
        src.rom_data.window.blit(
            pygame.transform.scale_by(
                src.rom_data.abs_window, src.rom_data.scale_factor
            ),
            (0, 0),
        )
        pygame.display.flip()

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()