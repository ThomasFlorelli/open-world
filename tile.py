from dataclasses import dataclass

WALKABLE_TILES = ["grass"]

@dataclass
class Tile:
    type: str  # Ex: "grass", "water", etc.
    walkable: bool = False
    
    
    def __post_init__(self):
        if self.type in WALKABLE_TILES:
            self.walkable = True