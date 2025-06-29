from src.data import rom_data
from src.states.manager import pop_state

class State:
    def __init__(self):
        self.background = None

    def startup(self):
        if self.background is None:
            msg = "Failed to define self.background at __init__."
            raise ValueError(msg)

    def cleanup(self):
        ...

    def render(self):
        rom_data.abs_window.blit(self.background, (0, 0))

    def update(self):
        ...

    def back(self):
        pop_state()
