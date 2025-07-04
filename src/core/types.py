from typing import Literal

RectAlignments = Literal[
    "topleft",
    "midtop",
    "topright",
    "midleft",
    "center",
    "midright",
    "bottomleft",
    "midbottom",
    "bottomright",
]
EventTypes = Literal["key", "keydown", "keyup", "mouse", "mousedown", "mouseup", "quit"]
