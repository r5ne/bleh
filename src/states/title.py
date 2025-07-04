from typing import override

from src.states.state import State
from src.states.manager import append_state


class Title(State):
    def __init__(self):
        super().__init__()
        self.background.fill((255, 100, 100))

    @override
    def back(self) -> None:
        append_state("game")
