import pygame
from sys import exit
from Game.Pacman import Pacman
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

    def draw_kaas(self, levelmap):
        tile_size = 30
        kleur = levelmap.kaasjes.kleur  # 🔥 direct gebruiken

        for (x, y) in levelmap.kaasjes.kaas_posities:
            pygame.draw.circle(
                self.window,
                kleur,
                (
                    x * tile_size + tile_size // 2,
                    y * tile_size + tile_size // 2
                ),
                5
            )

    def update(self):
        pygame.display.update()
        self.klok.tick(60)

    def run(self, game):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    game.handle_input(event)

            self.window.fill((0, 0, 0))
            self.draw_level(game.levelmap)
            self.draw_kaas(game.levelmap)
            game.pacman.draw(self.window, 30)
            for spook in game.spookjes:
                spook.draw(self.window, 30)
            for spook in game.spookjes:
                spook.random_move(game.levelmap)
            game.Pacman_Raakt_Spook()

            game.Pacman_eet_kaas()


            self.update()

        self.exit_game()



