import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict

import yaml


class NoiseSmoothing(str, Enum):
    LINEAR = "linear"  # map [-1, 1] -> [0, 1] (simple rescale)
    FAVOR_COMMON = "favor_common"  # pow(x, 2.2)
    FAVOR_RARE = "favor_rare"  # 1 - pow(1 - x, 2.2)


@dataclass
class GenerationConfig:
    seed: int = 12345
    biome_scale: int = 64
    terrain_scale: int = 32
    biome_rarity_thresholds: Dict[str, float] = field(
        default_factory=lambda: {
            "legendary": 0.97,
            "rare": 0.85,
            "uncommon": 0.5,
            "common": 0.0,
        }
    )
    terrain_rarity_thresholds: Dict[str, float] = field(
        default_factory=lambda: {
            "legendary": 0.97,
            "rare": 0.85,
            "uncommon": 0.5,
            "common": 0.0,
        }
    )
    biome_noise_smoothing: NoiseSmoothing = NoiseSmoothing.FAVOR_COMMON
    terrain_noise_smoothing: NoiseSmoothing = NoiseSmoothing.FAVOR_COMMON
    zone_size: int = 100

    @staticmethod
    def load_from_yaml(path: str) -> "GenerationConfig":
        with open(path, "r") as f:
            data = yaml.safe_load(f)
            return GenerationConfig(
                seed=data["seed"],
                biome_scale=data["biome_scale"],
                terrain_scale=data["terrain_scale"],
                biome_rarity_thresholds=data["biome_rarity_thresholds"],
                terrain_rarity_thresholds=data["biome_rarity_thresholds"],
                zone_size=data["zone_size"],
                biome_noise_smoothing=NoiseSmoothing(data["biome_noise_smoothing"]),
                terrain_noise_smoothing=NoiseSmoothing(data["terrain_noise_smoothing"]),
            )

    def to_yaml(self, path: str):
        with open(path, "w") as f:
            yaml.safe_dump(
                {
                    "seed": self.seed,
                    "biome_scale": self.biome_scale,
                    "terrain_scale": self.terrain_scale,
                    "biome_rarity_thresholds": self.biome_rarity_thresholds,
                    "terrain_rarity_thresholds": self.terrain_rarity_thresholds,
                    "zone_size": self.zone_size,
                    "biome_noise_smoothing": self.biome_noise_smoothing.value,
                    "terrain_noise_smoothing": self.terrain_noise_smoothing.value,
                },
                f,
            )


def print_loaded_generation_config():
    generation_config_path = os.path.join(
        os.path.dirname(__file__), "generation_config.yaml"
    )
    try:
        config = GenerationConfig.load_from_yaml(generation_config_path)
        print("=== GenerationConfig Loaded ===")
        print(f"Seed: {config.seed}")
        print(f"Biome Scale: {config.biome_scale}")
        print(f"Terrain Scale: {config.terrain_scale}")
        print(f"Biome Rarity Thresholds: {config.biome_rarity_thresholds}")
        print(f"Terrain Rarity Thresholds: {config.terrain_rarity_thresholds}")
        print(f"Zone Size: {config.zone_size}")
        print(f"Biome Noise Smoothing: {config.biome_noise_smoothing}")
        print(f"Terrain Noise Smoothing: {config.terrain_noise_smoothing}")
    except Exception as e:
        print(f"Failed to load GenerationConfig: {e}")


if __name__ == "__main__":
    print_loaded_generation_config()
