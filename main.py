import os

try:
    import pygame  # noqa: F401
except ImportError:
    pass

from config import Config
from game import Game
from generation_config import GenerationConfig

config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
generation_config_path = os.path.join(
    os.path.dirname(__file__), "generation_config.yaml"
)
generation_config = GenerationConfig.load_from_yaml(generation_config_path)
config = Config(config_path)
game = Game(config, generation_config)
game.loop()
