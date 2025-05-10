import os
import sys

import pygame

pygame.init()
path = os.path.join(os.path.dirname(__file__), "../assets/The Roguelike 1-14-8.png")

spritesheet = pygame.image.load(path)
TILE_SIZE = 32

spritesheet = pygame.transform.scale(
    pygame.image.load(path), (spritesheet.get_width() * 2, spritesheet.get_height() * 2)
)
cols = spritesheet.get_width() // TILE_SIZE
rows = spritesheet.get_height() // TILE_SIZE

screen = pygame.display.set_mode((spritesheet.get_width(), spritesheet.get_height()))
font = pygame.font.SysFont(None, 18)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(spritesheet, (0, 0))

    # Dessiner la grille et les indices
    for y in range(rows):
        for x in range(cols):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)
            text = font.render(f"{x},{y}", True, (255, 255, 0))
            screen.blit(text, (x * TILE_SIZE + 1, y * TILE_SIZE + 1))

    pygame.display.flip()
