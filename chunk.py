import random

from tile import Tile

CHUNK_SIZE = 16  # 16x16 tiles


class Chunk:
    def __init__(self, chunk_x: int, chunk_y: int, seed: int):
        self.chunk_x = chunk_x
        self.chunk_y = chunk_y
        self.seed = seed
        self.tiles = self.generate_tiles()

    def generate_tiles(self):
        rng = random.Random(self.get_chunk_seed())
        tiles = []
        for y in range(CHUNK_SIZE):
            row = []
            for x in range(CHUNK_SIZE):
                tile_type = "grass" if rng.random() < 0.8 else "rock"
                row.append(Tile(type=tile_type))
            tiles.append(row)
        return tiles

    def get_tile(self, local_x: int, local_y: int) -> Tile:
        return self.tiles[local_y][local_x]

    def get_chunk_seed(self):
        return hash((self.seed, self.chunk_x, self.chunk_y))
