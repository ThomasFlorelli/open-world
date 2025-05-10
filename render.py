import pygame


class TextureSet:
    # Indexes (row, column)
    TEXTURE_INDEXES = {
        "grass": (4, 9),
        "rock": (9, 10),
        "player": (4, 33),
    }

    def __init__(self, file_path: str, texture_size: int, display_texture_size: int):
        self.texture_size = texture_size
        self.display_texture_size = display_texture_size
        self.texturesheet = pygame.image.load(file_path).convert_alpha()
        self.textures = {
            name: self.load_texture(idx) for name, idx in self.TEXTURE_INDEXES.items()
        }

    def load_texture(self, index):
        x, y = index
        rect = pygame.Rect(
            x * self.texture_size,
            y * self.texture_size,
            self.texture_size,
            self.texture_size,
        )
        return pygame.transform.scale(
            self.texturesheet.subsurface(rect).copy(),
            (self.display_texture_size, self.display_texture_size),
        )

    def get_texture(self, name):
        return self.textures[name]


class Renderer:
    def __init__(self, screen_width, screen_height):
        self.screen = pygame.display.set_mode((screen_width, screen_height))

    def clear_screen(self):
        self.screen.fill((0, 0, 0))

    def draw_texture(self, texture, coords):
        self.screen.blit(texture, coords)


class DisplayManager:
    def __init__(self, texture_set: TextureSet, renderer: Renderer):
        self.texture_set = texture_set
        self.renderer = renderer

    def clear_screen(self):
        self.renderer.clear_screen()

    def draw(self, texture_name: str, x: int, y: int):
        texture = self.texture_set.get_texture(texture_name)
        self.renderer.draw_texture(
            texture,
            (
                x * self.texture_set.display_texture_size,
                y * self.texture_set.display_texture_size,
            ),
        )
