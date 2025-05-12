from chunk import CHUNK_SIZE

import pygame

from biome import Biome
from config import Config
from generation_config import GenerationConfig
from render import DisplayManager, Renderer, TextureSet
from world import World


class Player:
    def __init__(
        self, pos_x: int, pos_y: int, pass_through_obstacles: bool, base_speed: int = 1
    ):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = base_speed
        self.pass_through_obstacles = pass_through_obstacles

    def move(self, delta_x: int, delta_y: int):
        self.pos_x += delta_x * self.speed
        self.pos_y += delta_y * self.speed


class Game:
    def __init__(self, config: Config, generation_config: GenerationConfig):
        pygame.init()
        pygame.display.set_caption("Mini Roguelike")
        renderer = Renderer(
            config.screen_width * config.display_texture_size,
            config.screen_height * config.display_texture_size,
        )
        textureset = TextureSet(
            config.texture_index_map,
            config.texture_path,
            config.texture_size,
            config.display_texture_size,
        )
        self.display_manager = DisplayManager(textureset, renderer)
        self.renderer = renderer
        self.world = World(
            {
                biome_name: Biome.from_dict(biome_name, biome_data)
                for biome_name, biome_data in config.biomes.items()
            },
            generation_config=generation_config,
        )
        self.player = Player(
            0,
            0,
            config.player_settings["pass_through_obstacles"],
            config.player_settings["base_speed"],
        )
        self.player_chunk = (0, 0)
        self.config = config
        self.held_keys = set()

    def draw_viewport(self):
        px, py = (self.player.pos_x, self.player.pos_y)
        viewport_top_left_x, viewport_top_left_y = (
            px - self.config.viewport_width // 2,
            py - self.config.viewport_height // 2,
        )

        for y in range(self.config.viewport_height):
            tile_y = viewport_top_left_y + y
            for x in range(self.config.viewport_width):
                tile_x = viewport_top_left_x + x
                self.display_manager.draw(
                    self.world.get_tile(tile_x, tile_y).type, x, y
                )

        self.display_manager.draw(
            "player", self.config.viewport_width // 2, self.config.viewport_height // 2
        )

    def loop(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.held_keys.add(event.key)
                elif event.type == pygame.KEYUP:
                    self.held_keys.discard(event.key)

            dx, dy = 0, 0

            if pygame.K_LEFT in self.held_keys:
                dx -= 1
            elif pygame.K_RIGHT in self.held_keys:
                dx += 1
            elif pygame.K_UP in self.held_keys:
                dy -= 1
            elif pygame.K_DOWN in self.held_keys:
                dy += 1

            next_tile = self.world.get_tile(
                self.player.pos_x + dx, self.player.pos_y + dy
            )
            if self.player.pass_through_obstacles or not next_tile.is_obstacle:
                self.player.move(dx, dy)

            player_chunk = (
                self.player.pos_x // CHUNK_SIZE,
                self.player.pos_y // CHUNK_SIZE,
            )

            if player_chunk != self.player_chunk:
                self.player_chunk = player_chunk
                self.world.update_chunks(*player_chunk)

            self.display_manager.clear_screen()

            self.draw_viewport()

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
