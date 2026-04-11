import pygame
from highscore_screen import HighscoreScreen


class GameWindow:
    def __init__(self, window, breedte, hoogte, mqtt_handler):
        self.window = window
        self.breedte = breedte
        self.hoogte = hoogte
        self.mqtt_handler = mqtt_handler
        self.klok = pygame.time.Clock()
        self.running = True

    def exit_game(self):
        pygame.quit()

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
        kleur = levelmap.kaasjes.kleur

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

    def draw_players(self):
        """
        Teken alle spelers uit MQTT state.
        """
        tile_size = 30

        for player_id, player in self.mqtt_handler.players_state.items():
            x = player["x"] * tile_size + tile_size // 2
            y = player["y"] * tile_size + tile_size // 2

            if player_id == self.mqtt_handler.player_id:
                kleur = (255, 255, 0)   # jouw pacman
            else:
                kleur = (0, 255, 0)     # andere spelers

            pygame.draw.circle(self.window, kleur, (x, y), tile_size // 2 - 4)

    def draw_spoken(self, game):
        """
        Spoken blijven voorlopig uit je bestaande game-object komen.
        """
        for spook in game.spookjes:
            spook.draw(self.window, 30)

    def update(self):
        pygame.display.update()
        self.klok.tick(10)

    def run(self, game):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    game.handle_input(event)

            # Alleen host verwerkt echte game logica
            if self.mqtt_handler.is_host:
                for spook in game.spookjes:
                    spook.random_move(game.levelmap)

                game.host_tick()

            # Scherm tekenen
            self.window.fill((0, 0, 0))
            self.draw_level(game.levelmap)
            self.draw_kaas(game.levelmap)
            self.draw_players()
            self.draw_spoken(game)

            # Game over voorlopig alleen voor lokale host-speler
            if self.mqtt_handler.is_host:
                if game.check_game_over():
                    highscore_screen = HighscoreScreen(self.window, self.breedte, self.hoogte)
                    highscore_screen.show(game.pacman.score)
                    self.running = False

            self.update()

        self.exit_game()