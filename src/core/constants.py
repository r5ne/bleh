import pygame

from src.core.structs import Bidict

# convert from constant to name

DISPLAY_FLAG_NAMES_MAP = Bidict(
    {
        pygame.FULLSCREEN: "fullscreen",
        pygame.DOUBLEBUF: "doublebuf",
        pygame.HWSURFACE: "hwsurface",
        pygame.OPENGL: "opengl",
        pygame.NOFRAME: "noframe",
        pygame.RESIZABLE: "resizable",
        pygame.SCALED: "scaled",
        pygame.SHOWN: "shown",
        pygame.HIDDEN: "hidden",
    }
)
