import pygame

from config import Config


class Minimap:
    def __init__(self, world, config: Config, width=320, height=280, scale=4):
        self.config = config
        self.world = world
        self.width = width
        self.height = height
        self.scale = scale  # Combien de tiles par pixel
        self.last_render_pos = None
        self.surface = pygame.Surface((width, height))
        self.surface.set_alpha(150)

    def draw(self, player_pos):
        px, py = player_pos
        start_x = px - (self.width // self.scale) // 2
        start_y = py - (self.height // self.scale) // 2

        for i in range(0, self.width, self.scale):
            for j in range(0, self.height, self.scale):
                wx = start_x + i // self.scale
                wy = start_y + j // self.scale
                tile = self.world.get_tile(wx, wy)
                biome = self.world.biomes[tile.biome_name]
                color = biome.minimap_color if biome else (0, 0, 0)
                if tile.is_obstacle:
                    color = tuple(int(c * 0.8) for c in color)
                pygame.draw.rect(
                    self.surface,
                    color,
                    (i, j, self.scale, self.scale),
                )

        # Marqueur du joueur (en blanc)
        pygame.draw.rect(
            self.surface,
            (255, 255, 255),
            (self.width // 2 - 1, self.height // 2 - 1, 3, 3),
        )

    def blit_to(self, screen, position=(960, 360)):
        screen.blit(self.surface, position)
