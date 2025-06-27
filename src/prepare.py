import pygame
from src.data import rom_data

pygame.init()
pygame.display.set_caption(f"bleh v{rom_data.version}")
rom_data.screen = pygame.display.set_mode(
    (1920, 1080), pygame.SCALED | pygame.FULLSCREEN
)
rom_data.screen_rect = rom_data.screen.get_rect()
rom_data.running = True