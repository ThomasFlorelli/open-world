from chunk import CHUNK_SIZE, Chunk

from biome import Biome
from generation_config import GenerationConfig
from noise_map import NoiseMap
from threshold_selector import ThresholdSelector

CHUNK_GC_DISTANCE = 3
CHUNK_COLD_THRESHOLD = 2  # number of cold pass before collection


class World:
    def __init__(self, biomes: dict[str, Biome], generation_config: GenerationConfig):
        self.seed = generation_config.seed
        self.chunks = {}  # cache: (chunk_x, chunk_y) -> Chunk
        self.chunk_heat = {}  # (chunk_x, chunk_y) -> int
        self.zones = {}  # (zone_x, zone_y) -> Zone
        self.biomes = biomes
        self.noise_maps = {
            "biome": NoiseMap(
                seed=self.seed,
                scale=generation_config.biome_scale,
                smoothing=generation_config.biome_noise_smoothing,
            ),
            "terrain": NoiseMap(
                seed=self.seed,
                scale=generation_config.terrain_scale,
                smoothing=generation_config.terrain_noise_smoothing,
            ),
        }
        self.threshold_selectors = {
            "biome": ThresholdSelector(
                seed=self.seed, thresholds=generation_config.biome_rarity_thresholds
            ),
            "terrain": ThresholdSelector(
                seed=self.seed, thresholds=generation_config.terrain_rarity_thresholds
            ),
        }

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
            self.chunks[key] = Chunk(
                chunk_x,
                chunk_y,
                self.seed,
                self.biomes,
                noise_maps=self.noise_maps,
                threshold_selectors=self.threshold_selectors,
            )
            self.chunk_heat[key] = CHUNK_COLD_THRESHOLD
        return self.chunks[key]

    def update_chunks(self, player_x, player_y):
        player_chunk_x = player_x // CHUNK_SIZE
        player_chunk_y = player_y // CHUNK_SIZE
        to_remove = []

        for coords in self.chunks.keys():
            chunk_x, chunk_y = coords
            dist_sq = (chunk_x - player_chunk_x) ** 2 + (chunk_y - player_chunk_y) ** 2

            if dist_sq <= CHUNK_GC_DISTANCE**2:
                self.chunk_heat[coords] = CHUNK_COLD_THRESHOLD  # reheat the chunk
            else:
                self.chunk_heat[coords] -= 1
                if self.chunk_heat[coords] <= 0:
                    to_remove.append(coords)

        for coords in to_remove:
            del self.chunks[coords]
