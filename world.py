import random
from chunk import Chunk, CHUNK_SIZE

class World:
    def __init__(self, seed: int = 12345):
        self.seed = seed
        self.chunks = {}  # cache: (chunk_x, chunk_y) -> Chunk

    def get_tile(self, world_x: int, world_y: int):
        chunk_x = world_x // CHUNK_SIZE
        chunk_y = world_y // CHUNK_SIZE
        local_x = world_x % CHUNK_SIZE
        local_y = world_y % CHUNK_SIZE

        chunk = self.get_chunk(chunk_x, chunk_y)
        return chunk.get_tile(local_x, local_y)

    def get_chunk(self, chunk_x: int, chunk_y: int):
        key = (chunk_x, chunk_y)
        if key not in self.chunks:
            self.chunks[key] = Chunk(chunk_x, chunk_y, self.seed)
        return self.chunks[key]
                                       