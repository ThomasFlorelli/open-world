import os

import pygame

from config import Config
from render import DisplayManager, Renderer, TextureSet
from world import World


class Player:
    def __init__(self, pos_x: int, pos_y: int):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def move(self, delta_x: int, delta_y: int):
        self.pos_x += delta_x
        self.pos_y += delta_y


class Game:
    def __init__(self, config: Config):
        pygame.init()
        pygame.display.set_caption("Mini Roguelike")
        renderer = Renderer(
            config.SCREEN_WIDTH * config.DISPLAY_TEXTURE_SIZE,
            config.SCREEN_HEIGHT * config.DISPLAY_TEXTURE_SIZE,
        )
        textureset = TextureSet(
            config.TEXTURE_PATH, config.TEXTURE_SIZE, config.DISPLAY_TEXTURE_SIZE
        )
        self.display_manager = DisplayManager(textureset, renderer)
        self.renderer = renderer
        self.world = World()
        self.player = Player(0, 0)
        self.config = config

    def draw_viewport(self):
        px, py = (self.player.pos_x, self.player.pos_y)
        viewport_top_left_x, viewport_top_left_y = (
            px - self.config.VIEWPORT_WIDTH // 2,
            py - self.config.VIEWPORT_HEIGHT // 2,
        )

        for y in range(self.config.VIEWPORT_HEIGHT):
            tile_y = viewport_top_left_y + y
            for x in range(self.config.VIEWPORT_WIDTH):
                tile_x = viewport_top_left_x + x
                self.display_manager.draw(
                    self.world.get_tile(tile_x, tile_y).type, x, y
                )

        self.display_manager.draw(
            "player", self.config.VIEWPORT_WIDTH // 2, self.config.VIEWPORT_HEIGHT // 2
        )

    def loop(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player.move(0, -1)
                    elif event.key == pygame.K_DOWN:
                        self.player.move(0, 1)
                    elif event.key == pygame.K_LEFT:
                        self.player.move(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.player.move(1, 0)

            self.display_manager.clear_screen()

            self.draw_viewport()

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()


config_path = os.path.join(os.path.dirname(__file__), "config.json")
config = Config.from_json_file(config_path)
game = Game(config)
game.loop()
