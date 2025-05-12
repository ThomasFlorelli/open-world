class Terrain:
    def __init__(self, texture_suffix, is_obstacle, rarity, biome_name):
        self.texture_id = f"{biome_name}_{texture_suffix}"
        self.texture_suffix = texture_suffix
        self.is_obstacle = is_obstacle
        self.rarity = rarity

    @staticmethod
    def from_dict(data, biome_name: str):
        return Terrain(
            texture_suffix=data["texture_suffix"],
            is_obstacle=data["is_obstacle"],
            rarity=data["rarity"],
            biome_name=biome_name,
        )


class Biome:
    def __init__(self, name, rarity, terrains):
        self.name = name
        self.rarity = rarity
        self.terrains = {terrain.texture_suffix: terrain for terrain in terrains}
        self.terrain_rarities = {
            name: terrain.rarity for name, terrain in self.terrains.items()
        }

    @staticmethod
    def from_dict(name, data):
        terrains = [Terrain.from_dict(t, name) for t in data.get("terrains", [])]
        return Biome(name, data.get("rarity", "common"), terrains)
