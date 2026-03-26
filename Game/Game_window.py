import pygame
from sys import exit

import pygame


class GameWindow:
    def __init__(self, breedte, hoogte):
        self.breedte = breedte
        self.hoogte = hoogte
        self.window = pygame.display.set_mode((self.breedte, self.hoogte))
        pygame.display.set_caption("Pacman")
        self.klok = pygame.time.Clock()
        self.running = True

    def exit_game(self):
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def draw_level(self, levelmap):
        tile_size = 30

        for y, row in enumerate(levelmap.LEVEL_MAP1):
            for x, tile in enumerate(row):
                rect = pygame.Rect(
                    x * tile_size,
                    y * tile_size,
                    tile_size,
                    tile_size
                )

                if tile == "#":
                    pygame.draw.rect(self.window, (0, 0, 255), rect)
                else:
                    pygame.draw.rect(self.window, (0, 0, 0), rect)

    def update(self):
        pygame.display.update()
        self.klok.tick(60)

    def run(self, levelmap):
        while self.running:
            self.handle_events()
            self.window.fill((0, 0, 0))
            self.draw_level(levelmap)
            self.update()

        self.exit_game()



