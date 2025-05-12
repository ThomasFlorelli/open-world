from dataclasses import dataclass


@dataclass
class Tile:
    type: str
    is_obstacle: bool
