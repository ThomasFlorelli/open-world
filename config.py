import os
from pprint import pprint

import yaml


class Config:
    def __init__(self, path):
        with open(path, "r") as f:
            self._data = yaml.safe_load(f)

    def __getitem__(self, key):
        return self._data.get(key.lower())

    @property
    def display_texture_size(self):
        return self["display_texture_size"]

    @property
    def player_settings(self):
        return self["player_settings"]

    @property
    def screen_height(self):
        return self["screen_height"]

    @property
    def screen_width(self):
        return self["screen_width"]

    @property
    def texture_path(self):
        return self["texture_path"]

    @property
    def texture_size(self):
        return self["texture_size"]

    @property
    def texture_index_map(self):
        return self["texture_index_map"]

    @property
    def viewport_height(self):
        return self["viewport_height"]

    @property
    def viewport_width(self):
        return self["viewport_width"]

    @property
    def biomes(self):
        return self["biomes"]


def test_loaded_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    config = Config(config_path)

    print("=== CONFIG SUMMARY ===")
    print(f"Texture path: {config.texture_path}")
    print(f"Texture size: {config.texture_size}")
    print(f"Display size: {config.display_texture_size}")
    print(f"Screen: {config.screen_width}x{config.screen_height}")
    print(f"Viewport: {config.viewport_width}x{config.viewport_height}")

    print("\n=== PLAYER SETTINGS ===")
    pass_through = config.player_settings["pass_through_obstacles"]
    base_speed = config.player_settings["base_speed"]
    print(f"Pass through obstacles: {pass_through}")
    print(f"Base speed: {base_speed}")

    print("\n=== TEXTURE INDEX MAP ===")
    pprint(config.texture_index_map)

    print("\n=== BIOMES FOUND ===\n")
    for biome_name, biome_config in config.biomes.items():
        print(
            f"== {biome_name} ==\n    Rarity: {biome_config['rarity']}\n"
            + f"    Minimap color: {biome_config['minimap_color']}\n    Terrains:"
        )
        print()
        for terrain in biome_config["terrains"]:
            print(
                f"        = {terrain['texture_suffix']} ="
                + f"\n        Rarity: {terrain['rarity']}"
            )


if __name__ == "__main__":
    test_loaded_config()
