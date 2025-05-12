from biome import Biome
from noise_map import NoiseMap
from threshold_selector import ThresholdSelector
from tile import Tile

CHUNK_SIZE = 16
ZONE_SIZE = 64


class Chunk:
    def __init__(
        self,
        chunk_x: int,
        chunk_y: int,
        seed: int,
        biomes: dict[str, Biome],
        noise_maps: dict[str, NoiseMap],
        threshold_selectors: dict[str, ThresholdSelector],
    ):
        self.chunk_x = chunk_x
        self.chunk_y = chunk_y
        self.seed = seed
        self.biomes = biomes
        self.noise_maps = noise_maps
        self.threshold_selectors = threshold_selectors
        self.tiles = self.generate_tiles()

    def generate_tiles(self):
        biome_rarities = {name: biome.rarity for name, biome in self.biomes.items()}
        chunk_seed = self.get_chunk_seed()

        tiles = []
        for y in range(CHUNK_SIZE):
            row = []
            for x in range(CHUNK_SIZE):
                abs_x = self.chunk_x * CHUNK_SIZE + x
                abs_y = self.chunk_y * CHUNK_SIZE + y
                zone_seed = hash((self.seed, abs_x // ZONE_SIZE, abs_y // ZONE_SIZE))
                biome_noise = self.noise_maps["biome"].generate_global_noise(
                    abs_x, abs_y, seed=zone_seed
                )
                terrain_noise = self.noise_maps["terrain"].generate_global_noise(
                    abs_x, abs_y, seed=chunk_seed
                )
                biome_name = self.threshold_selectors["biome"].threshold_selection(
                    biome_noise, biome_rarities, seed=zone_seed
                )
                biome = self.biomes[biome_name]
                terrain_name = self.threshold_selectors["terrain"].threshold_selection(
                    terrain_noise, biome.terrain_rarities, seed=chunk_seed
                )
                terrain = biome.terrains[terrain_name]
                row.append(
                    Tile(
                        type=terrain.texture_id,
                        is_obstacle=terrain.is_obstacle,
                        biome_name=biome_name,
                    )
                )
            tiles.append(row)
        return tiles

    def get_tile(self, local_x: int, local_y: int) -> Tile:
        return self.tiles[local_y][local_x]

    def get_chunk_seed(self):
        return hash((self.seed, self.chunk_x, self.chunk_y))
