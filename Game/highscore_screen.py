import pygame
import sqlite3


class HighscoreScreen:
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height

    def get_top_10_scores(self):
        conn = sqlite3.connect("Pacman.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name, score
            FROM scores
            ORDER BY score DESC
            LIMIT 10
        """)

        scores = cursor.fetchall()
        conn.close()
        return scores

    def show(self, current_score):
        font_title = pygame.font.SysFont(None, 60)
        font_text = pygame.font.SysFont(None, 36)
        font_small = pygame.font.SysFont(None, 28)

        scores = self.get_top_10_scores()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            self.window.fill((0, 0, 0))

            # Titel
            title = font_title.render("GAME OVER", True, (255, 255, 0))
            self.window.blit(title, (self.width // 2 - 140, 50))

            # Huidige score
            current = font_text.render(
                f"Jouw score: {current_score}", True, (255, 255, 255)
            )
            self.window.blit(current, (self.width // 2 - 120, 130))

            # Highscore titel
            highscore_title = font_text.render(
                "Top 10 Highscores", True, (0, 255, 255)
            )
            self.window.blit(highscore_title, (self.width // 2 - 140, 200))

            # Scores lijst
            y = 260
            for i, (name, score) in enumerate(scores, start=1):
                text = f"{i}. {name} - {score}"
                score_text = font_small.render(text, True, (255, 255, 255))
                self.window.blit(score_text, (self.width // 2 - 140, y))
                y += 35

            # Exit tekst
            exit_text = font_small.render(
                "Druk op ESC om te sluiten", True, (200, 200, 200)
            )
            self.window.blit(exit_text, (self.width // 2 - 150, self.height - 50))

            pygame.display.update()

